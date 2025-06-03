/**
 * Log manager for client-side logging.
 * Handles log rotation, filtering, and persistence.
 */

const fs = require('fs');
const path = require('path');
const { app } = require('electron');
const winston = require('winston');
require('winston-daily-rotate-file');

class LogManager {
    constructor() {
        this.logDir = path.join(app.getPath('userData'), 'logs');
        this.initializeLogger();
    }

    /**
     * Initialize the logger with rotation and formatting
     */
    initializeLogger() {
        // Create log directory if it doesn't exist
        if (!fs.existsSync(this.logDir)) {
            fs.mkdirSync(this.logDir, { recursive: true });
        }

        // Configure log rotation
        const rotateTransport = new winston.transports.DailyRotateFile({
            dirname: this.logDir,
            filename: 'app-%DATE%.log',
            datePattern: 'YYYY-MM-DD',
            maxSize: '20m',
            maxFiles: '14d',
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.json()
            )
        });

        // Configure console transport for development
        const consoleTransport = new winston.transports.Console({
            format: winston.format.combine(
                winston.format.colorize(),
                winston.format.simple()
            )
        });

        // Create logger instance
        this.logger = winston.createLogger({
            level: process.env.NODE_ENV === 'development' ? 'debug' : 'info',
            transports: [rotateTransport, consoleTransport],
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.errors({ stack: true }),
                winston.format.json()
            )
        });

        // Handle uncaught exceptions and rejections
        this.logger.exceptions.handle(
            new winston.transports.File({
                filename: path.join(this.logDir, 'exceptions.log'),
                maxsize: 5242880, // 5MB
                maxFiles: 5
            })
        );

        this.logger.rejections.handle(
            new winston.transports.File({
                filename: path.join(this.logDir, 'rejections.log'),
                maxsize: 5242880, // 5MB
                maxFiles: 5
            })
        );
    }

    /**
     * Log a message with metadata
     * @param {string} category - Log category
     * @param {string} message - Log message
     * @param {Object} [metadata] - Additional metadata
     */
    log(category, message, metadata = {}) {
        this.logger.info(message, {
            category,
            ...metadata,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Log an error with stack trace
     * @param {string} category - Log category
     * @param {string} message - Error message
     * @param {Error} error - Error object
     * @param {Object} [metadata] - Additional metadata
     */
    error(category, message, error, metadata = {}) {
        this.logger.error(message, {
            category,
            error: {
                message: error.message,
                stack: error.stack,
                code: error.code
            },
            ...metadata,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Log a warning message
     * @param {string} category - Log category
     * @param {string} message - Warning message
     * @param {Object} [metadata] - Additional metadata
     */
    warn(category, message, metadata = {}) {
        this.logger.warn(message, {
            category,
            ...metadata,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Log a debug message
     * @param {string} category - Log category
     * @param {string} message - Debug message
     * @param {Object} [metadata] - Additional metadata
     */
    debug(category, message, metadata = {}) {
        this.logger.debug(message, {
            category,
            ...metadata,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Get recent logs with optional filtering
     * @param {Object} options - Query options
     * @returns {Promise<Array>} - Array of log entries
     */
    async getLogs(options = {}) {
        try {
            const {
                category,
                level,
                startDate,
                endDate,
                limit = 100
            } = options;

            // Get log files
            const logFiles = await this.getLogFiles();
            let logs = [];

            // Read and parse log files
            for (const file of logFiles) {
                const fileLogs = await this.readLogFile(file);
                logs = logs.concat(fileLogs);
            }

            // Apply filters
            logs = logs.filter(log => {
                if (category && log.category !== category) return false;
                if (level && log.level !== level) return false;
                if (startDate && new Date(log.timestamp) < new Date(startDate)) return false;
                if (endDate && new Date(log.timestamp) > new Date(endDate)) return false;
                return true;
            });

            // Sort by timestamp and limit results
            logs.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
            return logs.slice(0, limit);
        } catch (error) {
            this.error('log-manager', 'Error getting logs', error);
            return [];
        }
    }

    /**
     * Get list of log files
     * @returns {Promise<Array>} - Array of log file paths
     */
    async getLogFiles() {
        try {
            const files = await fs.promises.readdir(this.logDir);
            return files
                .filter(file => file.endsWith('.log'))
                .map(file => path.join(this.logDir, file));
        } catch (error) {
            this.error('log-manager', 'Error getting log files', error);
            return [];
        }
    }

    /**
     * Read and parse a log file
     * @param {string} filePath - Path to log file
     * @returns {Promise<Array>} - Array of log entries
     */
    async readLogFile(filePath) {
        try {
            const content = await fs.promises.readFile(filePath, 'utf8');
            return content
                .split('\n')
                .filter(line => line.trim())
                .map(line => {
                    try {
                        return JSON.parse(line);
                    } catch (error) {
                        return null;
                    }
                })
                .filter(log => log !== null);
        } catch (error) {
            this.error('log-manager', `Error reading log file: ${filePath}`, error);
            return [];
        }
    }

    /**
     * Clean up old log files
     * @param {number} maxAge - Maximum age of logs in days
     */
    async cleanupLogs(maxAge = 14) {
        try {
            const files = await this.getLogFiles();
            const now = Date.now();

            for (const file of files) {
                const stats = await fs.promises.stat(file);
                const age = (now - stats.mtime.getTime()) / (1000 * 60 * 60 * 24);

                if (age > maxAge) {
                    await fs.promises.unlink(file);
                    this.log('log-manager', `Deleted old log file: ${file}`);
                }
            }
        } catch (error) {
            this.error('log-manager', 'Error cleaning up logs', error);
        }
    }

    /**
     * Clean up resources
     */
    cleanup() {
        if (this.logger) {
            this.logger.end();
        }
    }
}

module.exports = new LogManager(); 