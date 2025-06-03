/**
 * Hook for detecting mobile devices and screen sizes.
 * Provides responsive breakpoints and device type detection.
 */

import { useState, useEffect } from 'react';
import { useTheme } from '@mui/material';

const useMobileDetection = () => {
    const theme = useTheme();
    const [isMobile, setIsMobile] = useState(false);
    const [isTablet, setIsTablet] = useState(false);
    const [isDesktop, setIsDesktop] = useState(false);
    const [orientation, setOrientation] = useState('portrait');

    useEffect(() => {
        const checkDevice = () => {
            const width = window.innerWidth;
            const height = window.innerHeight;

            // Check orientation
            setOrientation(width > height ? 'landscape' : 'portrait');

            // Check device type based on breakpoints
            setIsMobile(width < theme.breakpoints.values.sm);
            setIsTablet(
                width >= theme.breakpoints.values.sm &&
                width < theme.breakpoints.values.md
            );
            setIsDesktop(width >= theme.breakpoints.values.md);
        };

        // Initial check
        checkDevice();

        // Add event listeners
        window.addEventListener('resize', checkDevice);
        window.addEventListener('orientationchange', checkDevice);

        // Cleanup
        return () => {
            window.removeEventListener('resize', checkDevice);
            window.removeEventListener('orientationchange', checkDevice);
        };
    }, [theme.breakpoints.values.sm, theme.breakpoints.values.md]);

    return {
        isMobile,
        isTablet,
        isDesktop,
        orientation,
        isLandscape: orientation === 'landscape',
        isPortrait: orientation === 'portrait'
    };
};

export default useMobileDetection; 