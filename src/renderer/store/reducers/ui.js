/**
 * UI reducer for managing application UI state.
 * Handles theme, layout, and UI preferences.
 */

import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    theme: 'light',
    isDarkMode: false,
    isSidebarOpen: true,
    isQuickActionsOpen: false,
    notifications: [],
    activeModal: null,
    activeTour: null,
    layout: {
        isMobile: false,
        isTablet: false,
        isDesktop: true
    },
    preferences: {
        fontSize: 'medium',
        animationSpeed: 'normal',
        reduceMotion: false,
        highContrast: false
    },
    loadingStates: {},
    errors: []
};

const uiSlice = createSlice({
    name: 'ui',
    initialState,
    reducers: {
        setTheme: (state, action) => {
            state.theme = action.payload;
            state.isDarkMode = action.payload === 'dark';
        },
        toggleSidebar: (state) => {
            state.isSidebarOpen = !state.isSidebarOpen;
        },
        toggleQuickActions: (state) => {
            state.isQuickActionsOpen = !state.isQuickActionsOpen;
        },
        addNotification: (state, action) => {
            state.notifications.push({
                id: Date.now(),
                ...action.payload
            });
        },
        removeNotification: (state, action) => {
            state.notifications = state.notifications.filter(
                notification => notification.id !== action.payload
            );
        },
        setActiveModal: (state, action) => {
            state.activeModal = action.payload;
        },
        setActiveTour: (state, action) => {
            state.activeTour = action.payload;
        },
        updateLayout: (state, action) => {
            state.layout = { ...state.layout, ...action.payload };
        },
        updatePreferences: (state, action) => {
            state.preferences = { ...state.preferences, ...action.payload };
        },
        setLoadingState: (state, action) => {
            const { key, isLoading } = action.payload;
            state.loadingStates[key] = isLoading;
        },
        addError: (state, action) => {
            state.errors.push({
                id: Date.now(),
                ...action.payload
            });
        },
        removeError: (state, action) => {
            state.errors = state.errors.filter(
                error => error.id !== action.payload
            );
        },
        clearErrors: (state) => {
            state.errors = [];
        }
    }
});

export const {
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
} = uiSlice.actions;

// Selectors
export const selectTheme = (state) => state.ui.theme;
export const selectIsDarkMode = (state) => state.ui.isDarkMode;
export const selectIsSidebarOpen = (state) => state.ui.isSidebarOpen;
export const selectIsQuickActionsOpen = (state) => state.ui.isQuickActionsOpen;
export const selectNotifications = (state) => state.ui.notifications;
export const selectActiveModal = (state) => state.ui.activeModal;
export const selectActiveTour = (state) => state.ui.activeTour;
export const selectLayout = (state) => state.ui.layout;
export const selectPreferences = (state) => state.ui.preferences;
export const selectLoadingStates = (state) => state.ui.loadingStates;
export const selectErrors = (state) => state.ui.errors;

export default uiSlice.reducer; 