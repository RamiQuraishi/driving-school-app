/**
 * Performance middleware for monitoring application performance.
 * Tracks CPU, memory, frame rate, and network performance.
 */

import { createAction } from '@reduxjs/toolkit';
import { updateMetrics, setThresholds } from '../reducers/performance';

// Action types
const START_MONITORING = 'performance/startMonitoring';
const STOP_MONITORING = 'performance/stopMonitoring';
const UPDATE_METRICS = 'performance/updateMetrics';

// Action creators
export const startMonitoring = createAction(START_MONITORING);
export const stopMonitoring = createAction(STOP_MONITORING);
export const updatePerformanceMetrics = createAction(UPDATE_METRICS);

// Performance monitoring
let monitoringInterval = null;
let frameCount = 0;
let lastFrameTime = performance.now();
let frameRateHistory = [];

const calculateFrameRate = () => {
    const now = performance.now();
    const elapsed = now - lastFrameTime;
    const fps = 1000 / elapsed;
    
    frameRateHistory.push(fps);
    if (frameRateHistory.length > 60) {
        frameRateHistory.shift();
    }
    
    lastFrameTime = now;
    frameCount++;
    
    return {
        current: Math.round(fps),
        average: Math.round(frameRateHistory.reduce((a, b) => a + b, 0) / frameRateHistory.length),
        min: Math.round(Math.min(...frameRateHistory)),
        max: Math.round(Math.max(...frameRateHistory))
    };
};

const getMemoryInfo = () => {
    if (performance.memory) {
        const { totalJSHeapSize, usedJSHeapSize, jsHeapSizeLimit } = performance.memory;
        return {
            total: totalJSHeapSize,
            used: usedJSHeapSize,
            free: totalJSHeapSize - usedJSHeapSize,
            percentage: (usedJSHeapSize / totalJSHeapSize) * 100
        };
    }
    return null;
};

const getNetworkInfo = async () => {
    if (navigator.connection) {
        const connection = navigator.connection;
        return {
            type: connection.effectiveType,
            downlink: connection.downlink,
            rtt: connection.rtt,
            saveData: connection.saveData
        };
    }
    return null;
};

const createPerformanceMiddleware = (config = {}) => {
    const {
        interval = 1000,
        thresholds = {
            cpu: 80,
            memory: 85,
            frameRate: 30,
            network: 1000
        },
        onWarning = console.warn
    } = config;

    return ({ dispatch }) => {
        const monitorPerformance = async () => {
            const frameRate = calculateFrameRate();
            const memory = getMemoryInfo();
            const network = await getNetworkInfo();

            const metrics = {
                frameRate,
                memory,
                network,
                timestamp: Date.now()
            };

            dispatch(updateMetrics(metrics));

            // Check thresholds and trigger warnings
            if (frameRate.current < thresholds.frameRate) {
                onWarning('Low frame rate detected:', frameRate.current);
            }

            if (memory && memory.percentage > thresholds.memory) {
                onWarning('High memory usage detected:', memory.percentage);
            }

            if (network && network.rtt > thresholds.network) {
                onWarning('High network latency detected:', network.rtt);
            }
        };

        return (next) => (action) => {
            const result = next(action);

            if (action.type === START_MONITORING) {
                if (monitoringInterval) {
                    clearInterval(monitoringInterval);
                }
                monitoringInterval = setInterval(monitorPerformance, interval);
                dispatch(setThresholds(thresholds));
            }

            if (action.type === STOP_MONITORING) {
                if (monitoringInterval) {
                    clearInterval(monitoringInterval);
                    monitoringInterval = null;
                }
            }

            return result;
        };
    };
};

export default createPerformanceMiddleware; 