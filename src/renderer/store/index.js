/**
 * Redux store configuration.
 * Sets up the store with middleware and reducers.
 */

import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { combineReducers } from 'redux';

import authReducer from './reducers/auth';
import syncReducer from './reducers/sync';
import uiReducer from './reducers/ui';
import featuresReducer from './reducers/features';

// Configure persist options
const persistConfig = {
    key: 'root',
    storage,
    whitelist: ['auth', 'ui', 'features'], // Only persist these reducers
    blacklist: ['sync'] // Don't persist sync state
};

// Combine reducers
const rootReducer = combineReducers({
    auth: authReducer,
    sync: syncReducer,
    ui: uiReducer,
    features: featuresReducer
});

// Create persisted reducer
const persistedReducer = persistReducer(persistConfig, rootReducer);

// Configure store
const store = configureStore({
    reducer: persistedReducer,
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: {
                // Ignore these action types
                ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
                // Ignore these field paths in all actions
                ignoredActionPaths: ['meta.arg', 'payload.timestamp'],
                // Ignore these paths in the state
                ignoredPaths: ['sync.pendingChanges']
            }
        })
});

// Create persistor
const persistor = persistStore(store);

export { store, persistor };
export default store; 