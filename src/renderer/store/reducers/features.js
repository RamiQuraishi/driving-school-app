/**
 * Features reducer for managing feature flags and toggles.
 * Handles feature availability and A/B testing.
 */

import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    flags: {
        // Core features
        offlineMode: true,
        darkMode: true,
        notifications: true,
        sync: true,
        
        // Experimental features
        advancedSearch: false,
        dataExport: false,
        analytics: false,
        
        // A/B test features
        newDashboard: 'control',
        enhancedForms: 'test',
        
        // User-specific features
        betaFeatures: [],
        premiumFeatures: []
    },
    experiments: {
        active: {},
        results: {}
    },
    rollout: {
        percentage: 0,
        startDate: null,
        endDate: null
    }
};

const featuresSlice = createSlice({
    name: 'features',
    initialState,
    reducers: {
        setFeatureFlag: (state, action) => {
            const { flag, value } = action.payload;
            state.flags[flag] = value;
        },
        setFeatureFlags: (state, action) => {
            state.flags = { ...state.flags, ...action.payload };
        },
        setExperiment: (state, action) => {
            const { name, variant } = action.payload;
            state.experiments.active[name] = variant;
        },
        recordExperimentResult: (state, action) => {
            const { name, result } = action.payload;
            if (!state.experiments.results[name]) {
                state.experiments.results[name] = [];
            }
            state.experiments.results[name].push({
                ...result,
                timestamp: Date.now()
            });
        },
        setRollout: (state, action) => {
            state.rollout = { ...state.rollout, ...action.payload };
        },
        addBetaFeature: (state, action) => {
            if (!state.flags.betaFeatures.includes(action.payload)) {
                state.flags.betaFeatures.push(action.payload);
            }
        },
        removeBetaFeature: (state, action) => {
            state.flags.betaFeatures = state.flags.betaFeatures.filter(
                feature => feature !== action.payload
            );
        },
        addPremiumFeature: (state, action) => {
            if (!state.flags.premiumFeatures.includes(action.payload)) {
                state.flags.premiumFeatures.push(action.payload);
            }
        },
        removePremiumFeature: (state, action) => {
            state.flags.premiumFeatures = state.flags.premiumFeatures.filter(
                feature => feature !== action.payload
            );
        },
        resetFeatures: (state) => {
            return initialState;
        }
    }
});

export const {
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
} = featuresSlice.actions;

// Selectors
export const selectFeatureFlags = (state) => state.features.flags;
export const selectFeatureFlag = (flag) => (state) => state.features.flags[flag];
export const selectExperiments = (state) => state.features.experiments;
export const selectRollout = (state) => state.features.rollout;
export const selectBetaFeatures = (state) => state.features.flags.betaFeatures;
export const selectPremiumFeatures = (state) => state.features.flags.premiumFeatures;

export default featuresSlice.reducer; 