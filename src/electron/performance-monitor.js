/**
 * Performance monitor for tracking client performance metrics.
 * Monitors CPU, memory, and renderer process performance.
 */

const { app, BrowserWindow } = require('electron');
const os = require('os');
const logManager = require('./log-manager');

class PerformanceMonitor {
    constructor() {
        this.metrics = new Map();
        this.windows = new Map();
        this.interval = 5000; // 5 seconds
        this.monitorTimer = null;
        this.initialize();
    }

    /**
     * Initialize performance monitoring
     */
    initialize() {
        // Start monitoring
        this.startMonitoring();

        // Track window creation
        app.on('browser-window-created', (event, window) => {
            this.trackWindow(window);
        });

        // Track window destruction
        app.on('browser-window-blur', (event, window) => {
            this.untrackWindow(window);
        });
    }

    /**
     * Start performance monitoring
     */
    startMonitoring() {
        if (this.monitorTimer) {
            clearInterval(this.monitorTimer);
        }

        this.monitorTimer = setInterval(() => {
            this.collectMetrics();
        }, this.interval);
    }

    /**
     * Stop performance monitoring
     */
    stopMonitoring() {
        if (this.monitorTimer) {
            clearInterval(this.monitorTimer);
            this.monitorTimer = null;
        }
    }

    /**
     * Track a window for performance monitoring
     * @param {BrowserWindow} window - Browser window to track
     */
    trackWindow(window) {
        const id = window.id;
        this.windows.set(id, {
            window,
            metrics: {
                fps: 0,
                memory: 0,
                cpu: 0,
                lastUpdate: Date.now()
            }
        });

        // Set up window event listeners
        window.webContents.on('did-start-loading', () => {
            this.updateWindowMetric(id, 'loading', true);
        });

        window.webContents.on('did-stop-loading', () => {
            this.updateWindowMetric(id, 'loading', false);
        });

        window.webContents.on('crashed', () => {
            this.updateWindowMetric(id, 'crashed', true);
        });

        window.webContents.on('render-process-gone', (event, details) => {
            this.updateWindowMetric(id, 'rendererGone', {
                reason: details.reason,
                exitCode: details.exitCode
            });
        });
    }

    /**
     * Stop tracking a window
     * @param {BrowserWindow} window - Browser window to untrack
     */
    untrackWindow(window) {
        this.windows.delete(window.id);
    }

    /**
     * Update a window's metric
     * @param {number} windowId - Window ID
     * @param {string} metric - Metric name
     * @param {*} value - Metric value
     */
    updateWindowMetric(windowId, metric, value) {
        const windowData = this.windows.get(windowId);
        if (windowData) {
            windowData.metrics[metric] = value;
            windowData.metrics.lastUpdate = Date.now();
        }
    }

    /**
     * Collect performance metrics
     */
    collectMetrics() {
        try {
            // Collect system metrics
            const systemMetrics = {
                cpu: this.getCpuUsage(),
                memory: this.getMemoryUsage(),
                uptime: os.uptime(),
                timestamp: Date.now()
            };

            // Collect window metrics
            for (const [id, windowData] of this.windows) {
                const window = windowData.window;
                if (window.isDestroyed()) {
                    this.windows.delete(id);
                    continue;
                }

                // Get window metrics
                const metrics = {
                    ...windowData.metrics,
                    memory: window.getProcessMemoryInfo(),
                    cpu: window.getCPUUsage(),
                    fps: this.getWindowFPS(window)
                };

                // Update window metrics
                this.updateWindowMetric(id, 'metrics', metrics);
            }

            // Store metrics
            this.metrics.set(systemMetrics.timestamp, {
                system: systemMetrics,
                windows: Array.from(this.windows.entries()).map(([id, data]) => ({
                    id,
                    metrics: data.metrics
                }))
            });

            // Clean up old metrics
            this.cleanupMetrics();

            // Log metrics
            this.logMetrics(systemMetrics);
        } catch (error) {
            logManager.error('performance', 'Error collecting metrics', error);
        }
    }

    /**
     * Get CPU usage
     * @returns {Object} - CPU usage metrics
     */
    getCpuUsage() {
        const cpus = os.cpus();
        const totalIdle = cpus.reduce((acc, cpu) => acc + cpu.times.idle, 0);
        const totalTick = cpus.reduce((acc, cpu) => {
            return acc + Object.values(cpu.times).reduce((sum, time) => sum + time, 0);
        }, 0);

        return {
            idle: totalIdle,
            total: totalTick,
            usage: 100 - (totalIdle / totalTick * 100)
        };
    }

    /**
     * Get memory usage
     * @returns {Object} - Memory usage metrics
     */
    getMemoryUsage() {
        const total = os.totalmem();
        const free = os.freemem();
        const used = total - free;

        return {
            total,
            free,
            used,
            usage: (used / total) * 100
        };
    }

    /**
     * Get window FPS
     * @param {BrowserWindow} window - Browser window
     * @returns {number} - FPS value
     */
    getWindowFPS(window) {
        try {
            return window.webContents.getFrameRate();
        } catch (error) {
            return 0;
        }
    }

    /**
     * Clean up old metrics
     */
    cleanupMetrics() {
        const now = Date.now();
        const maxAge = 3600000; // 1 hour

        for (const [timestamp] of this.metrics) {
            if (now - timestamp > maxAge) {
                this.metrics.delete(timestamp);
            }
        }
    }

    /**
     * Log performance metrics
     * @param {Object} metrics - System metrics
     */
    logMetrics(metrics) {
        logManager.debug('performance', 'Performance metrics', {
            cpu: metrics.cpu.usage.toFixed(2) + '%',
            memory: metrics.memory.usage.toFixed(2) + '%',
            uptime: Math.floor(metrics.uptime / 60) + ' minutes',
            windows: this.windows.size
        });
    }

    /**
     * Get performance report
     * @returns {Object} - Performance report
     */
    getReport() {
        const now = Date.now();
        const report = {
            timestamp: now,
            system: {
                cpu: this.getCpuUsage(),
                memory: this.getMemoryUsage(),
                uptime: os.uptime()
            },
            windows: Array.from(this.windows.entries()).map(([id, data]) => ({
                id,
                metrics: data.metrics
            })),
            history: Array.from(this.metrics.entries())
                .filter(([timestamp]) => now - timestamp <= 3600000) // Last hour
                .map(([timestamp, data]) => ({
                    timestamp,
                    ...data
                }))
        };

        return report;
    }

    /**
     * Clean up resources
     */
    cleanup() {
        this.stopMonitoring();
        this.metrics.clear();
        this.windows.clear();
    }
}

module.exports = new PerformanceMonitor(); 