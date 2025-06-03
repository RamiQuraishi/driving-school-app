/**
 * PerformanceWarning component for alerting users about slow performance.
 * Monitors and displays warnings for CPU, memory, and renderer performance issues.
 */

import React, { useEffect, useState } from 'react';
import {
    Snackbar,
    Alert,
    IconButton,
    Typography,
    Box,
    useTheme
} from '@mui/material';
import {
    Speed as SpeedIcon,
    Memory as MemoryIcon,
    Cpu as CpuIcon,
    Close as CloseIcon
} from '@mui/icons-material';
import { useAppContext } from '../../context/AppContext';

const PerformanceWarning = () => {
    const theme = useTheme();
    const { performanceMetrics } = useAppContext();
    const [warning, setWarning] = useState(null);

    useEffect(() => {
        if (!performanceMetrics) return;

        const { cpu, memory, fps } = performanceMetrics;
        let newWarning = null;

        // Check CPU usage
        if (cpu > 80) {
            newWarning = {
                type: 'cpu',
                message: 'High CPU usage detected. This may affect performance.',
                severity: 'warning'
            };
        }

        // Check memory usage
        if (memory.percentage > 90) {
            newWarning = {
                type: 'memory',
                message: 'High memory usage detected. Consider closing unused tabs.',
                severity: 'error'
            };
        }

        // Check FPS
        if (fps < 30) {
            newWarning = {
                type: 'fps',
                message: 'Low frame rate detected. The application may feel sluggish.',
                severity: 'warning'
            };
        }

        setWarning(newWarning);
    }, [performanceMetrics]);

    const getWarningIcon = () => {
        if (!warning) return null;

        switch (warning.type) {
            case 'cpu':
                return <CpuIcon />;
            case 'memory':
                return <MemoryIcon />;
            case 'fps':
                return <SpeedIcon />;
            default:
                return null;
        }
    };

    const handleClose = () => {
        setWarning(null);
    };

    if (!warning) return null;

    return (
        <Snackbar
            open={Boolean(warning)}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            sx={{
                bottom: { xs: 56, sm: 0 } // Account for mobile navigation
            }}
        >
            <Alert
                severity={warning.severity}
                variant="filled"
                icon={getWarningIcon()}
                action={
                    <IconButton
                        size="small"
                        color="inherit"
                        onClick={handleClose}
                    >
                        <CloseIcon />
                    </IconButton>
                }
                sx={{
                    width: '100%',
                    backgroundColor: warning.severity === 'error'
                        ? theme.palette.error.main
                        : theme.palette.warning.main
                }}
            >
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="body2">
                        {warning.message}
                    </Typography>
                </Box>
            </Alert>
        </Snackbar>
    );
};

export default PerformanceWarning; 