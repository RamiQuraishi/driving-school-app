/**
 * Feature flags for the renderer process
 */
const isDev = process.env.NODE_ENV === 'development';

const features = {
    // Core features
    analytics: {
        enabled: true,
        privacyCompliant: true,
        dataRetentionDays: 30
    },
    
    telemetry: {
        enabled: true,
        anonymous: true,
        collectionInterval: 3600 // 1 hour
    },
    
    monitoring: {
        performance: true,
        errors: true,
        conflicts: true
    },
    
    // UI features
    ui: {
        darkMode: true,
        animations: true,
        accessibility: true
    },
    
    // Development features
    development: {
        devTools: isDev,
        hotReload: isDev,
        debugMode: isDev
    },
    
    // Experimental features
    experimental: {
        enabled: false,
        features: []
    }
};

export default features; 