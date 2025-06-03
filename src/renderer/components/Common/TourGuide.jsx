/**
 * TourGuide component for providing interactive onboarding tours.
 * Uses react-joyride for step-by-step feature introductions.
 */

import React, { useState, useEffect } from 'react';
import Joyride, { STATUS } from 'react-joyride';
import { useTheme } from '@mui/material';
import { useAppContext } from '../../context/AppContext';

const TourGuide = () => {
    const theme = useTheme();
    const { user } = useAppContext();
    const [steps, setSteps] = useState([]);
    const [run, setRun] = useState(false);

    useEffect(() => {
        // Define tour steps
        const tourSteps = [
            {
                target: '.app-title',
                content: 'Welcome to Rami Drive School! Let\'s take a quick tour.',
                placement: 'bottom',
                disableBeacon: true
            },
            {
                target: '.sidebar-menu',
                content: 'Access all features from this menu.',
                placement: 'right'
            },
            {
                target: '.quick-actions',
                content: 'Quick actions for common tasks.',
                placement: 'left'
            },
            {
                target: '.notification-center',
                content: 'Stay updated with notifications.',
                placement: 'bottom'
            },
            {
                target: '.user-profile',
                content: 'Manage your profile and settings.',
                placement: 'bottom'
            }
        ];

        setSteps(tourSteps);

        // Check if user needs tour
        const hasSeenTour = localStorage.getItem('hasSeenTour');
        if (!hasSeenTour && user) {
            setRun(true);
        }
    }, [user]);

    const handleJoyrideCallback = (data) => {
        const { status } = data;

        if ([STATUS.FINISHED, STATUS.SKIPPED].includes(status)) {
            // Save tour completion
            localStorage.setItem('hasSeenTour', 'true');
            setRun(false);
        }
    };

    const styles = {
        options: {
            primaryColor: theme.palette.primary.main,
            zIndex: theme.zIndex.modal + 1
        },
        tooltip: {
            backgroundColor: theme.palette.background.paper,
            color: theme.palette.text.primary,
            borderRadius: theme.shape.borderRadius,
            padding: theme.spacing(2)
        },
        buttonNext: {
            backgroundColor: theme.palette.primary.main,
            color: theme.palette.primary.contrastText
        },
        buttonBack: {
            color: theme.palette.text.secondary
        }
    };

    return (
        <Joyride
            steps={steps}
            run={run}
            continuous
            showProgress
            showSkipButton
            styles={styles}
            callback={handleJoyrideCallback}
            locale={{
                back: 'Back',
                close: 'Close',
                last: 'Finish',
                next: 'Next',
                skip: 'Skip Tour'
            }}
        />
    );
};

export default TourGuide; 