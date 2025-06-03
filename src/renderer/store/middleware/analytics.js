/**
 * Analytics middleware for tracking user actions and application events.
 * Provides event tracking, user behavior analysis, and performance monitoring.
 */

import { createAction } from '@reduxjs/toolkit';

// Action types
const TRACK_EVENT = 'analytics/trackEvent';
const TRACK_ERROR = 'analytics/trackError';
const TRACK_PERFORMANCE = 'analytics/trackPerformance';
const TRACK_USER_ACTION = 'analytics/trackUserAction';

// Action creators
export const trackEvent = createAction(TRACK_EVENT);
export const trackError = createAction(TRACK_ERROR);
export const trackPerformance = createAction(TRACK_PERFORMANCE);
export const trackUserAction = createAction(TRACK_USER_ACTION);

// Event categories
const EVENT_CATEGORIES = {
    NAVIGATION: 'navigation',
    INTERACTION: 'interaction',
    PERFORMANCE: 'performance',
    ERROR: 'error',
    FEATURE: 'feature',
    SYNC: 'sync'
};

// Analytics queue
const queue = [];
let isProcessing = false;
let batchSize = 10;
let flushInterval = 30000; // 30 seconds

const createAnalyticsMiddleware = (config = {}) => {
    const {
        enabled = true,
        debug = false,
        endpoint = '/api/analytics',
        batchSize: customBatchSize,
        flushInterval: customFlushInterval,
        onError = console.error
    } = config;

    if (customBatchSize) batchSize = customBatchSize;
    if (customFlushInterval) flushInterval = customFlushInterval;

    const processQueue = async () => {
        if (!enabled || isProcessing || queue.length === 0) return;

        isProcessing = true;
        const batch = queue.splice(0, batchSize);

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    events: batch,
                    timestamp: Date.now()
                })
            });

            if (!response.ok) {
                throw new Error(`Analytics request failed: ${response.statusText}`);
            }

            if (debug) {
                console.log('Analytics batch sent:', batch);
            }
        } catch (error) {
            onError('Analytics error:', error);
            // Put failed events back in queue
            queue.unshift(...batch);
        } finally {
            isProcessing = false;
        }
    };

    // Set up periodic flush
    const flushTimer = setInterval(processQueue, flushInterval);

    return ({ getState }) => {
        const trackAnalyticsEvent = (action) => {
            const state = getState();
            const { user } = state.auth;
            const { isOnline } = state.sync;

            const event = {
                type: action.type,
                payload: action.payload,
                timestamp: Date.now(),
                userId: user?.id,
                sessionId: state.auth.sessionId,
                isOnline,
                userAgent: navigator.userAgent,
                screenSize: {
                    width: window.innerWidth,
                    height: window.innerHeight
                }
            };

            queue.push(event);

            if (queue.length >= batchSize) {
                processQueue();
            }
        };

        return (next) => (action) => {
            const result = next(action);

            // Track specific action types
            if (action.type.startsWith('analytics/')) {
                trackAnalyticsEvent(action);
            }

            // Track errors
            if (action.type.endsWith('/rejected')) {
                trackAnalyticsEvent({
                    type: TRACK_ERROR,
                    payload: {
                        error: action.error,
                        originalAction: action.meta?.arg
                    }
                });
            }

            // Track performance metrics
            if (action.type === 'performance/updateMetrics') {
                trackAnalyticsEvent({
                    type: TRACK_PERFORMANCE,
                    payload: action.payload
                });
            }

            return result;
        };
    };
};

export {
    EVENT_CATEGORIES,
    createAnalyticsMiddleware as default
}; 