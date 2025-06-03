/**
 * Error Recovery middleware with circuit breaker pattern.
 * Handles failures gracefully and prevents cascading failures.
 */

import { createAction } from '@reduxjs/toolkit';
import { isRejectedWithValue } from '@reduxjs/toolkit/query';

// Action types
const CIRCUIT_OPEN = 'error/circuitOpen';
const CIRCUIT_CLOSED = 'error/circuitClosed';
const CIRCUIT_HALF_OPEN = 'error/circuitHalfOpen';
const ERROR_RECOVERED = 'error/recovered';
const ERROR_THRESHOLD_REACHED = 'error/thresholdReached';

// Action creators
export const circuitOpen = createAction(CIRCUIT_OPEN);
export const circuitClosed = createAction(CIRCUIT_CLOSED);
export const circuitHalfOpen = createAction(CIRCUIT_HALF_OPEN);
export const errorRecovered = createAction(ERROR_RECOVERED);
export const errorThresholdReached = createAction(ERROR_THRESHOLD_REACHED);

// Circuit breaker states
const CIRCUIT_STATES = {
    CLOSED: 'closed',
    OPEN: 'open',
    HALF_OPEN: 'half-open'
};

// Error tracking
const errorCounts = new Map();
const lastErrorTimes = new Map();
const circuitStates = new Map();

const createErrorRecoveryMiddleware = (config = {}) => {
    const {
        errorThreshold = 5,
        errorWindow = 60000, // 1 minute
        resetTimeout = 30000, // 30 seconds
        onCircuitOpen = console.warn,
        onCircuitClosed = console.info,
        onErrorThreshold = console.error,
        onRecovery = console.info
    } = config;

    const resetErrorCount = (key) => {
        errorCounts.set(key, 0);
        lastErrorTimes.set(key, Date.now());
    };

    const incrementErrorCount = (key) => {
        const count = (errorCounts.get(key) || 0) + 1;
        errorCounts.set(key, count);
        lastErrorTimes.set(key, Date.now());
        return count;
    };

    const isErrorWindowExpired = (key) => {
        const lastErrorTime = lastErrorTimes.get(key);
        return lastErrorTime && Date.now() - lastErrorTime > errorWindow;
    };

    const getCircuitState = (key) => {
        return circuitStates.get(key) || CIRCUIT_STATES.CLOSED;
    };

    const setCircuitState = (key, state) => {
        circuitStates.set(key, state);
        return state;
    };

    const handleCircuitState = (key, state, dispatch) => {
        switch (state) {
            case CIRCUIT_STATES.OPEN:
                dispatch(circuitOpen({ key }));
                onCircuitOpen(`Circuit opened for ${key}`);
                setTimeout(() => {
                    setCircuitState(key, CIRCUIT_STATES.HALF_OPEN);
                    dispatch(circuitHalfOpen({ key }));
                }, resetTimeout);
                break;
            case CIRCUIT_STATES.CLOSED:
                dispatch(circuitClosed({ key }));
                onCircuitClosed(`Circuit closed for ${key}`);
                break;
            case CIRCUIT_STATES.HALF_OPEN:
                dispatch(circuitHalfOpen({ key }));
                break;
        }
    };

    return ({ dispatch }) => {
        return (next) => (action) => {
            const result = next(action);

            if (isRejectedWithValue(result)) {
                const { error, meta } = result;
                const key = meta?.arg?.endpoint || 'unknown';

                // Check if error window has expired
                if (isErrorWindowExpired(key)) {
                    resetErrorCount(key);
                }

                // Increment error count
                const errorCount = incrementErrorCount(key);

                // Check if error threshold is reached
                if (errorCount >= errorThreshold) {
                    dispatch(errorThresholdReached({ key, count: errorCount }));
                    onErrorThreshold(`Error threshold reached for ${key}: ${errorCount} errors`);

                    // Open circuit if not already open
                    if (getCircuitState(key) !== CIRCUIT_STATES.OPEN) {
                        handleCircuitState(key, setCircuitState(key, CIRCUIT_STATES.OPEN), dispatch);
                    }
                }
            } else if (result.type?.endsWith('/fulfilled')) {
                const key = result.meta?.arg?.endpoint || 'unknown';
                const state = getCircuitState(key);

                // If circuit is half-open and request succeeds, close it
                if (state === CIRCUIT_STATES.HALF_OPEN) {
                    handleCircuitState(key, setCircuitState(key, CIRCUIT_STATES.CLOSED), dispatch);
                    dispatch(errorRecovered({ key }));
                    onRecovery(`Error recovered for ${key}`);
                    resetErrorCount(key);
                }
            }

            return result;
        };
    };
};

export {
    CIRCUIT_STATES,
    createErrorRecoveryMiddleware as default
}; 