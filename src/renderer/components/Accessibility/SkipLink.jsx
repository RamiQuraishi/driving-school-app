import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

/**
 * SkipLink component
 * 
 * This component provides a hidden link that becomes visible when focused,
 * allowing keyboard users to skip navigation and jump directly to the main content.
 * 
 * @param {Object} props - Component props
 * @param {string} props.targetId - ID of the main content element to skip to
 * @param {string} props.text - Text to display in the skip link
 * @param {string} props.className - Additional CSS classes
 */
const SkipLink = ({
    targetId = 'main-content',
    text = 'Skip to main content',
    className = ''
}) => {
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        // Ensure the target element exists
        const targetElement = document.getElementById(targetId);
        if (!targetElement) {
            console.warn(`SkipLink: Target element with ID "${targetId}" not found.`);
        }
    }, [targetId]);

    const handleFocus = () => setIsVisible(true);
    const handleBlur = () => setIsVisible(false);

    return (
        <a
            href={`#${targetId}`}
            className={`skip-link ${isVisible ? 'visible' : ''} ${className}`}
            onFocus={handleFocus}
            onBlur={handleBlur}
            onClick={(e) => {
                e.preventDefault();
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    targetElement.tabIndex = -1;
                    targetElement.focus();
                    // Remove tabIndex after focus
                    setTimeout(() => {
                        targetElement.removeAttribute('tabindex');
                    }, 100);
                }
            }}
        >
            {text}
        </a>
    );
};

SkipLink.propTypes = {
    targetId: PropTypes.string,
    text: PropTypes.string,
    className: PropTypes.string
};

export default SkipLink; 