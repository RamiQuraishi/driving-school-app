/**
 * Sync reducer for managing data synchronization.
 * Handles offline changes, conflict resolution, and version tracking.
 */

import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    isOnline: true,
    isSyncing: false,
    lastSync: null,
    pendingChanges: [],
    conflicts: [],
    versions: {
        local: {},
        remote: {},
        lastSynced: {}
    },
    syncErrors: [],
    retryCount: 0,
    maxRetries: 3
};

const syncSlice = createSlice({
    name: 'sync',
    initialState,
    reducers: {
        setOnlineStatus: (state, action) => {
            state.isOnline = action.payload;
        },
        startSync: (state) => {
            state.isSyncing = true;
            state.syncErrors = [];
        },
        completeSync: (state, action) => {
            state.isSyncing = false;
            state.lastSync = Date.now();
            state.retryCount = 0;
            state.pendingChanges = [];
            state.conflicts = [];
            state.versions.lastSynced = { ...state.versions.local };
        },
        addPendingChange: (state, action) => {
            const { entity, id, type, data, version } = action.payload;
            state.pendingChanges.push({
                id: `${entity}-${id}-${Date.now()}`,
                entity,
                type,
                data,
                version,
                timestamp: Date.now()
            });
            state.versions.local[`${entity}-${id}`] = version;
        },
        removePendingChange: (state, action) => {
            state.pendingChanges = state.pendingChanges.filter(
                change => change.id !== action.payload
            );
        },
        addConflict: (state, action) => {
            const { entity, id, local, remote } = action.payload;
            state.conflicts.push({
                id: `${entity}-${id}`,
                entity,
                local,
                remote,
                timestamp: Date.now()
            });
        },
        resolveConflict: (state, action) => {
            const { conflictId, resolution } = action.payload;
            state.conflicts = state.conflicts.filter(
                conflict => conflict.id !== conflictId
            );
            if (resolution === 'local') {
                state.versions.remote[conflictId] = state.versions.local[conflictId];
            } else {
                state.versions.local[conflictId] = state.versions.remote[conflictId];
            }
        },
        updateVersion: (state, action) => {
            const { entity, id, version, source } = action.payload;
            const key = `${entity}-${id}`;
            state.versions[source][key] = version;
        },
        addSyncError: (state, action) => {
            state.syncErrors.push({
                ...action.payload,
                timestamp: Date.now()
            });
            state.retryCount += 1;
        },
        clearSyncErrors: (state) => {
            state.syncErrors = [];
            state.retryCount = 0;
        },
        resetSync: (state) => {
            return { ...initialState, isOnline: state.isOnline };
        }
    }
});

export const {
    setOnlineStatus,
    startSync,
    completeSync,
    addPendingChange,
    removePendingChange,
    addConflict,
    resolveConflict,
    updateVersion,
    addSyncError,
    clearSyncErrors,
    resetSync
} = syncSlice.actions;

// Selectors
export const selectIsOnline = (state) => state.sync.isOnline;
export const selectIsSyncing = (state) => state.sync.isSyncing;
export const selectPendingChanges = (state) => state.sync.pendingChanges;
export const selectConflicts = (state) => state.sync.conflicts;
export const selectSyncErrors = (state) => state.sync.syncErrors;
export const selectVersions = (state) => state.sync.versions;
export const selectRetryCount = (state) => state.sync.retryCount;

export default syncSlice.reducer; 