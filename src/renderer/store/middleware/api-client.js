/**
 * API Client middleware for handling unified API calls.
 * Provides request caching, retry logic, and error handling.
 */

import { createAction } from '@reduxjs/toolkit';
import { isRejectedWithValue } from '@reduxjs/toolkit/query';

// Action types
const API_REQUEST = 'api/request';
const API_SUCCESS = 'api/success';
const API_FAILURE = 'api/failure';
const API_CACHE_HIT = 'api/cacheHit';
const API_CACHE_MISS = 'api/cacheMiss';

// Action creators
export const apiRequest = createAction(API_REQUEST);
export const apiSuccess = createAction(API_SUCCESS);
export const apiFailure = createAction(API_FAILURE);
export const apiCacheHit = createAction(API_CACHE_HIT);
export const apiCacheMiss = createAction(API_CACHE_MISS);

// Cache management
const cache = new Map();
const pendingRequests = new Map();

const getCacheKey = (endpoint, params) => {
    return `${endpoint}:${JSON.stringify(params)}`;
};

const createApiClientMiddleware = (config = {}) => {
    const {
        baseUrl = '/api',
        defaultHeaders = {
            'Content-Type': 'application/json'
        },
        cacheTime = 5 * 60 * 1000, // 5 minutes
        maxRetries = 3,
        retryDelay = 1000,
        timeout = 30000, // 30 seconds
        onError = console.error
    } = config;

    const fetchWithTimeout = async (url, options, timeout) => {
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), timeout);

        try {
            const response = await fetch(url, {
                ...options,
                signal: controller.signal
            });
            clearTimeout(id);
            return response;
        } catch (error) {
            clearTimeout(id);
            throw error;
        }
    };

    const makeRequest = async (endpoint, options = {}) => {
        const {
            method = 'GET',
            params = {},
            body,
            headers = {},
            retryCount = 0,
            useCache = true
        } = options;

        const url = new URL(`${baseUrl}${endpoint}`);
        Object.entries(params).forEach(([key, value]) => {
            url.searchParams.append(key, value);
        });

        const cacheKey = getCacheKey(endpoint, params);
        const cachedResponse = cache.get(cacheKey);

        if (useCache && cachedResponse && Date.now() - cachedResponse.timestamp < cacheTime) {
            return {
                data: cachedResponse.data,
                fromCache: true
            };
        }

        try {
            const response = await fetchWithTimeout(url.toString(), {
                method,
                headers: {
                    ...defaultHeaders,
                    ...headers
                },
                body: body ? JSON.stringify(body) : undefined
            }, timeout);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (useCache) {
                cache.set(cacheKey, {
                    data,
                    timestamp: Date.now()
                });
            }

            return {
                data,
                fromCache: false
            };
        } catch (error) {
            if (retryCount < maxRetries) {
                await new Promise(resolve => setTimeout(resolve, retryDelay * (retryCount + 1)));
                return makeRequest(endpoint, {
                    ...options,
                    retryCount: retryCount + 1
                });
            }
            throw error;
        }
    };

    return ({ dispatch }) => {
        return (next) => async (action) => {
            if (action.type !== API_REQUEST) {
                return next(action);
            }

            const { endpoint, options = {}, meta = {} } = action.payload;
            const requestId = meta.requestId || Date.now().toString();

            // Check for duplicate requests
            if (pendingRequests.has(requestId)) {
                return pendingRequests.get(requestId);
            }

            const requestPromise = (async () => {
                try {
                    const { data, fromCache } = await makeRequest(endpoint, options);

                    if (fromCache) {
                        dispatch(apiCacheHit({ endpoint, requestId }));
                    } else {
                        dispatch(apiCacheMiss({ endpoint, requestId }));
                    }

                    dispatch(apiSuccess({
                        endpoint,
                        data,
                        requestId,
                        meta
                    }));

                    return data;
                } catch (error) {
                    dispatch(apiFailure({
                        endpoint,
                        error,
                        requestId,
                        meta
                    }));

                    onError('API request failed:', error);
                    throw error;
                } finally {
                    pendingRequests.delete(requestId);
                }
            })();

            pendingRequests.set(requestId, requestPromise);
            return requestPromise;
        };
    };
};

export default createApiClientMiddleware; 