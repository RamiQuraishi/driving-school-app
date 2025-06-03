/**
 * Main layout component for desktop view.
 * Provides the primary application structure with sidebar, toolbar, and content area.
 */

import React, { useState } from 'react';
import { Box, useTheme } from '@mui/material';
import { styled } from '@mui/material/styles';

// Layout components
import Sidebar from './Sidebar';
import Toolbar from './Toolbar';
import StatusBar from './StatusBar';
import QuickActions from './QuickActions';

// Common components
import ErrorBoundary from '../Common/ErrorBoundary';

const MainContainer = styled(Box)(({ theme }) => ({
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    overflow: 'hidden',
    backgroundColor: theme.palette.background.default
}));

const ContentContainer = styled(Box)(({ theme }) => ({
    display: 'flex',
    flex: 1,
    overflow: 'hidden'
}));

const MainContent = styled(Box)(({ theme }) => ({
    flex: 1,
    overflow: 'auto',
    padding: theme.spacing(2),
    backgroundColor: theme.palette.background.paper
}));

const MainLayout = ({ children }) => {
    const theme = useTheme();
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const [quickActionsOpen, setQuickActionsOpen] = useState(false);

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };

    const toggleQuickActions = () => {
        setQuickActionsOpen(!quickActionsOpen);
    };

    return (
        <ErrorBoundary>
            <MainContainer>
                <Toolbar
                    onMenuClick={toggleSidebar}
                    onQuickActionsClick={toggleQuickActions}
                />
                <ContentContainer>
                    <Sidebar
                        open={sidebarOpen}
                        onClose={() => setSidebarOpen(false)}
                    />
                    <MainContent>
                        {children}
                    </MainContent>
                    <QuickActions
                        open={quickActionsOpen}
                        onClose={() => setQuickActionsOpen(false)}
                    />
                </ContentContainer>
                <StatusBar />
            </MainContainer>
        </ErrorBoundary>
    );
};

export default MainLayout; 