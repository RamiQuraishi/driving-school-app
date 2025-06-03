/**
 * Performance reducer for tracking application performance metrics.
 * Handles CPU, memory, frame rate, and network performance monitoring.
 */

import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    metrics: {
        cpu: {
            usage: 0,
            temperature: 0,
            cores: []
        },
        memory: {
            total: 0,
            used: 0,
            free: 0,
            percentage: 0
        },
        frameRate: {
            current: 0,
            average: 0,
            min: Infinity,
            max: 0,
            samples: []
        },
        network: {
            latency: 0,
            throughput: 0,
            errors: 0
        }
    },
    thresholds: {
        cpu: 80, // percentage
        memory: 85, // percentage
        frameRate: 30, // fps
        network: 1000 // ms
    },
    warnings: {
        cpu: false,
        memory: false,
        frameRate: false,
        network: false
    },
    history: [],
    isMonitoring: false,
    lastUpdate: null
};

const performanceSlice = createSlice({
    name: 'performance',
    initialState,
    reducers: {
        updateMetrics: (state, action) => {
            const { timestamp = Date.now(), ...metrics } = action.payload;
            
            // Update metrics
            state.metrics = {
                ...state.metrics,
                ...metrics
            };
            
            // Update frame rate samples
            if (metrics.frameRate?.current) {
                const samples = state.metrics.frameRate.samples;
                samples.push(metrics.frameRate.current);
                if (samples.length > 60) samples.shift(); // Keep last 60 samples
                
                state.metrics.frameRate.average = samples.reduce((a, b) => a + b, 0) / samples.length;
                state.metrics.frameRate.min = Math.min(...samples);
                state.metrics.frameRate.max = Math.max(...samples);
            }
            
            // Check thresholds and update warnings
            state.warnings = {
                cpu: state.metrics.cpu.usage > state.thresholds.cpu,
                memory: state.metrics.memory.percentage > state.thresholds.memory,
                frameRate: state.metrics.frameRate.current < state.thresholds.frameRate,
                network: state.metrics.network.latency > state.thresholds.network
            };
            
            // Add to history
            state.history.push({
                timestamp,
                metrics: state.metrics,
                warnings: state.warnings
            });
            
            // Keep last 1000 history entries
            if (state.history.length > 1000) {
                state.history.shift();
            }
            
            state.lastUpdate = timestamp;
        },
        setThresholds: (state, action) => {
            state.thresholds = { ...state.thresholds, ...action.payload };
        },
        startMonitoring: (state) => {
            state.isMonitoring = true;
        },
        stopMonitoring: (state) => {
            state.isMonitoring = false;
        },
        clearHistory: (state) => {
            state.history = [];
        },
        resetMetrics: (state) => {
            return {
                ...initialState,
                thresholds: state.thresholds,
                isMonitoring: state.isMonitoring
            };
        }
    }
});

export const {
    updateMetrics,
    setThresholds,
    startMonitoring,
    stopMonitoring,
    clearHistory,
    resetMetrics
} = performanceSlice.actions;

// Selectors
export const selectMetrics = (state) => state.performance.metrics;
export const selectThresholds = (state) => state.performance.thresholds;
export const selectWarnings = (state) => state.performance.warnings;
export const selectHistory = (state) => state.performance.history;
export const selectIsMonitoring = (state) => state.performance.isMonitoring;
export const selectLastUpdate = (state) => state.performance.lastUpdate;

export default performanceSlice.reducer; 