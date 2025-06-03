import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';

/**
 * FocusTrap component
 * 
 * This component traps focus within its children, preventing focus from
 * escaping to elements outside the trap. Useful for modals and dialogs.
 * 
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Child elements to trap focus within
 * @param {boolean} props.active - Whether the focus trap is active
 * @param {Function} props.onEscape - Callback when Escape key is pressed
 * @param {string} props.className - Additional CSS classes
 */
const FocusTrap = ({
    children,
    active = true,
    onEscape,
    className = ''
}) => {
    const containerRef = useRef(null);
    const previousFocusRef = useRef(null);

    useEffect(() => {
        if (!active) return;

        // Store the currently focused element
        previousFocusRef.current = document.activeElement;

        // Find all focusable elements within the trap
        const getFocusableElements = () => {
            const container = containerRef.current;
            if (!container) return [];

            return Array.from(container.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            )).filter(element => {
                const style = window.getComputedStyle(element);
                return style.display !== 'none' && style.visibility !== 'hidden';
            });
        };

        // Handle tab key navigation
        const handleTabKey = (event) => {
            const focusableElements = getFocusableElements();
            if (focusableElements.length === 0) return;

            const firstElement = focusableElements[0];
            const lastElement = focusableElements[focusableElements.length - 1];

            if (event.shiftKey) {
                if (document.activeElement === firstElement) {
                    event.preventDefault();
                    lastElement.focus();
                }
            } else {
                if (document.activeElement === lastElement) {
                    event.preventDefault();
                    firstElement.focus();
                }
            }
        };

        // Handle escape key
        const handleEscapeKey = (event) => {
            if (event.key === 'Escape') {
                onEscape?.(event);
            }
        };

        // Focus the first focusable element
        const focusableElements = getFocusableElements();
        if (focusableElements.length > 0) {
            focusableElements[0].focus();
        }

        // Add event listeners
        document.addEventListener('keydown', handleTabKey);
        document.addEventListener('keydown', handleEscapeKey);

        // Cleanup function
        return () => {
            document.removeEventListener('keydown', handleTabKey);
            document.removeEventListener('keydown', handleEscapeKey);
            
            // Restore focus to the previous element
            if (previousFocusRef.current) {
                previousFocusRef.current.focus();
            }
        };
    }, [active, onEscape]);

    return (
        <div
            ref={containerRef}
            className={`focus-trap ${className}`}
            role="dialog"
            aria-modal="true"
        >
            {children}
        </div>
    );
};

FocusTrap.propTypes = {
    children: PropTypes.node.isRequired,
    active: PropTypes.bool,
    onEscape: PropTypes.func,
    className: PropTypes.string
};

export default FocusTrap; 