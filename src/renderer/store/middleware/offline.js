/**
 * Offline middleware for handling offline data synchronization.
 * Provides version tracking, conflict detection, and automatic sync.
 */

import { createAction } from '@reduxjs/toolkit';
import { isRejectedWithValue } from '@reduxjs/toolkit/query';
import { v4 as uuidv4 } from 'uuid';

// Action types
const OFFLINE_ACTION = 'offline/action';
const SYNC_STARTED = 'offline/syncStarted';
const SYNC_COMPLETED = 'offline/syncCompleted';
const SYNC_FAILED = 'offline/syncFailed';

// Action creators
export const offlineAction = createAction(OFFLINE_ACTION);
export const syncStarted = createAction(SYNC_STARTED);
export const syncCompleted = createAction(SYNC_COMPLETED);
export const syncFailed = createAction(SYNC_FAILED);

// Queue management
const queue = new Map();
const versionMap = new Map();

const getEntityVersion = (entity, id) => {
    const key = `${entity}-${id}`;
    return versionMap.get(key) || 0;
};

const incrementEntityVersion = (entity, id) => {
    const key = `${entity}-${id}`;
    const version = getEntityVersion(entity, id) + 1;
    versionMap.set(key, version);
    return version;
};

const createOfflineMiddleware = (config = {}) => {
    const {
        retryInterval = 5000,
        maxRetries = 3,
        syncOnReconnect = true,
        syncOnStart = true,
        versionTracking = true
    } = config;

    return ({ dispatch, getState }) => {
        let syncTimer = null;
        let retryCount = 0;

        const processQueue = async () => {
            if (queue.size === 0) return;

            dispatch(syncStarted());

            try {
                for (const [id, action] of queue) {
                    const { type, payload, meta } = action;
                    const { entity, id: entityId } = meta;

                    if (versionTracking) {
                        const version = incrementEntityVersion(entity, entityId);
                        meta.version = version;
                    }

                    const result = await dispatch(action);
                    
                    if (isRejectedWithValue(result)) {
                        throw new Error(result.error);
                    }

                    queue.delete(id);
                }

                dispatch(syncCompleted());
                retryCount = 0;
            } catch (error) {
                console.error('Sync failed:', error);
                dispatch(syncFailed(error));

                if (retryCount < maxRetries) {
                    retryCount++;
                    syncTimer = setTimeout(processQueue, retryInterval);
                }
            }
        };

        const startSync = () => {
            if (syncTimer) {
                clearTimeout(syncTimer);
            }
            processQueue();
        };

        // Handle reconnection
        if (syncOnReconnect) {
            window.addEventListener('online', startSync);
        }

        // Initial sync
        if (syncOnStart) {
            setTimeout(startSync, 1000);
        }

        return (next) => (action) => {
            if (action.type === OFFLINE_ACTION) {
                const { payload, meta } = action;
                const id = uuidv4();

                queue.set(id, {
                    ...payload,
                    meta: {
                        ...meta,
                        offline: true,
                        id
                    }
                });

                startSync();
                return;
            }

            return next(action);
        };
    };
};

export default createOfflineMiddleware; 