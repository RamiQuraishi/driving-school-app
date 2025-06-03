/**
 * Conflicts reducer for managing data conflicts and resolutions.
 * Handles conflict detection, resolution strategies, and history.
 */

import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    activeConflicts: [],
    resolvedConflicts: [],
    resolutionStrategy: 'manual', // manual, auto-local, auto-remote, merge
    autoResolveEnabled: false,
    mergeStrategy: 'smart', // smart, local-wins, remote-wins
    conflictHistory: [],
    lastResolved: null,
    stats: {
        total: 0,
        resolved: 0,
        pending: 0,
        autoResolved: 0
    }
};

const conflictsSlice = createSlice({
    name: 'conflicts',
    initialState,
    reducers: {
        addConflict: (state, action) => {
            const conflict = {
                id: Date.now(),
                timestamp: new Date().toISOString(),
                status: 'pending',
                ...action.payload
            };
            state.activeConflicts.push(conflict);
            state.stats.total += 1;
            state.stats.pending += 1;
        },
        resolveConflict: (state, action) => {
            const { conflictId, resolution, strategy } = action.payload;
            const conflict = state.activeConflicts.find(c => c.id === conflictId);
            
            if (conflict) {
                conflict.status = 'resolved';
                conflict.resolution = resolution;
                conflict.resolutionStrategy = strategy;
                conflict.resolvedAt = new Date().toISOString();
                
                state.resolvedConflicts.push(conflict);
                state.activeConflicts = state.activeConflicts.filter(c => c.id !== conflictId);
                state.lastResolved = conflict;
                
                state.stats.resolved += 1;
                state.stats.pending -= 1;
                if (strategy === 'auto') {
                    state.stats.autoResolved += 1;
                }
                
                state.conflictHistory.unshift({
                    conflictId,
                    resolution,
                    strategy,
                    timestamp: new Date().toISOString()
                });
            }
        },
        setResolutionStrategy: (state, action) => {
            state.resolutionStrategy = action.payload;
        },
        toggleAutoResolve: (state) => {
            state.autoResolveEnabled = !state.autoResolveEnabled;
        },
        setMergeStrategy: (state, action) => {
            state.mergeStrategy = action.payload;
        },
        clearResolvedConflicts: (state) => {
            state.resolvedConflicts = [];
        },
        clearConflictHistory: (state) => {
            state.conflictHistory = [];
        },
        resetConflicts: (state) => {
            return {
                ...initialState,
                resolutionStrategy: state.resolutionStrategy,
                autoResolveEnabled: state.autoResolveEnabled,
                mergeStrategy: state.mergeStrategy
            };
        }
    }
});

export const {
    addConflict,
    resolveConflict,
    setResolutionStrategy,
    toggleAutoResolve,
    setMergeStrategy,
    clearResolvedConflicts,
    clearConflictHistory,
    resetConflicts
} = conflictsSlice.actions;

// Selectors
export const selectActiveConflicts = (state) => state.conflicts.activeConflicts;
export const selectResolvedConflicts = (state) => state.conflicts.resolvedConflicts;
export const selectResolutionStrategy = (state) => state.conflicts.resolutionStrategy;
export const selectAutoResolveEnabled = (state) => state.conflicts.autoResolveEnabled;
export const selectMergeStrategy = (state) => state.conflicts.mergeStrategy;
export const selectConflictHistory = (state) => state.conflicts.conflictHistory;
export const selectLastResolved = (state) => state.conflicts.lastResolved;
export const selectConflictStats = (state) => state.conflicts.stats;

export default conflictsSlice.reducer; 