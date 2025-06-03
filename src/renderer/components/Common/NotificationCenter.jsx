/**
 * NotificationCenter component for displaying system notifications.
 * Manages notification queue and provides a UI for viewing notifications.
 */

import React, { useState } from 'react';
import {
    Box,
    IconButton,
    Badge,
    Menu,
    MenuItem,
    Typography,
    List,
    ListItem,
    ListItemText,
    ListItemIcon,
    ListItemSecondaryAction,
    Divider,
    useTheme
} from '@mui/material';
import {
    Notifications as NotificationsIcon,
    NotificationsActive as NotificationsActiveIcon,
    Error as ErrorIcon,
    Warning as WarningIcon,
    Info as InfoIcon,
    CheckCircle as SuccessIcon,
    Close as CloseIcon
} from '@mui/icons-material';
import { useAppContext } from '../../context/AppContext';

const NotificationCenter = () => {
    const theme = useTheme();
    const { notifications, removeNotification } = useAppContext();
    const [anchorEl, setAnchorEl] = useState(null);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const getNotificationIcon = (type) => {
        switch (type) {
            case 'error':
                return <ErrorIcon color="error" />;
            case 'warning':
                return <WarningIcon color="warning" />;
            case 'success':
                return <SuccessIcon color="success" />;
            default:
                return <InfoIcon color="info" />;
        }
    };

    const handleNotificationClick = (notification) => {
        if (notification.onClick) {
            notification.onClick();
        }
        handleClose();
    };

    const handleNotificationDismiss = (id, event) => {
        event.stopPropagation();
        removeNotification(id);
    };

    return (
        <>
            <IconButton
                color="inherit"
                onClick={handleClick}
                sx={{ ml: 1 }}
            >
                <Badge
                    badgeContent={notifications.length}
                    color="error"
                    overlap="circular"
                >
                    {notifications.length > 0 ? (
                        <NotificationsActiveIcon />
                    ) : (
                        <NotificationsIcon />
                    )}
                </Badge>
            </IconButton>

            <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleClose}
                PaperProps={{
                    sx: {
                        width: 360,
                        maxHeight: 480
                    }
                }}
            >
                <Box sx={{ p: 2 }}>
                    <Typography variant="h6">Notifications</Typography>
                </Box>
                <Divider />
                <List sx={{ p: 0 }}>
                    {notifications.length === 0 ? (
                        <ListItem>
                            <ListItemText
                                primary="No new notifications"
                                sx={{ textAlign: 'center', color: 'text.secondary' }}
                            />
                        </ListItem>
                    ) : (
                        notifications.map((notification) => (
                            <ListItem
                                key={notification.id}
                                button
                                onClick={() => handleNotificationClick(notification)}
                                sx={{
                                    '&:hover': {
                                        backgroundColor: theme.palette.action.hover
                                    }
                                }}
                            >
                                <ListItemIcon>
                                    {getNotificationIcon(notification.type)}
                                </ListItemIcon>
                                <ListItemText
                                    primary={notification.title}
                                    secondary={
                                        <>
                                            <Typography
                                                component="span"
                                                variant="body2"
                                                color="text.primary"
                                            >
                                                {notification.message}
                                            </Typography>
                                            {notification.timestamp && (
                                                <Typography
                                                    component="span"
                                                    variant="caption"
                                                    color="text.secondary"
                                                    sx={{ display: 'block' }}
                                                >
                                                    {new Date(notification.timestamp).toLocaleString()}
                                                </Typography>
                                            )}
                                        </>
                                    }
                                />
                                <ListItemSecondaryAction>
                                    <IconButton
                                        edge="end"
                                        size="small"
                                        onClick={(e) => handleNotificationDismiss(notification.id, e)}
                                    >
                                        <CloseIcon fontSize="small" />
                                    </IconButton>
                                </ListItemSecondaryAction>
                            </ListItem>
                        ))
                    )}
                </List>
            </Menu>
        </>
    );
};

export default NotificationCenter; 