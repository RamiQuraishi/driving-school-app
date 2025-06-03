/**
 * Navigation component for both mobile and desktop views.
 * Provides navigation links and handles routing.
 */

import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
    BottomNavigation,
    BottomNavigationAction,
    Paper,
    useTheme,
    useMediaQuery
} from '@mui/material';
import {
    Home as HomeIcon,
    School as SchoolIcon,
    Person as PersonIcon,
    Settings as SettingsIcon
} from '@mui/icons-material';

const Navigation = () => {
    const theme = useTheme();
    const location = useLocation();
    const navigate = useNavigate();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

    const handleChange = (event, newValue) => {
        navigate(newValue);
    };

    const navigationItems = [
        {
            label: 'Home',
            value: '/',
            icon: <HomeIcon />
        },
        {
            label: 'Schools',
            value: '/schools',
            icon: <SchoolIcon />
        },
        {
            label: 'Profile',
            value: '/profile',
            icon: <PersonIcon />
        },
        {
            label: 'Settings',
            value: '/settings',
            icon: <SettingsIcon />
        }
    ];

    if (isMobile) {
        return (
            <Paper
                sx={{
                    position: 'fixed',
                    bottom: 0,
                    left: 0,
                    right: 0,
                    zIndex: theme.zIndex.appBar
                }}
                elevation={3}
            >
                <BottomNavigation
                    value={location.pathname}
                    onChange={handleChange}
                    showLabels
                >
                    {navigationItems.map((item) => (
                        <BottomNavigationAction
                            key={item.value}
                            label={item.label}
                            value={item.value}
                            icon={item.icon}
                        />
                    ))}
                </BottomNavigation>
            </Paper>
        );
    }

    // Desktop navigation can be implemented here if needed
    return null;
};

export default Navigation; 