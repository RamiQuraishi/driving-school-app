/**
 * Feature flags configuration for the renderer process.
 * Manages feature toggles and experimental features in the frontend.
 */

const isDev = process.env.NODE_ENV === 'development';

const features = {
    // Core features
    core: {
        enableOfflineMode: true,
        enableDataSync: true,
        enableAutoSave: true,
        enableKeyboardShortcuts: true
    },

    // UI features
    ui: {
        enableDarkMode: true,
        enableAnimations: true,
        enableTooltips: true,
        enableContextMenu: true,
        enableDragAndDrop: true
    },

    // Student management features
    students: {
        enableBulkImport: true,
        enableExport: true,
        enableSearch: true,
        enableFilters: true,
        enableSorting: true
    },

    // Course management features
    courses: {
        enableScheduling: true,
        enableWaitlist: true,
        enablePrerequisites: true,
        enableCertificates: true
    },

    // Instructor management features
    instructors: {
        enableAvailability: true,
        enableScheduling: true,
        enablePerformance: true,
        enablePayroll: true
    },

    // Vehicle management features
    vehicles: {
        enableMaintenance: true,
        enableTracking: true,
        enableScheduling: true,
        enableReports: true
    },

    // Financial features
    financial: {
        enableInvoicing: true,
        enablePayments: true,
        enableRefunds: true,
        enableReports: true
    },

    // Reporting features
    reporting: {
        enableCustomReports: true,
        enableExport: true,
        enableCharts: true,
        enableDashboards: true
    },

    // Communication features
    communication: {
        enableEmail: true,
        enableSMS: true,
        enableNotifications: true,
        enableTemplates: true
    },

    // Integration features
    integration: {
        enableGoogleCalendar: true,
        enableStripe: true,
        enableQuickBooks: true,
        enableZapier: true
    },

    // Development features
    development: {
        enableDevTools: isDev,
        enableHotReload: isDev,
        enableDebugMode: isDev,
        enablePerformanceMonitor: isDev
    },

    // Experimental features
    experimental: {
        enableAI: false,
        enableVoiceCommands: false,
        enableAR: false,
        enableBlockchain: false
    }
};

// Feature flag management
class FeatureManager {
    constructor() {
        this.features = features;
        this.overrides = new Map();
    }

    /**
     * Check if a feature is enabled
     * @param {string} path - Dot notation path to feature (e.g., 'ui.enableDarkMode')
     * @returns {boolean} - Whether the feature is enabled
     */
    isEnabled(path) {
        // Check for override first
        if (this.overrides.has(path)) {
            return this.overrides.get(path);
        }

        // Get feature value
        const value = this.getFeatureValue(path);
        return value === true;
    }

    /**
     * Get a feature's value
     * @param {string} path - Dot notation path to feature
     * @returns {any} - Feature value
     */
    getFeatureValue(path) {
        return path.split('.').reduce((obj, key) => obj?.[key], this.features);
    }

    /**
     * Override a feature flag
     * @param {string} path - Dot notation path to feature
     * @param {boolean} value - New value
     */
    override(path, value) {
        this.overrides.set(path, value);
    }

    /**
     * Remove a feature override
     * @param {string} path - Dot notation path to feature
     */
    removeOverride(path) {
        this.overrides.delete(path);
    }

    /**
     * Get all enabled features
     * @returns {Object} - Object containing all enabled features
     */
    getEnabledFeatures() {
        const enabled = {};
        this.traverseFeatures(this.features, '', enabled);
        return enabled;
    }

    /**
     * Traverse features object recursively
     * @private
     */
    traverseFeatures(obj, path, result) {
        for (const [key, value] of Object.entries(obj)) {
            const newPath = path ? `${path}.${key}` : key;
            if (typeof value === 'object' && value !== null) {
                this.traverseFeatures(value, newPath, result);
            } else if (value === true) {
                result[newPath] = true;
            }
        }
    }
}

// Create singleton instance
const featureManager = new FeatureManager();

// Export both the features object and the manager
module.exports = {
    features,
    featureManager
}; 