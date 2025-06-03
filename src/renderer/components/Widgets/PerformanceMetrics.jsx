/**
 * PerformanceMetrics component.
 * Displays real-time performance metrics with visual indicators and thresholds.
 */

import React from 'react';
import {
    Box,
    Paper,
    Typography,
    LinearProgress,
    Tooltip,
    useTheme,
    useMediaQuery
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
    Memory as MemoryIcon,
    Speed as SpeedIcon,
    NetworkCheck as NetworkIcon,
    Storage as StorageIcon
} from '@mui/icons-material';

const MetricPaper = styled(Paper)(({ theme }) => ({
    padding: theme.spacing(2),
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    [theme.breakpoints.down('sm')]: {
        padding: theme.spacing(1.5)
    }
}));

const MetricValue = styled(Typography)(({ theme, color }) => ({
    color: color || theme.palette.text.primary,
    fontWeight: 'bold'
}));

const MetricIcon = styled(Box)(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    marginBottom: theme.spacing(1)
}));

const PerformanceMetrics = ({
    metrics = {
        cpu: { value: 0, threshold: 80 },
        memory: { value: 0, threshold: 85 },
        network: { value: 0, threshold: 90 },
        storage: { value: 0, threshold: 75 }
    },
    showIcons = true,
    showThresholds = true,
    size = 'medium',
    variant = 'elevation'
}) => {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

    const getMetricColor = (value, threshold) => {
        if (value >= threshold) return theme.palette.error.main;
        if (value >= threshold * 0.8) return theme.palette.warning.main;
        return theme.palette.success.main;
    };

    const formatValue = (value, type) => {
        switch (type) {
            case 'cpu':
                return `${value.toFixed(1)}%`;
            case 'memory':
                return `${value.toFixed(1)}%`;
            case 'network':
                return `${value.toFixed(1)}%`;
            case 'storage':
                return `${value.toFixed(1)}%`;
            default:
                return value;
        }
    };

    const getMetricIcon = (type) => {
        switch (type) {
            case 'cpu':
                return <SpeedIcon />;
            case 'memory':
                return <MemoryIcon />;
            case 'network':
                return <NetworkIcon />;
            case 'storage':
                return <StorageIcon />;
            default:
                return null;
        }
    };

    const getMetricLabel = (type) => {
        switch (type) {
            case 'cpu':
                return 'CPU Usage';
            case 'memory':
                return 'Memory Usage';
            case 'network':
                return 'Network Usage';
            case 'storage':
                return 'Storage Usage';
            default:
                return type;
        }
    };

    return (
        <Box
            sx={{
                display: 'grid',
                gridTemplateColumns: {
                    xs: '1fr',
                    sm: 'repeat(2, 1fr)',
                    md: 'repeat(4, 1fr)'
                },
                gap: 2
            }}
        >
            {Object.entries(metrics).map(([type, { value, threshold }]) => (
                <MetricPaper
                    key={type}
                    elevation={variant === 'elevation' ? 2 : 0}
                    variant={variant}
                >
                    <MetricIcon>
                        {showIcons && getMetricIcon(type)}
                        <Typography
                            variant={isMobile ? 'body2' : 'body1'}
                            sx={{ ml: showIcons ? 1 : 0 }}
                        >
                            {getMetricLabel(type)}
                        </Typography>
                    </MetricIcon>

                    <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
                        <Box sx={{ display: 'flex', alignItems: 'baseline', mb: 1 }}>
                            <MetricValue
                                variant={isMobile ? 'h6' : 'h5'}
                                color={getMetricColor(value, threshold)}
                            >
                                {formatValue(value, type)}
                            </MetricValue>
                            {showThresholds && (
                                <Typography
                                    variant="caption"
                                    color="textSecondary"
                                    sx={{ ml: 1 }}
                                >
                                    / {threshold}%
                                </Typography>
                            )}
                        </Box>

                        <Tooltip
                            title={`${value.toFixed(1)}% of ${getMetricLabel(type)}`}
                            placement="bottom"
                        >
                            <LinearProgress
                                variant="determinate"
                                value={value}
                                sx={{
                                    height: 8,
                                    borderRadius: 4,
                                    backgroundColor: theme.palette.grey[200],
                                    '& .MuiLinearProgress-bar': {
                                        backgroundColor: getMetricColor(value, threshold)
                                    }
                                }}
                            />
                        </Tooltip>
                    </Box>
                </MetricPaper>
            ))}
        </Box>
    );
};

export default PerformanceMetrics; 