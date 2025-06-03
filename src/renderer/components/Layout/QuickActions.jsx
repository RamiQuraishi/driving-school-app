/**
 * QuickActions component for providing floating action buttons for common tasks.
 * Shows different actions based on the current route and user permissions.
 */

import React from 'react';
import {
    SpeedDial,
    SpeedDialAction,
    SpeedDialIcon,
    useTheme,
    useMediaQuery
} from '@mui/material';
import {
    Add as AddIcon,
    Edit as EditIcon,
    Delete as DeleteIcon,
    Print as PrintIcon,
    Share as ShareIcon,
    Save as SaveIcon,
    Refresh as RefreshIcon
} from '@mui/icons-material';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAppContext } from '../../context/AppContext';

const QuickActions = () => {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    const location = useLocation();
    const navigate = useNavigate();
    const { user } = useAppContext();

    // Define actions based on current route
    const getActions = () => {
        const baseActions = [
            { icon: <RefreshIcon />, name: 'Refresh', action: () => window.location.reload() }
        ];

        // Add route-specific actions
        if (location.pathname.startsWith('/schools')) {
            return [
                ...baseActions,
                { icon: <AddIcon />, name: 'New School', action: () => navigate('/schools/new') },
                { icon: <PrintIcon />, name: 'Print List', action: () => {/* Handle print */} },
                { icon: <ShareIcon />, name: 'Share', action: () => {/* Handle share */} }
            ];
        }

        if (location.pathname.startsWith('/students')) {
            return [
                ...baseActions,
                { icon: <AddIcon />, name: 'New Student', action: () => navigate('/students/new') },
                { icon: <PrintIcon />, name: 'Print List', action: () => {/* Handle print */} },
                { icon: <ShareIcon />, name: 'Share', action: () => {/* Handle share */} }
            ];
        }

        if (location.pathname.startsWith('/lessons')) {
            return [
                ...baseActions,
                { icon: <AddIcon />, name: 'New Lesson', action: () => navigate('/lessons/new') },
                { icon: <SaveIcon />, name: 'Save', action: () => {/* Handle save */} },
                { icon: <PrintIcon />, name: 'Print', action: () => {/* Handle print */} }
            ];
        }

        return baseActions;
    };

    return (
        <SpeedDial
            ariaLabel="Quick Actions"
            sx={{
                position: 'fixed',
                bottom: isMobile ? 80 : 32,
                right: 32,
                zIndex: theme.zIndex.speedDial
            }}
            icon={<SpeedDialIcon />}
            direction="up"
        >
            {getActions().map((action) => (
                <SpeedDialAction
                    key={action.name}
                    icon={action.icon}
                    tooltipTitle={action.name}
                    onClick={action.action}
                />
            ))}
        </SpeedDial>
    );
};

export default QuickActions; 