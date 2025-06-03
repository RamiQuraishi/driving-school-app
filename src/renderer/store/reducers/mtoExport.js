/**
 * MTO Export reducer for managing MTO data export state.
 * Handles export progress, status, and history.
 */

import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    isExporting: false,
    progress: 0,
    status: 'idle', // idle, preparing, exporting, completed, failed
    currentExport: null,
    history: [],
    lastExport: null,
    error: null,
    exportConfig: {
        format: 'csv',
        includeInactive: false,
        dateRange: null,
        filters: {}
    }
};

const mtoExportSlice = createSlice({
    name: 'mtoExport',
    initialState,
    reducers: {
        startExport: (state, action) => {
            state.isExporting = true;
            state.progress = 0;
            state.status = 'preparing';
            state.error = null;
            state.currentExport = {
                id: Date.now(),
                startTime: new Date().toISOString(),
                config: action.payload || state.exportConfig
            };
        },
        updateProgress: (state, action) => {
            state.progress = action.payload;
            state.status = 'exporting';
        },
        completeExport: (state, action) => {
            const { filePath, recordCount } = action.payload;
            state.isExporting = false;
            state.progress = 100;
            state.status = 'completed';
            state.lastExport = {
                ...state.currentExport,
                endTime: new Date().toISOString(),
                filePath,
                recordCount
            };
            state.history.unshift(state.lastExport);
            state.currentExport = null;
        },
        failExport: (state, action) => {
            state.isExporting = false;
            state.status = 'failed';
            state.error = action.payload;
            state.currentExport = null;
        },
        updateExportConfig: (state, action) => {
            state.exportConfig = { ...state.exportConfig, ...action.payload };
        },
        clearExportHistory: (state) => {
            state.history = [];
        },
        resetExport: (state) => {
            return { ...initialState, history: state.history };
        }
    }
});

export const {
    startExport,
    updateProgress,
    completeExport,
    failExport,
    updateExportConfig,
    clearExportHistory,
    resetExport
} = mtoExportSlice.actions;

// Selectors
export const selectIsExporting = (state) => state.mtoExport.isExporting;
export const selectExportProgress = (state) => state.mtoExport.progress;
export const selectExportStatus = (state) => state.mtoExport.status;
export const selectCurrentExport = (state) => state.mtoExport.currentExport;
export const selectExportHistory = (state) => state.mtoExport.history;
export const selectLastExport = (state) => state.mtoExport.lastExport;
export const selectExportError = (state) => state.mtoExport.error;
export const selectExportConfig = (state) => state.mtoExport.exportConfig;

export default mtoExportSlice.reducer; 