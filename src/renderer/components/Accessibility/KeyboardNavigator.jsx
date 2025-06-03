import React, { useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';

/**
 * KeyboardNavigator component
 * 
 * This component provides keyboard navigation and shortcut functionality
 * for improved accessibility.
 * 
 * @param {Object} props - Component props
 * @param {Object} props.shortcuts - Object mapping key combinations to handlers
 * @param {boolean} props.enabled - Whether keyboard navigation is enabled
 * @param {Function} props.onShortcut - Callback when a shortcut is triggered
 * @param {string} props.className - Additional CSS classes
 */
const KeyboardNavigator = ({
    shortcuts = {},
    enabled = true,
    onShortcut,
    className = ''
}) => {
    const handleKeyDown = useCallback((event) => {
        if (!enabled) return;

        // Get the key combination
        const key = event.key.toLowerCase();
        const ctrlKey = event.ctrlKey;
        const altKey = event.altKey;
        const shiftKey = event.shiftKey;
        const metaKey = event.metaKey;

        // Create the key combination string
        const combination = [
            ctrlKey && 'ctrl',
            altKey && 'alt',
            shiftKey && 'shift',
            metaKey && 'meta',
            key
        ].filter(Boolean).join('+');

        // Check if this combination is registered
        const handler = shortcuts[combination];
        if (handler) {
            event.preventDefault();
            event.stopPropagation();
            handler(event);
            onShortcut?.(combination, event);
        }
    }, [enabled, shortcuts, onShortcut]);

    useEffect(() => {
        if (enabled) {
            document.addEventListener('keydown', handleKeyDown);
            return () => document.removeEventListener('keydown', handleKeyDown);
        }
    }, [enabled, handleKeyDown]);

    // Common keyboard navigation patterns
    const handleArrowNavigation = useCallback((event) => {
        if (!enabled) return;

        const target = event.target;
        const isInput = target.tagName === 'INPUT' || target.tagName === 'TEXTAREA';
        
        // Don't handle arrow keys in input fields
        if (isInput) return;

        const focusableElements = document.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        const currentIndex = Array.from(focusableElements).indexOf(document.activeElement);

        let nextIndex;
        switch (event.key) {
            case 'ArrowDown':
            case 'ArrowRight':
                nextIndex = (currentIndex + 1) % focusableElements.length;
                break;
            case 'ArrowUp':
            case 'ArrowLeft':
                nextIndex = (currentIndex - 1 + focusableElements.length) % focusableElements.length;
                break;
            default:
                return;
        }

        event.preventDefault();
        focusableElements[nextIndex]?.focus();
    }, [enabled]);

    useEffect(() => {
        if (enabled) {
            document.addEventListener('keydown', handleArrowNavigation);
            return () => document.removeEventListener('keydown', handleArrowNavigation);
        }
    }, [enabled, handleArrowNavigation]);

    return (
        <div
            className={`keyboard-navigator ${className}`}
            role="application"
            aria-label="Keyboard Navigation"
        />
    );
};

KeyboardNavigator.propTypes = {
    shortcuts: PropTypes.objectOf(PropTypes.func),
    enabled: PropTypes.bool,
    onShortcut: PropTypes.func,
    className: PropTypes.string
};

export default KeyboardNavigator; 