/**
 * Electron configuration
 */
const isDev = process.env.NODE_ENV === 'development';

const config = {
    // Application
    appName: 'Ontario Driving School Manager',
    appVersion: '0.1.0',
    
    // Window
    window: {
        width: 1200,
        height: 800,
        minWidth: 800,
        minHeight: 600,
        title: 'Ontario Driving School Manager'
    },
    
    // Development
    isDev,
    devTools: isDev,
    
    // API
    api: {
        baseUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000',
        timeout: 30000,
        retries: 3
    },
    
    // Features
    features: {
        analytics: true,
        telemetry: true,
        performanceMonitoring: true,
        errorTracking: true,
        conflictTracking: true
    },
    
    // Security
    security: {
        contextIsolation: true,
        nodeIntegration: false,
        sandbox: true
    },
    
    // Logging
    logging: {
        level: isDev ? 'debug' : 'info',
        file: 'logs/electron.log'
    }
};

export default config; 