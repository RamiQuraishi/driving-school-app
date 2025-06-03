/**
 * SwipeableViews component for mobile swipe navigation.
 * Provides smooth swipe transitions between views with touch gestures.
 */

import React, { useState, useCallback } from 'react';
import { Box, useTheme } from '@mui/material';
import { useTouchGestures } from '../../hooks/useTouchGestures';

const SwipeableViews = ({
    children,
    index = 0,
    onChangeIndex,
    threshold = 0.3,
    resistance = 0.5,
    style = {}
}) => {
    const theme = useTheme();
    const [position, setPosition] = useState(0);
    const [isDragging, setIsDragging] = useState(false);

    const handleDragStart = useCallback(() => {
        setIsDragging(true);
    }, []);

    const handleDragMove = useCallback((deltaX) => {
        if (!isDragging) return;

        const newPosition = deltaX * resistance;
        setPosition(newPosition);
    }, [isDragging, resistance]);

    const handleDragEnd = useCallback((deltaX, velocity) => {
        setIsDragging(false);

        const shouldChange = Math.abs(deltaX) > window.innerWidth * threshold ||
            Math.abs(velocity) > 0.5;

        if (shouldChange) {
            const direction = deltaX > 0 ? -1 : 1;
            const newIndex = Math.max(0, Math.min(children.length - 1, index + direction));
            onChangeIndex?.(newIndex);
        }

        setPosition(0);
    }, [index, children.length, threshold, onChangeIndex]);

    const { bind } = useTouchGestures({
        onDragStart: handleDragStart,
        onDragMove: handleDragMove,
        onDragEnd: handleDragEnd
    });

    return (
        <Box
            {...bind}
            sx={{
                position: 'relative',
                overflow: 'hidden',
                touchAction: 'pan-y',
                ...style
            }}
        >
            <Box
                sx={{
                    display: 'flex',
                    width: '100%',
                    height: '100%',
                    transform: `translateX(${position}px)`,
                    transition: isDragging ? 'none' : theme.transitions.create('transform'),
                }}
            >
                {React.Children.map(children, (child, i) => (
                    <Box
                        key={i}
                        sx={{
                            flex: '0 0 100%',
                            width: '100%',
                            height: '100%',
                            display: i === index ? 'block' : 'none'
                        }}
                    >
                        {child}
                    </Box>
                ))}
            </Box>
        </Box>
    );
};

export default SwipeableViews; 