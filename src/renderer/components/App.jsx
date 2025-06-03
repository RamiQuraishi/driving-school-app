/**
 * Main App component that serves as the root of the application.
 * Handles routing, theme, and global state management.
 */

import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { useMediaQuery } from '@mui/material';

// Layout components
import MainLayout from './Layout/MainLayout';
import MobileLayout from './Layout/MobileLayout';

// Common components
import ErrorBoundary from './Common/ErrorBoundary';
import OfflineIndicator from './Common/OfflineIndicator';
import NotificationCenter from './Common/NotificationCenter';
import PerformanceWarning from './Common/PerformanceWarning';

// Theme and context
import { lightTheme, darkTheme } from '../theme';
import { AppContext } from '../context/AppContext';

const App = () => {
    // State management
    const [isDarkMode, setIsDarkMode] = useState(false);
    const [isOnline, setIsOnline] = useState(navigator.onLine);
    const [isLoading, setIsLoading] = useState(true);
    const [notifications, setNotifications] = useState([]);
    const [performanceMetrics, setPerformanceMetrics] = useState(null);

    // Responsive design
    const isMobile = useMediaQuery('(max-width:600px)');

    // Theme selection
    const theme = isDarkMode ? darkTheme : lightTheme;

    // Initialize app
    useEffect(() => {
        const initializeApp = async () => {
            try {
                // Load user preferences
                const savedTheme = localStorage.getItem('theme');
                if (savedTheme) {
                    setIsDarkMode(savedTheme === 'dark');
                }

                // Initialize performance monitoring
                window.electron.ipcRenderer.invoke('system:get-metrics')
                    .then(metrics => setPerformanceMetrics(metrics))
                    .catch(console.error);

                setIsLoading(false);
            } catch (error) {
                console.error('Failed to initialize app:', error);
                setIsLoading(false);
            }
        };

        initializeApp();
    }, []);

    // Network status monitoring
    useEffect(() => {
        const handleOnline = () => setIsOnline(true);
        const handleOffline = () => setIsOnline(false);

        window.addEventListener('online', handleOnline);
        window.addEventListener('offline', handleOffline);

        return () => {
            window.removeEventListener('online', handleOnline);
            window.removeEventListener('offline', handleOffline);
        };
    }, []);

    // Performance monitoring
    useEffect(() => {
        const interval = setInterval(() => {
            window.electron.ipcRenderer.invoke('system:get-metrics')
                .then(metrics => setPerformanceMetrics(metrics))
                .catch(console.error);
        }, 5000);

        return () => clearInterval(interval);
    }, []);

    // Theme toggle handler
    const toggleTheme = () => {
        const newTheme = !isDarkMode;
        setIsDarkMode(newTheme);
        localStorage.setItem('theme', newTheme ? 'dark' : 'light');
    };

    // Notification handlers
    const addNotification = (notification) => {
        setNotifications(prev => [...prev, { ...notification, id: Date.now() }]);
    };

    const removeNotification = (id) => {
        setNotifications(prev => prev.filter(n => n.id !== id));
    };

    // Context value
    const contextValue = {
        isDarkMode,
        toggleTheme,
        isOnline,
        isLoading,
        notifications,
        addNotification,
        removeNotification,
        performanceMetrics
    };

    if (isLoading) {
        return <div>Loading...</div>; // Replace with proper loading component
    }

    return (
        <ErrorBoundary>
            <AppContext.Provider value={contextValue}>
                <ThemeProvider theme={theme}>
                    <CssBaseline />
                    <Router>
                        {isMobile ? <MobileLayout /> : <MainLayout />}
                    </Router>
                    <OfflineIndicator />
                    <NotificationCenter />
                    <PerformanceWarning />
                </ThemeProvider>
            </AppContext.Provider>
        </ErrorBoundary>
    );
};

export default App; 