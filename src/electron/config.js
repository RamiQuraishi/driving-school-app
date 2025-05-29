/**
 * Electron configuration for Ontario Driving School Manager.
 * Handles Electron-specific settings and window configuration.
 */

const path = require('path');
const isDev = process.env.NODE_ENV === 'development';

module.exports = {
    // Application settings
    app: {
        name: 'Ontario Driving School Manager',
        version: '1.0.0',
        description: 'Management system for driving schools in Ontario',
        author: 'Your Name',
        license: 'MIT'
    },

    // Window settings
    window: {
        width: 1200,
        height: 800,
        minWidth: 800,
        minHeight: 600,
        title: 'Ontario Driving School Manager',
        icon: path.join(__dirname, '../assets/icons/icon.png'),
        show: false,
        frame: true,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true,
            webSecurity: !isDev
        }
    },

    // Development settings
    development: {
        isDev,
        devTools: isDev,
        hotReload: isDev,
        openDevTools: isDev
    },

    // API settings
    api: {
        baseUrl: isDev ? 'http://localhost:8000' : 'https://api.example.com',
        timeout: 30000,
        retryAttempts: 3
    },

    // Database settings
    database: {
        type: 'sqlite',
        path: path.join(__dirname, '../data/database.sqlite'),
        backupPath: path.join(__dirname, '../data/backups'),
        maxBackups: 5
    },

    // Cache settings
    cache: {
        enabled: true,
        type: 'file',
        path: path.join(__dirname, '../data/cache'),
        maxSize: 100 * 1024 * 1024, // 100MB
        ttl: 3600 // 1 hour
    },

    // Logging settings
    logging: {
        level: isDev ? 'debug' : 'info',
        file: path.join(__dirname, '../logs/app.log'),
        maxSize: 10 * 1024 * 1024, // 10MB
        maxFiles: 5
    },

    // Update settings
    updates: {
        enabled: true,
        autoDownload: true,
        autoInstall: false,
        checkInterval: 3600000 // 1 hour
    },

    // Security settings
    security: {
        enableCSP: true,
        enableSandbox: true,
        enableRemoteContent: false
    },

    // Feature flags
    features: {
        enableTelemetry: !isDev,
        enableAnalytics: !isDev,
        enableCrashReporting: !isDev
    },

    // Paths
    paths: {
        root: __dirname,
        assets: path.join(__dirname, '../assets'),
        data: path.join(__dirname, '../data'),
        logs: path.join(__dirname, '../logs'),
        temp: path.join(__dirname, '../temp')
    },

    // IPC channels
    channels: {
        app: {
            ready: 'app:ready',
            quit: 'app:quit',
            update: 'app:update'
        },
        window: {
            minimize: 'window:minimize',
            maximize: 'window:maximize',
            close: 'window:close'
        },
        database: {
            query: 'database:query',
            backup: 'database:backup',
            restore: 'database:restore'
        }
    }
}; 