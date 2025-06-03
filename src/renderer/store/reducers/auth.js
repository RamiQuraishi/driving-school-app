/**
 * Auth reducer for managing authentication state.
 * Handles user authentication, session management, and permissions.
 */

import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    user: null,
    token: null,
    refreshToken: null,
    isAuthenticated: false,
    isInitialized: false,
    permissions: [],
    lastActivity: null,
    sessionExpiry: null
};

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setCredentials: (state, action) => {
            const { user, token, refreshToken, permissions } = action.payload;
            state.user = user;
            state.token = token;
            state.refreshToken = refreshToken;
            state.permissions = permissions;
            state.isAuthenticated = true;
            state.isInitialized = true;
            state.lastActivity = Date.now();
            state.sessionExpiry = Date.now() + (30 * 60 * 1000); // 30 minutes
        },
        updateUser: (state, action) => {
            state.user = { ...state.user, ...action.payload };
        },
        updatePermissions: (state, action) => {
            state.permissions = action.payload;
        },
        updateActivity: (state) => {
            state.lastActivity = Date.now();
            state.sessionExpiry = Date.now() + (30 * 60 * 1000);
        },
        logout: (state) => {
            state.user = null;
            state.token = null;
            state.refreshToken = null;
            state.isAuthenticated = false;
            state.permissions = [];
            state.lastActivity = null;
            state.sessionExpiry = null;
        },
        setInitialized: (state) => {
            state.isInitialized = true;
        }
    }
});

export const {
    setCredentials,
    updateUser,
    updatePermissions,
    updateActivity,
    logout,
    setInitialized
} = authSlice.actions;

// Selectors
export const selectCurrentUser = (state) => state.auth.user;
export const selectIsAuthenticated = (state) => state.auth.isAuthenticated;
export const selectIsInitialized = (state) => state.auth.isInitialized;
export const selectPermissions = (state) => state.auth.permissions;
export const selectSessionExpiry = (state) => state.auth.sessionExpiry;

export default authSlice.reducer; 