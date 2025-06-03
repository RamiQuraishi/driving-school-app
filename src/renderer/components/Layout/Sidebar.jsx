/**
 * Sidebar component for desktop view.
 * Provides navigation and quick access to features.
 */

import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
    Drawer,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    ListItemButton,
    Divider,
    Box,
    useTheme
} from '@mui/material';
import {
    Home as HomeIcon,
    School as SchoolIcon,
    Person as PersonIcon,
    Settings as SettingsIcon,
    Dashboard as DashboardIcon,
    CalendarToday as CalendarIcon,
    Assessment as AssessmentIcon,
    Help as HelpIcon
} from '@mui/icons-material';

const DRAWER_WIDTH = 240;

const Sidebar = ({ open, onClose }) => {
    const theme = useTheme();
    const location = useLocation();
    const navigate = useNavigate();

    const navigationItems = [
        {
            label: 'Home',
            path: '/',
            icon: <HomeIcon />
        },
        {
            label: 'Schools',
            path: '/schools',
            icon: <SchoolIcon />
        },
        {
            label: 'Dashboard',
            path: '/dashboard',
            icon: <DashboardIcon />
        },
        {
            label: 'Calendar',
            path: '/calendar',
            icon: <CalendarIcon />
        },
        {
            label: 'Reports',
            path: '/reports',
            icon: <AssessmentIcon />
        }
    ];

    const secondaryItems = [
        {
            label: 'Profile',
            path: '/profile',
            icon: <PersonIcon />
        },
        {
            label: 'Settings',
            path: '/settings',
            icon: <SettingsIcon />
        },
        {
            label: 'Help',
            path: '/help',
            icon: <HelpIcon />
        }
    ];

    const handleNavigation = (path) => {
        navigate(path);
        onClose();
    };

    return (
        <Drawer
            variant="persistent"
            open={open}
            onClose={onClose}
            sx={{
                width: DRAWER_WIDTH,
                flexShrink: 0,
                '& .MuiDrawer-paper': {
                    width: DRAWER_WIDTH,
                    boxSizing: 'border-box',
                    backgroundColor: theme.palette.background.paper,
                    borderRight: `1px solid ${theme.palette.divider}`
                }
            }}
        >
            <Box sx={{ overflow: 'auto' }}>
                <List>
                    {navigationItems.map((item) => (
                        <ListItem key={item.path} disablePadding>
                            <ListItemButton
                                selected={location.pathname === item.path}
                                onClick={() => handleNavigation(item.path)}
                            >
                                <ListItemIcon>{item.icon}</ListItemIcon>
                                <ListItemText primary={item.label} />
                            </ListItemButton>
                        </ListItem>
                    ))}
                </List>
                <Divider />
                <List>
                    {secondaryItems.map((item) => (
                        <ListItem key={item.path} disablePadding>
                            <ListItemButton
                                selected={location.pathname === item.path}
                                onClick={() => handleNavigation(item.path)}
                            >
                                <ListItemIcon>{item.icon}</ListItemIcon>
                                <ListItemText primary={item.label} />
                            </ListItemButton>
                        </ListItem>
                    ))}
                </List>
            </Box>
        </Drawer>
    );
};

export default Sidebar; 