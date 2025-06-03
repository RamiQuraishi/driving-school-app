/**
 * Rate limiter for IPC calls.
 * Prevents abuse by limiting the number of calls per channel.
 */

const logManager = require('../log-manager');

class RateLimiter {
    constructor() {
        this.limits = new Map();
        this.counters = new Map();
        this.initializeLimits();
    }

    /**
     * Initialize rate limits for different channels
     */
    initializeLimits() {
        // Window control limits
        this.limits.set('window:minimize', { max: 10, window: 1000 }); // 10 calls per second
        this.limits.set('window:maximize', { max: 10, window: 1000 });
        this.limits.set('window:close', { max: 5, window: 1000 });
        this.limits.set('window:reload', { max: 5, window: 1000 });

        // API request limits
        this.limits.set('api:request', { max: 30, window: 1000 }); // 30 calls per second
        this.limits.set('api:stream', { max: 10, window: 1000 }); // 10 connections per second

        // System info limits
        this.limits.set('system:get-info', { max: 5, window: 5000 }); // 5 calls per 5 seconds
        this.limits.set('system:get-metrics', { max: 10, window: 1000 }); // 10 calls per second
    }

    /**
     * Check if a channel is within its rate limit
     * @param {string} channel - IPC channel name
     * @returns {boolean} - Whether the call is allowed
     */
    checkLimit(channel) {
        try {
            // Get rate limit for channel
            const limit = this.limits.get(channel);
            if (!limit) {
                return true; // No limit set for this channel
            }

            // Get or initialize counter for channel
            let counter = this.counters.get(channel);
            if (!counter) {
                counter = {
                    count: 0,
                    resetTime: Date.now() + limit.window
                };
                this.counters.set(channel, counter);
            }

            // Check if counter needs reset
            if (Date.now() > counter.resetTime) {
                counter.count = 0;
                counter.resetTime = Date.now() + limit.window;
            }

            // Check if limit is exceeded
            if (counter.count >= limit.max) {
                logManager.warn('rate-limit', `Rate limit exceeded for channel: ${channel}`, {
                    limit: limit.max,
                    window: limit.window
                });
                return false;
            }

            // Increment counter
            counter.count++;

            return true;
        } catch (error) {
            logManager.error('rate-limit', `Error checking rate limit for channel: ${channel}`, error);
            return false; // Fail closed on error
        }
    }

    /**
     * Get current rate limit status for a channel
     * @param {string} channel - IPC channel name
     * @returns {Object} - Rate limit status
     */
    getStatus(channel) {
        const limit = this.limits.get(channel);
        const counter = this.counters.get(channel);

        if (!limit) {
            return {
                limited: false,
                message: 'No rate limit set'
            };
        }

        if (!counter) {
            return {
                limited: false,
                remaining: limit.max,
                resetTime: Date.now() + limit.window
            };
        }

        const remaining = Math.max(0, limit.max - counter.count);
        const resetTime = counter.resetTime;

        return {
            limited: counter.count >= limit.max,
            remaining,
            resetTime,
            limit: limit.max,
            window: limit.window
        };
    }

    /**
     * Reset rate limit counters
     */
    reset() {
        this.counters.clear();
    }

    /**
     * Clean up resources
     */
    cleanup() {
        this.reset();
        this.limits.clear();
    }
}

module.exports = new RateLimiter(); 