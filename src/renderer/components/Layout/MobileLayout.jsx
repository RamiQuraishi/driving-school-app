/**
 * Mobile layout component optimized for smaller screens.
 * Provides a mobile-friendly interface with bottom navigation and swipe gestures.
 */

import React, { useState } from 'react';
import { Box, useTheme, SwipeableDrawer } from '@mui/material';
import { styled } from '@mui/material/styles';

// Layout components
import Navigation from './Navigation';
import Toolbar from './Toolbar';
import StatusBar from './StatusBar';
import QuickActions from './QuickActions';

// Common components
import ErrorBoundary from '../Common/ErrorBoundary';

const MobileContainer = styled(Box)(({ theme }) => ({
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    overflow: 'hidden',
    backgroundColor: theme.palette.background.default
}));

const ContentContainer = styled(Box)(({ theme }) => ({
    flex: 1,
    overflow: 'auto',
    padding: theme.spacing(2),
    paddingBottom: theme.spacing(8), // Space for bottom navigation
    backgroundColor: theme.palette.background.paper
}));

const BottomNavigation = styled(Box)(({ theme }) => ({
    position: 'fixed',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: theme.palette.background.paper,
    borderTop: `1px solid ${theme.palette.divider}`,
    zIndex: theme.zIndex.appBar
}));

const MobileLayout = ({ children }) => {
    const theme = useTheme();
    const [drawerOpen, setDrawerOpen] = useState(false);
    const [quickActionsOpen, setQuickActionsOpen] = useState(false);

    const toggleDrawer = () => {
        setDrawerOpen(!drawerOpen);
    };

    const toggleQuickActions = () => {
        setQuickActionsOpen(!quickActionsOpen);
    };

    return (
        <ErrorBoundary>
            <MobileContainer>
                <Toolbar
                    onMenuClick={toggleDrawer}
                    onQuickActionsClick={toggleQuickActions}
                    variant="mobile"
                />
                <ContentContainer>
                    {children}
                </ContentContainer>
                <BottomNavigation>
                    <Navigation />
                </BottomNavigation>
                <StatusBar variant="mobile" />
                <SwipeableDrawer
                    anchor="left"
                    open={drawerOpen}
                    onClose={() => setDrawerOpen(false)}
                    onOpen={() => setDrawerOpen(true)}
                    swipeAreaWidth={20}
                >
                    <Box
                        sx={{
                            width: 250,
                            height: '100%',
                            backgroundColor: theme.palette.background.paper
                        }}
                    >
                        {/* Drawer content */}
                    </Box>
                </SwipeableDrawer>
                <QuickActions
                    open={quickActionsOpen}
                    onClose={() => setQuickActionsOpen(false)}
                    variant="mobile"
                />
            </MobileContainer>
        </ErrorBoundary>
    );
};

export default MobileLayout; 