/**
 * OfflineIndicator component for displaying offline status.
 * Shows a banner when the app loses internet connectivity.
 */

import React, { useEffect, useState } from 'react';
import {
    Snackbar,
    Alert,
    IconButton,
    useTheme
} from '@mui/material';
import {
    CloudOff as OfflineIcon,
    Close as CloseIcon,
    Refresh as RefreshIcon
} from '@mui/icons-material';
import { useAppContext } from '../../context/AppContext';

const OfflineIndicator = () => {
    const theme = useTheme();
    const { isOnline } = useAppContext();
    const [open, setOpen] = useState(false);
    const [autoHide, setAutoHide] = useState(true);

    useEffect(() => {
        if (!isOnline) {
            setOpen(true);
            setAutoHide(false);
        } else {
            setOpen(false);
        }
    }, [isOnline]);

    const handleClose = () => {
        setOpen(false);
    };

    const handleRetry = () => {
        window.location.reload();
    };

    return (
        <Snackbar
            open={open}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            sx={{
                bottom: { xs: 56, sm: 0 } // Account for mobile navigation
            }}
        >
            <Alert
                severity="error"
                variant="filled"
                icon={<OfflineIcon />}
                action={
                    <>
                        <IconButton
                            size="small"
                            color="inherit"
                            onClick={handleRetry}
                            sx={{ mr: 1 }}
                        >
                            <RefreshIcon />
                        </IconButton>
                        <IconButton
                            size="small"
                            color="inherit"
                            onClick={handleClose}
                        >
                            <CloseIcon />
                        </IconButton>
                    </>
                }
                sx={{
                    width: '100%',
                    backgroundColor: theme.palette.error.main
                }}
            >
                You are currently offline. Some features may be unavailable.
            </Alert>
        </Snackbar>
    );
};

export default OfflineIndicator; 