/**
 * Hook for handling touch gestures and interactions.
 * Provides touch event handling with velocity and direction detection.
 */

import { useCallback, useRef } from 'react';

const useTouchGestures = ({
    onDragStart,
    onDragMove,
    onDragEnd,
    onTap,
    onDoubleTap,
    onPinch,
    onRotate
}) => {
    const startPos = useRef({ x: 0, y: 0 });
    const startTime = useRef(0);
    const lastTap = useRef(0);
    const isDragging = useRef(false);
    const startDistance = useRef(0);
    const startAngle = useRef(0);

    const getTouchPosition = (event) => {
        const touch = event.touches[0] || event.changedTouches[0];
        return {
            x: touch.clientX,
            y: touch.clientY
        };
    };

    const getTouchDistance = (event) => {
        if (event.touches.length < 2) return 0;
        const dx = event.touches[1].clientX - event.touches[0].clientX;
        const dy = event.touches[1].clientY - event.touches[0].clientY;
        return Math.sqrt(dx * dx + dy * dy);
    };

    const getTouchAngle = (event) => {
        if (event.touches.length < 2) return 0;
        const dx = event.touches[1].clientX - event.touches[0].clientX;
        const dy = event.touches[1].clientY - event.touches[0].clientY;
        return Math.atan2(dy, dx) * 180 / Math.PI;
    };

    const handleTouchStart = useCallback((event) => {
        const pos = getTouchPosition(event);
        startPos.current = pos;
        startTime.current = Date.now();
        isDragging.current = false;

        if (event.touches.length === 2) {
            startDistance.current = getTouchDistance(event);
            startAngle.current = getTouchAngle(event);
        }

        onDragStart?.(pos);
    }, [onDragStart]);

    const handleTouchMove = useCallback((event) => {
        if (!startPos.current) return;

        const pos = getTouchPosition(event);
        const deltaX = pos.x - startPos.current.x;
        const deltaY = pos.y - startPos.current.y;

        // Start dragging after a small threshold
        if (!isDragging.current && (Math.abs(deltaX) > 5 || Math.abs(deltaY) > 5)) {
            isDragging.current = true;
        }

        if (isDragging.current) {
            onDragMove?.(deltaX, deltaY);
        }

        if (event.touches.length === 2) {
            const distance = getTouchDistance(event);
            const angle = getTouchAngle(event);
            const scale = distance / startDistance.current;
            const rotation = angle - startAngle.current;

            onPinch?.(scale);
            onRotate?.(rotation);
        }
    }, [onDragMove, onPinch, onRotate]);

    const handleTouchEnd = useCallback((event) => {
        if (!startPos.current) return;

        const pos = getTouchPosition(event);
        const deltaX = pos.x - startPos.current.x;
        const deltaY = pos.y - startPos.current.y;
        const deltaTime = Date.now() - startTime.current;

        // Calculate velocity
        const velocityX = deltaX / deltaTime;
        const velocityY = deltaY / deltaTime;

        if (isDragging.current) {
            onDragEnd?.(deltaX, deltaY, velocityX, velocityY);
        } else {
            // Handle tap
            const now = Date.now();
            const timeSinceLastTap = now - lastTap.current;

            if (timeSinceLastTap < 300) {
                onDoubleTap?.(pos);
            } else {
                onTap?.(pos);
            }

            lastTap.current = now;
        }

        startPos.current = null;
        isDragging.current = false;
    }, [onDragEnd, onTap, onDoubleTap]);

    return {
        bind: {
            onTouchStart: handleTouchStart,
            onTouchMove: handleTouchMove,
            onTouchEnd: handleTouchEnd
        }
    };
};

export default useTouchGestures; 