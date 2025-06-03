/**
 * LoadingSpinner component for displaying loading states.
 * Supports different variants and sizes with customizable messages.
 */

import React from 'react';
import {
    Box,
    CircularProgress,
    Typography,
    useTheme
} from '@mui/material';

const LoadingSpinner = ({
    message = 'Loading...',
    size = 'medium',
    variant = 'circular',
    fullScreen = false,
    color = 'primary'
}) => {
    const theme = useTheme();

    // Size mapping
    const sizeMap = {
        small: 24,
        medium: 40,
        large: 60
    };

    const spinnerSize = sizeMap[size] || sizeMap.medium;

    const spinnerContent = (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 2
            }}
        >
            <CircularProgress
                size={spinnerSize}
                color={color}
                variant={variant === 'determinate' ? 'determinate' : 'indeterminate'}
            />
            {message && (
                <Typography
                    variant="body2"
                    color="textSecondary"
                    sx={{ mt: 1 }}
                >
                    {message}
                </Typography>
            )}
        </Box>
    );

    if (fullScreen) {
        return (
            <Box
                sx={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    backgroundColor: theme.palette.background.paper,
                    zIndex: theme.zIndex.modal
                }}
            >
                {spinnerContent}
            </Box>
        );
    }

    return spinnerContent;
};

export default LoadingSpinner; 