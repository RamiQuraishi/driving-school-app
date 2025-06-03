/**
 * Actions index file.
 * Exports all action creators for the application.
 */

// Auth actions
export {
    setCredentials,
    updateUser,
    updatePermissions,
    updateActivity,
    logout,
    setInitialized
} from '../reducers/auth';

// Sync actions
export {
    setOnlineStatus,
    startSync,
    completeSync,
    addPendingChange,
    removePendingChange,
    addConflict,
    resolveConflict,
    updateVersion,
    addSyncError,
    clearSyncErrors,
    resetSync
} from '../reducers/sync';

// UI actions
export {
    setTheme,
    toggleSidebar,
    toggleQuickActions,
    addNotification,
    removeNotification,
    setActiveModal,
    setActiveTour,
    updateLayout,
    updatePreferences,
    setLoadingState,
    addError,
    removeError,
    clearErrors
} from '../reducers/ui';

// Features actions
export {
    setFeatureFlag,
    setFeatureFlags,
    setExperiment,
    recordExperimentResult,
    setRollout,
    addBetaFeature,
    removeBetaFeature,
    addPremiumFeature,
    removePremiumFeature,
    resetFeatures
} from '../reducers/features';

// MTO Export actions
export {
    startExport,
    updateProgress,
    completeExport,
    failExport,
    updateExportConfig,
    clearExportHistory,
    resetExport
} from '../reducers/mtoExport';

// Conflicts actions
export {
    addConflict,
    resolveConflict,
    setResolutionStrategy,
    toggleAutoResolve,
    setMergeStrategy,
    clearResolvedConflicts,
    clearConflictHistory,
    resetConflicts
} from '../reducers/conflicts';

// Performance actions
export {
    updateMetrics,
    setThresholds,
    startMonitoring,
    stopMonitoring,
    clearHistory,
    resetMetrics
} from '../reducers/performance'; 