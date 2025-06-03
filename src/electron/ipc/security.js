/**
 * Security module for IPC communication.
 * Handles request validation, sanitization, and security checks.
 */

const { validate } = require('jsonschema');
const logManager = require('../log-manager');

class IpcSecurity {
    constructor() {
        this.schemas = new Map();
        this.initializeSchemas();
    }

    /**
     * Initialize validation schemas for different IPC channels
     */
    initializeSchemas() {
        // Window control schemas
        this.schemas.set('window:minimize', { type: 'object', properties: {} });
        this.schemas.set('window:maximize', { type: 'object', properties: {} });
        this.schemas.set('window:close', { type: 'object', properties: {} });
        this.schemas.set('window:reload', { type: 'object', properties: {} });

        // API request schema
        this.schemas.set('api:request', {
            type: 'object',
            required: ['method', 'path'],
            properties: {
                method: { type: 'string', enum: ['GET', 'POST', 'PUT', 'DELETE'] },
                path: { type: 'string', pattern: '^/[a-zA-Z0-9/-]*$' },
                body: { type: 'object' },
                headers: { type: 'object' }
            }
        });

        // API stream schema
        this.schemas.set('api:stream', {
            type: 'object',
            required: ['path'],
            properties: {
                path: { type: 'string', pattern: '^/[a-zA-Z0-9/-]*$' },
                options: { type: 'object' }
            }
        });
    }

    /**
     * Validate an IPC request
     * @param {string} channel - IPC channel name
     * @param {Array} args - Request arguments
     * @returns {boolean} - Whether the request is valid
     */
    validateRequest(channel, args) {
        try {
            // Get schema for channel
            const schema = this.schemas.get(channel);
            if (!schema) {
                logManager.warn('security', `No schema found for channel: ${channel}`);
                return false;
            }

            // Validate request data
            const requestData = args[0] || {};
            const validation = validate(requestData, schema);
            
            if (!validation.valid) {
                logManager.warn('security', `Invalid request data for channel: ${channel}`, {
                    errors: validation.errors
                });
                return false;
            }

            // Additional security checks
            if (!this.performSecurityChecks(channel, requestData)) {
                return false;
            }

            return true;
        } catch (error) {
            logManager.error('security', `Error validating request for channel: ${channel}`, error);
            return false;
        }
    }

    /**
     * Perform additional security checks
     * @param {string} channel - IPC channel name
     * @param {Object} data - Request data
     * @returns {boolean} - Whether the request passes security checks
     */
    performSecurityChecks(channel, data) {
        // Check for potentially dangerous operations
        if (this.isDangerousOperation(channel, data)) {
            logManager.warn('security', `Dangerous operation detected: ${channel}`);
            return false;
        }

        // Check for malicious patterns
        if (this.containsMaliciousPatterns(data)) {
            logManager.warn('security', `Malicious patterns detected in request: ${channel}`);
            return false;
        }

        // Check for excessive data size
        if (this.isExcessiveDataSize(data)) {
            logManager.warn('security', `Excessive data size detected in request: ${channel}`);
            return false;
        }

        return true;
    }

    /**
     * Check if an operation is potentially dangerous
     * @param {string} channel - IPC channel name
     * @param {Object} data - Request data
     * @returns {boolean} - Whether the operation is dangerous
     */
    isDangerousOperation(channel, data) {
        const dangerousChannels = [
            'system:execute',
            'system:shell',
            'system:spawn'
        ];

        if (dangerousChannels.includes(channel)) {
            return true;
        }

        // Check for dangerous patterns in data
        const dangerousPatterns = [
            /^rm\s+-rf/i,
            /^mkfs/i,
            /^format/i,
            /^dd\s+if=/i
        ];

        return dangerousPatterns.some(pattern => 
            JSON.stringify(data).match(pattern)
        );
    }

    /**
     * Check for malicious patterns in data
     * @param {Object} data - Request data
     * @returns {boolean} - Whether malicious patterns are found
     */
    containsMaliciousPatterns(data) {
        const maliciousPatterns = [
            /<script>/i,
            /javascript:/i,
            /data:/i,
            /vbscript:/i,
            /on\w+=/i,
            /eval\(/i,
            /setTimeout\(/i,
            /setInterval\(/i
        ];

        return maliciousPatterns.some(pattern => 
            JSON.stringify(data).match(pattern)
        );
    }

    /**
     * Check if data size is excessive
     * @param {Object} data - Request data
     * @returns {boolean} - Whether data size is excessive
     */
    isExcessiveDataSize(data) {
        const MAX_DATA_SIZE = 10 * 1024 * 1024; // 10MB
        const dataSize = Buffer.from(JSON.stringify(data)).length;
        return dataSize > MAX_DATA_SIZE;
    }

    /**
     * Sanitize request data
     * @param {Object} data - Request data
     * @returns {Object} - Sanitized data
     */
    sanitizeData(data) {
        if (typeof data !== 'object' || data === null) {
            return data;
        }

        const sanitized = {};

        for (const [key, value] of Object.entries(data)) {
            if (typeof value === 'string') {
                // Sanitize strings
                sanitized[key] = this.sanitizeString(value);
            } else if (typeof value === 'object' && value !== null) {
                // Recursively sanitize objects
                sanitized[key] = this.sanitizeData(value);
            } else {
                sanitized[key] = value;
            }
        }

        return sanitized;
    }

    /**
     * Sanitize a string
     * @param {string} str - String to sanitize
     * @returns {string} - Sanitized string
     */
    sanitizeString(str) {
        return str
            .replace(/[<>]/g, '') // Remove angle brackets
            .replace(/javascript:/gi, '') // Remove javascript: protocol
            .replace(/data:/gi, '') // Remove data: protocol
            .replace(/on\w+=/gi, '') // Remove event handlers
            .trim();
    }
}

module.exports = new IpcSecurity(); 