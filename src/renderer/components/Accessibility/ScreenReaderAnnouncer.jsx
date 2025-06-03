import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';

/**
 * ScreenReaderAnnouncer component
 * 
 * This component provides a way to announce dynamic content to screen readers
 * without affecting the visual layout of the page.
 * 
 * @param {Object} props - Component props
 * @param {string} props.message - The message to announce
 * @param {string} props.politeness - The politeness level ('polite' or 'assertive')
 * @param {string} props.className - Additional CSS classes
 */
const ScreenReaderAnnouncer = ({ message, politeness = 'polite', className = '' }) => {
    const announcerRef = useRef(null);

    useEffect(() => {
        if (message && announcerRef.current) {
            // Clear previous message
            announcerRef.current.textContent = '';
            
            // Force a reflow to ensure the announcement is triggered
            void announcerRef.current.offsetHeight;
            
            // Set the new message
            announcerRef.current.textContent = message;
        }
    }, [message]);

    return (
        <div
            ref={announcerRef}
            className={`sr-only ${className}`}
            aria-live={politeness}
            aria-atomic="true"
            role="status"
        />
    );
};

ScreenReaderAnnouncer.propTypes = {
    message: PropTypes.string.isRequired,
    politeness: PropTypes.oneOf(['polite', 'assertive']),
    className: PropTypes.string
};

export default ScreenReaderAnnouncer; 