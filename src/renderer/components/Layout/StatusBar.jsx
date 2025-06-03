/**
 * StatusBar component for displaying system status and notifications.
 * Shows network status, sync state, and other system information.
 */

import React from 'react';
import {
    Box,
    Typography,
    IconButton,
    Tooltip,
    useTheme,
    LinearProgress
} from '@mui/material';
import {
    CloudOff as OfflineIcon,
    CloudDone as OnlineIcon,
    Sync as SyncIcon,
    SyncDisabled as SyncDisabledIcon,
    Warning as WarningIcon,
    Error as ErrorIcon
} from '@mui/icons-material';
import { useAppContext } from '../../context/AppContext';

const StatusBar = () => {
    const theme = useTheme();
    const { isOnline, syncStatus, notifications } = useAppContext();

    return (
        <Box
            sx={{
                position: 'fixed',
                bottom: 0,
                left: 0,
                right: 0,
                height: 24,
                backgroundColor: theme.palette.background.paper,
                borderTop: `1px solid ${theme.palette.divider}`,
                display: 'flex',
                alignItems: 'center',
                padding: '0 16px',
                zIndex: theme.zIndex.appBar
            }}
        >
            {/* Network Status */}
            <Tooltip title={isOnline ? 'Online' : 'Offline'}>
                <IconButton
                    size="small"
                    sx={{ color: isOnline ? 'success.main' : 'error.main' }}
                >
                    {isOnline ? <OnlineIcon fontSize="small" /> : <OfflineIcon fontSize="small" />}
                </IconButton>
            </Tooltip>

            {/* Sync Status */}
            <Tooltip title={syncStatus.message}>
                <IconButton
                    size="small"
                    sx={{
                        color: syncStatus.inProgress
                            ? 'info.main'
                            : syncStatus.error
                            ? 'error.main'
                            : 'success.main'
                    }}
                >
                    {syncStatus.inProgress ? (
                        <SyncIcon fontSize="small" className="rotating" />
                    ) : syncStatus.error ? (
                        <SyncDisabledIcon fontSize="small" />
                    ) : (
                        <SyncIcon fontSize="small" />
                    )}
                </IconButton>
            </Tooltip>

            {/* Notifications */}
            {notifications.length > 0 && (
                <Tooltip title={notifications[0].message}>
                    <IconButton
                        size="small"
                        sx={{
                            color: notifications[0].type === 'error'
                                ? 'error.main'
                                : 'warning.main'
                        }}
                    >
                        {notifications[0].type === 'error' ? (
                            <ErrorIcon fontSize="small" />
                        ) : (
                            <WarningIcon fontSize="small" />
                        )}
                    </IconButton>
                </Tooltip>
            )}

            {/* Status Message */}
            <Typography
                variant="caption"
                sx={{
                    ml: 1,
                    color: theme.palette.text.secondary
                }}
            >
                {syncStatus.message}
            </Typography>

            {/* Progress Bar */}
            {syncStatus.inProgress && (
                <LinearProgress
                    variant="determinate"
                    value={syncStatus.progress}
                    sx={{
                        position: 'absolute',
                        bottom: 0,
                        left: 0,
                        right: 0,
                        height: 2
                    }}
                />
            )}
        </Box>
    );
};

export default StatusBar; 