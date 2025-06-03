/**
 * FeatureFlag component for conditionally rendering features based on flags.
 * Supports different types of flags and fallback content.
 */

import React from 'react';
import { useAppContext } from '../../context/AppContext';

const FeatureFlag = ({
    flag,
    type = 'boolean',
    fallback = null,
    children
}) => {
    const { featureFlags } = useAppContext();

    const isEnabled = () => {
        if (!featureFlags) return false;

        switch (type) {
            case 'boolean':
                return Boolean(featureFlags[flag]);
            case 'percentage':
                const percentage = featureFlags[flag];
                if (typeof percentage !== 'number') return false;
                return Math.random() * 100 < percentage;
            case 'user':
                const userId = featureFlags[flag];
                if (!userId) return false;
                return userId === 'all' || userId.includes(userId);
            case 'date':
                const date = new Date(featureFlags[flag]);
                return !isNaN(date) && date <= new Date();
            default:
                return false;
        }
    };

    return isEnabled() ? children : fallback;
};

export default FeatureFlag; 