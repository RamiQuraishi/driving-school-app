/**
 * Telemetry module for anonymous usage tracking.
 * Collects and sends anonymous usage data to help improve the application.
 */

const { app } = require('electron');
const axios = require('axios');
const crypto = require('crypto');
const logManager = require('./log-manager');

class Telemetry {
    constructor() {
        this.enabled = this.isTelemetryEnabled();
        this.anonymousId = this.getAnonymousId();
        this.endpoint = process.env.TELEMETRY_ENDPOINT || 'https://telemetry.example.com';
        this.queue = [];
        this.batchSize = 50;
        this.flushInterval = 60000; // 1 minute
        this.initialize();
    }

    /**
     * Initialize telemetry
     */
    initialize() {
        if (!this.enabled) {
            return;
        }

        // Start periodic flush
        this.flushTimer = setInterval(() => this.flush(), this.flushInterval);

        // Track app lifecycle events
        this.trackAppLifecycle();

        // Track system events
        this.trackSystemEvents();
    }

    /**
     * Check if telemetry is enabled
     * @returns {boolean} - Whether telemetry is enabled
     */
    isTelemetryEnabled() {
        try {
            return app.getStore().get('telemetry.enabled', true);
        } catch (error) {
            return true; // Default to enabled
        }
    }

    /**
     * Get or generate anonymous ID
     * @returns {string} - Anonymous ID
     */
    getAnonymousId() {
        try {
            let id = app.getStore().get('telemetry.anonymousId');
            if (!id) {
                id = crypto.randomBytes(16).toString('hex');
                app.getStore().set('telemetry.anonymousId', id);
            }
            return id;
        } catch (error) {
            return crypto.randomBytes(16).toString('hex');
        }
    }

    /**
     * Track app lifecycle events
     */
    trackAppLifecycle() {
        app.on('ready', () => this.track('app_ready'));
        app.on('window-all-closed', () => this.track('app_closed'));
        app.on('activate', () => this.track('app_activated'));
        app.on('before-quit', () => this.track('app_quitting'));
    }

    /**
     * Track system events
     */
    trackSystemEvents() {
        app.on('gpu-process-crashed', () => this.track('gpu_crashed'));
        app.on('render-process-gone', (event, details) => {
            this.track('renderer_crashed', { reason: details.reason });
        });
        app.on('child-process-gone', (event, details) => {
            this.track('child_process_gone', { type: details.type });
        });
    }

    /**
     * Track an event
     * @param {string} event - Event name
     * @param {Object} [properties] - Event properties
     */
    track(event, properties = {}) {
        if (!this.enabled) {
            return;
        }

        try {
            const eventData = {
                event,
                properties: this.sanitizeProperties(properties),
                timestamp: new Date().toISOString(),
                anonymousId: this.anonymousId,
                appVersion: app.getVersion(),
                platform: process.platform,
                arch: process.arch
            };

            this.queue.push(eventData);

            // Flush if queue is full
            if (this.queue.length >= this.batchSize) {
                this.flush();
            }
        } catch (error) {
            logManager.error('telemetry', 'Error tracking event', error);
        }
    }

    /**
     * Sanitize event properties
     * @param {Object} properties - Event properties
     * @returns {Object} - Sanitized properties
     */
    sanitizeProperties(properties) {
        const sanitized = { ...properties };

        // Remove sensitive data
        delete sanitized.password;
        delete sanitized.token;
        delete sanitized.key;
        delete sanitized.secret;

        // Remove PII
        delete sanitized.email;
        delete sanitized.phone;
        delete sanitized.address;
        delete sanitized.name;

        return sanitized;
    }

    /**
     * Flush queued events
     */
    async flush() {
        if (this.queue.length === 0) {
            return;
        }

        try {
            const events = [...this.queue];
            this.queue = [];

            await axios.post(`${this.endpoint}/events`, {
                events,
                batchId: crypto.randomBytes(16).toString('hex'),
                timestamp: new Date().toISOString()
            });

            logManager.debug('telemetry', `Flushed ${events.length} events`);
        } catch (error) {
            logManager.error('telemetry', 'Error flushing events', error);
            
            // Put events back in queue
            this.queue = [...this.queue, ...events];
        }
    }

    /**
     * Enable telemetry
     */
    enable() {
        this.enabled = true;
        app.getStore().set('telemetry.enabled', true);
        this.initialize();
    }

    /**
     * Disable telemetry
     */
    disable() {
        this.enabled = false;
        app.getStore().set('telemetry.enabled', false);
        this.cleanup();
    }

    /**
     * Clean up resources
     */
    cleanup() {
        if (this.flushTimer) {
            clearInterval(this.flushTimer);
        }

        // Flush any remaining events
        if (this.queue.length > 0) {
            this.flush();
        }
    }
}

module.exports = new Telemetry(); 