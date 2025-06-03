/**
 * Core accessibility utilities for AODA compliance
 */

/**
 * Checks if an element is visible to screen readers
 * @param {HTMLElement} element - The element to check
 * @returns {boolean} - Whether the element is visible to screen readers
 */
export const isVisibleToScreenReader = (element) => {
    if (!element) return false;

    const style = window.getComputedStyle(element);
    return !(
        style.display === 'none' ||
        style.visibility === 'hidden' ||
        style.opacity === '0' ||
        element.getAttribute('aria-hidden') === 'true'
    );
};

/**
 * Gets the accessible name of an element
 * @param {HTMLElement} element - The element to get the name for
 * @returns {string} - The accessible name
 */
export const getAccessibleName = (element) => {
    if (!element) return '';

    // Check for aria-label
    const ariaLabel = element.getAttribute('aria-label');
    if (ariaLabel) return ariaLabel;

    // Check for aria-labelledby
    const ariaLabelledBy = element.getAttribute('aria-labelledby');
    if (ariaLabelledBy) {
        const labels = ariaLabelledBy.split(' ')
            .map(id => document.getElementById(id))
            .filter(Boolean)
            .map(el => el.textContent)
            .join(' ');
        if (labels) return labels;
    }

    // Check for alt text on images
    if (element.tagName === 'IMG') {
        const alt = element.getAttribute('alt');
        if (alt) return alt;
    }

    // Check for label association
    if (element.id) {
        const label = document.querySelector(`label[for="${element.id}"]`);
        if (label) return label.textContent;
    }

    // Fallback to element text content
    return element.textContent.trim();
};

/**
 * Checks if an element has sufficient color contrast
 * @param {string} foreground - The foreground color (hex or rgb)
 * @param {string} background - The background color (hex or rgb)
 * @returns {boolean} - Whether the contrast ratio meets WCAG AA standards
 */
export const hasSufficientContrast = (foreground, background) => {
    const getLuminance = (color) => {
        const rgb = color.match(/\d+/g).map(Number);
        const [r, g, b] = rgb.map(c => {
            c = c / 255;
            return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
        });
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    };

    const l1 = getLuminance(foreground);
    const l2 = getLuminance(background);
    const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    return ratio >= 4.5; // WCAG AA standard for normal text
};

/**
 * Ensures an element is focusable
 * @param {HTMLElement} element - The element to make focusable
 */
export const ensureFocusable = (element) => {
    if (!element) return;

    if (element.tagName === 'DIV' || element.tagName === 'SPAN') {
        element.setAttribute('tabindex', '0');
        element.setAttribute('role', 'button');
    }
};

/**
 * Manages focus trap for modals and dialogs
 * @param {HTMLElement} container - The container element
 * @param {boolean} trap - Whether to trap focus
 */
export const manageFocusTrap = (container, trap) => {
    if (!container) return;

    const focusableElements = container.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];

    if (trap) {
        container.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                if (e.shiftKey && document.activeElement === firstFocusable) {
                    e.preventDefault();
                    lastFocusable.focus();
                } else if (!e.shiftKey && document.activeElement === lastFocusable) {
                    e.preventDefault();
                    firstFocusable.focus();
                }
            }
        });
    }
};

/**
 * Checks if an element is in the viewport
 * @param {HTMLElement} element - The element to check
 * @returns {boolean} - Whether the element is in the viewport
 */
export const isInViewport = (element) => {
    if (!element) return false;

    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
};

/**
 * Scrolls an element into view with smooth behavior
 * @param {HTMLElement} element - The element to scroll into view
 * @param {Object} options - Scroll options
 */
export const scrollIntoView = (element, options = {}) => {
    if (!element) return;

    const defaultOptions = {
        behavior: 'smooth',
        block: 'nearest',
        inline: 'nearest'
    };

    element.scrollIntoView({ ...defaultOptions, ...options });
};

/**
 * Checks if an element has valid ARIA attributes
 * @param {HTMLElement} element - The element to check
 * @returns {boolean} - Whether the element has valid ARIA attributes
 */
export const hasValidAriaAttributes = (element) => {
    if (!element) return false;

    const ariaAttributes = element.getAttributeNames()
        .filter(name => name.startsWith('aria-'));

    return ariaAttributes.every(attr => {
        const value = element.getAttribute(attr);
        return value !== null && value !== '';
    });
}; 