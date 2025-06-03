/**
 * PullToRefresh component for mobile pull-to-refresh functionality.
 * Provides visual feedback and triggers refresh on pull down.
 */

import React, { useState, useCallback } from 'react';
import {
    Box,
    CircularProgress,
    useTheme
} from '@mui/material';
import { useTouchGestures } from '../../hooks/useTouchGestures';

const PullToRefresh = ({
    onRefresh,
    children,
    threshold = 80,
    style = {}
}) => {
    const theme = useTheme();
    const [isRefreshing, setIsRefreshing] = useState(false);
    const [pullDistance, setPullDistance] = useState(0);

    const handleDragStart = useCallback(() => {
        if (isRefreshing) return;
        setPullDistance(0);
    }, [isRefreshing]);

    const handleDragMove = useCallback((deltaY) => {
        if (isRefreshing) return;
        if (deltaY < 0) return; // Only allow pulling down

        const newDistance = Math.min(deltaY * 0.5, threshold * 1.5);
        setPullDistance(newDistance);
    }, [isRefreshing, threshold]);

    const handleDragEnd = useCallback(async (deltaY) => {
        if (isRefreshing) return;

        if (deltaY > threshold) {
            setIsRefreshing(true);
            try {
                await onRefresh();
            } finally {
                setIsRefreshing(false);
                setPullDistance(0);
            }
        } else {
            setPullDistance(0);
        }
    }, [isRefreshing, threshold, onRefresh]);

    const { bind } = useTouchGestures({
        onDragStart: handleDragStart,
        onDragMove: handleDragMove,
        onDragEnd: handleDragEnd
    });

    const progress = Math.min((pullDistance / threshold) * 100, 100);

    return (
        <Box
            {...bind}
            sx={{
                position: 'relative',
                overflow: 'hidden',
                ...style
            }}
        >
            <Box
                sx={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    height: threshold,
                    transform: `translateY(${pullDistance - threshold}px)`,
                    transition: isRefreshing ? 'none' : theme.transitions.create('transform'),
                    zIndex: 1
                }}
            >
                <CircularProgress
                    variant={isRefreshing ? 'indeterminate' : 'determinate'}
                    value={progress}
                    size={24}
                    thickness={4}
                />
            </Box>
            <Box
                sx={{
                    transform: `translateY(${pullDistance}px)`,
                    transition: isRefreshing ? 'none' : theme.transitions.create('transform')
                }}
            >
                {children}
            </Box>
        </Box>
    );
};

export default PullToRefresh; 