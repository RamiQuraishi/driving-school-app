/**
 * IPC handlers for the Electron application.
 * This module manages IPC communication between main and renderer processes.
 */

const { ipcMain } = require('electron');
const rateLimiter = require('./rate_limiter');
const security = require('./security');
const apiBridge = require('./api-bridge');
const logManager = require('../log-manager');

class IpcHandlers {
    constructor() {
        this.handlers = new Map();
        this.initializeHandlers();
    }

    /**
     * Initialize all IPC handlers
     */
    initializeHandlers() {
        // Window control handlers
        this.registerHandler('window:minimize', this.handleWindowMinimize);
        this.registerHandler('window:maximize', this.handleWindowMaximize);
        this.registerHandler('window:close', this.handleWindowClose);
        this.registerHandler('window:reload', this.handleWindowReload);

        // Application handlers
        this.registerHandler('app:get-version', this.handleGetVersion);
        this.registerHandler('app:check-updates', this.handleCheckUpdates);
        this.registerHandler('app:restart', this.handleRestart);

        // API bridge handlers
        this.registerHandler('api:request', this.handleApiRequest);
        this.registerHandler('api:stream', this.handleApiStream);

        // System handlers
        this.registerHandler('system:get-info', this.handleGetSystemInfo);
        this.registerHandler('system:get-metrics', this.handleGetMetrics);
    }

    /**
     * Register an IPC handler with rate limiting and security checks
     * @param {string} channel - IPC channel name
     * @param {Function} handler - Handler function
     */
    registerHandler(channel, handler) {
        const wrappedHandler = async (event, ...args) => {
            try {
                // Rate limiting check
                if (!rateLimiter.checkLimit(channel)) {
                    throw new Error('Rate limit exceeded');
                }

                // Security validation
                if (!security.validateRequest(channel, args)) {
                    throw new Error('Invalid request');
                }

                // Log the request
                logManager.log('ipc', `Handling IPC request: ${channel}`, { args });

                // Execute handler
                const result = await handler(event, ...args);
                return { success: true, data: result };
            } catch (error) {
                // Log the error
                logManager.error('ipc', `IPC handler error: ${channel}`, error);

                // Return error response
                return {
                    success: false,
                    error: {
                        message: error.message,
                        code: error.code || 'UNKNOWN_ERROR'
                    }
                };
            }
        };

        this.handlers.set(channel, wrappedHandler);
        ipcMain.handle(channel, wrappedHandler);
    }

    /**
     * Window control handlers
     */
    handleWindowMinimize = (event) => {
        const window = event.sender.getOwnerBrowserWindow();
        window.minimize();
    };

    handleWindowMaximize = (event) => {
        const window = event.sender.getOwnerBrowserWindow();
        if (window.isMaximized()) {
            window.unmaximize();
        } else {
            window.maximize();
        }
    };

    handleWindowClose = (event) => {
        const window = event.sender.getOwnerBrowserWindow();
        window.close();
    };

    handleWindowReload = (event) => {
        const window = event.sender.getOwnerBrowserWindow();
        window.reload();
    };

    /**
     * Application handlers
     */
    handleGetVersion = () => {
        return require('../../package.json').version;
    };

    handleCheckUpdates = async () => {
        const updater = require('../updater');
        return await updater.checkForUpdates();
    };

    handleRestart = () => {
        require('electron').app.relaunch();
        require('electron').app.exit(0);
    };

    /**
     * API bridge handlers
     */
    handleApiRequest = async (event, request) => {
        return await apiBridge.handleRequest(request);
    };

    handleApiStream = async (event, request) => {
        return await apiBridge.handleStream(request);
    };

    /**
     * System handlers
     */
    handleGetSystemInfo = () => {
        return {
            platform: process.platform,
            arch: process.arch,
            version: process.version,
            memory: process.getSystemMemoryInfo(),
            cpu: process.getCPUUsage()
        };
    };

    handleGetMetrics = () => {
        return {
            memory: process.getProcessMemoryInfo(),
            cpu: process.getCPUUsage(),
            uptime: process.uptime()
        };
    };

    /**
     * Remove all registered handlers
     */
    cleanup() {
        for (const [channel, handler] of this.handlers) {
            ipcMain.removeHandler(channel);
        }
        this.handlers.clear();
    }
}

module.exports = new IpcHandlers(); 