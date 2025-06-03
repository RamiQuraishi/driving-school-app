/**
 * TouchableList component for mobile touch interactions.
 * Provides swipe actions and touch feedback for list items.
 */

import React, { useState, useCallback } from 'react';
import {
    List,
    ListItem,
    ListItemText,
    ListItemSecondaryAction,
    IconButton,
    Box,
    useTheme
} from '@mui/material';
import { useTouchGestures } from '../../hooks/useTouchGestures';

const TouchableList = ({
    items,
    onItemClick,
    onSwipeLeft,
    onSwipeRight,
    renderItem,
    style = {}
}) => {
    const theme = useTheme();
    const [activeItem, setActiveItem] = useState(null);
    const [swipePosition, setSwipePosition] = useState(0);

    const handleDragStart = useCallback((itemId) => {
        setActiveItem(itemId);
    }, []);

    const handleDragMove = useCallback((deltaX) => {
        if (!activeItem) return;
        setSwipePosition(deltaX);
    }, [activeItem]);

    const handleDragEnd = useCallback((deltaX, velocity) => {
        if (!activeItem) return;

        const threshold = window.innerWidth * 0.3;
        const shouldTrigger = Math.abs(deltaX) > threshold || Math.abs(velocity) > 0.5;

        if (shouldTrigger) {
            if (deltaX > 0) {
                onSwipeRight?.(activeItem);
            } else {
                onSwipeLeft?.(activeItem);
            }
        }

        setActiveItem(null);
        setSwipePosition(0);
    }, [activeItem, onSwipeLeft, onSwipeRight]);

    const { bind } = useTouchGestures({
        onDragStart: () => handleDragStart(activeItem),
        onDragMove: handleDragMove,
        onDragEnd: handleDragEnd
    });

    const defaultRenderItem = (item) => (
        <ListItem
            button
            onClick={() => onItemClick?.(item)}
            sx={{
                transform: activeItem === item.id ? `translateX(${swipePosition}px)` : 'none',
                transition: theme.transitions.create('transform'),
                backgroundColor: theme.palette.background.paper,
                '&:active': {
                    backgroundColor: theme.palette.action.selected
                }
            }}
        >
            <ListItemText
                primary={item.title}
                secondary={item.subtitle}
            />
            {item.actions && (
                <ListItemSecondaryAction>
                    {item.actions}
                </ListItemSecondaryAction>
            )}
        </ListItem>
    );

    return (
        <List
            {...bind}
            sx={{
                width: '100%',
                ...style
            }}
        >
            {items.map((item) => (
                <Box
                    key={item.id}
                    sx={{
                        position: 'relative',
                        overflow: 'hidden'
                    }}
                >
                    {renderItem ? renderItem(item) : defaultRenderItem(item)}
                </Box>
            ))}
        </List>
    );
};

export default TouchableList; 