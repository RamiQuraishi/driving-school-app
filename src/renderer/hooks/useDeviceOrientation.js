/**
 * Hook for detecting and handling device orientation changes.
 * Provides orientation data and screen lock functionality.
 */

import { useState, useEffect, useCallback } from 'react';

const useDeviceOrientation = () => {
    const [orientation, setOrientation] = useState({
        alpha: 0, // Z-axis rotation
        beta: 0,  // X-axis rotation
        gamma: 0, // Y-axis rotation
        absolute: false
    });
    const [isSupported, setIsSupported] = useState(false);
    const [isLocked, setIsLocked] = useState(false);

    useEffect(() => {
        // Check if device orientation is supported
        setIsSupported(
            window.DeviceOrientationEvent !== undefined &&
            'ondeviceorientation' in window
        );

        if (!isSupported) return;

        const handleOrientation = (event) => {
            setOrientation({
                alpha: event.alpha,
                beta: event.beta,
                gamma: event.gamma,
                absolute: event.absolute
            });
        };

        window.addEventListener('deviceorientation', handleOrientation);

        return () => {
            window.removeEventListener('deviceorientation', handleOrientation);
        };
    }, [isSupported]);

    const lockOrientation = useCallback(async (type = 'portrait') => {
        if (!isSupported) return false;

        try {
            if (screen.orientation && screen.orientation.lock) {
                await screen.orientation.lock(type);
                setIsLocked(true);
                return true;
            }
            return false;
        } catch (error) {
            console.error('Failed to lock orientation:', error);
            return false;
        }
    }, [isSupported]);

    const unlockOrientation = useCallback(async () => {
        if (!isSupported) return false;

        try {
            if (screen.orientation && screen.orientation.unlock) {
                await screen.orientation.unlock();
                setIsLocked(false);
                return true;
            }
            return false;
        } catch (error) {
            console.error('Failed to unlock orientation:', error);
            return false;
        }
    }, [isSupported]);

    const getOrientationType = useCallback(() => {
        const { beta, gamma } = orientation;
        
        // Determine orientation based on device angles
        if (Math.abs(beta) < 45) {
            return Math.abs(gamma) < 45 ? 'portrait' : 'landscape';
        }
        return 'portrait';
    }, [orientation]);

    return {
        orientation,
        isSupported,
        isLocked,
        lockOrientation,
        unlockOrientation,
        getOrientationType,
        isPortrait: getOrientationType() === 'portrait',
        isLandscape: getOrientationType() === 'landscape'
    };
};

export default useDeviceOrientation; 