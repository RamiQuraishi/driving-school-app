/**
 * WCAG compliance validation utilities
 */

import { hasSufficientContrast } from './accessibility';

/**
 * WCAG 2.1 Level AA validation rules
 */
const WCAG_RULES = {
    // 1.1.1 Non-text Content
    hasAltText: (element) => {
        if (element.tagName === 'IMG') {
            return element.hasAttribute('alt');
        }
        return true;
    },

    // 1.2.1 Audio-only and Video-only (Prerecorded)
    hasTranscript: (element) => {
        if (element.tagName === 'AUDIO' || element.tagName === 'VIDEO') {
            return element.hasAttribute('aria-describedby') || 
                   element.querySelector('track[kind="descriptions"]');
        }
        return true;
    },

    // 1.3.1 Info and Relationships
    hasValidStructure: (element) => {
        const hasHeading = element.querySelector('h1, h2, h3, h4, h5, h6');
        const hasList = element.querySelector('ul, ol');
        const hasTable = element.querySelector('table');
        
        if (hasTable) {
            const hasCaption = element.querySelector('caption');
            const hasTh = element.querySelector('th');
            return hasCaption && hasTh;
        }
        
        return true;
    },

    // 1.4.1 Use of Color
    notColorAlone: (element) => {
        const style = window.getComputedStyle(element);
        const color = style.color;
        const backgroundColor = style.backgroundColor;
        
        return hasSufficientContrast(color, backgroundColor);
    },

    // 1.4.3 Contrast (Minimum)
    hasMinimumContrast: (element) => {
        const style = window.getComputedStyle(element);
        return hasSufficientContrast(style.color, style.backgroundColor);
    },

    // 2.1.1 Keyboard
    isKeyboardAccessible: (element) => {
        if (element.tagName === 'A' || element.tagName === 'BUTTON') {
            return true;
        }
        return element.hasAttribute('tabindex');
    },

    // 2.4.4 Link Purpose (In Context)
    hasDescriptiveLink: (element) => {
        if (element.tagName === 'A') {
            const text = element.textContent.trim();
            const ariaLabel = element.getAttribute('aria-label');
            return text.length > 0 || ariaLabel;
        }
        return true;
    },

    // 2.4.6 Headings and Labels
    hasDescriptiveHeading: (element) => {
        if (element.tagName.match(/^H[1-6]$/)) {
            return element.textContent.trim().length > 0;
        }
        return true;
    },

    // 3.2.1 On Focus
    hasFocusHandler: (element) => {
        return element.hasAttribute('onfocus') || 
               element.hasAttribute('onblur') ||
               element.hasAttribute('tabindex');
    },

    // 3.2.2 On Input
    hasInputHandler: (element) => {
        if (element.tagName === 'INPUT' || element.tagName === 'SELECT' || element.tagName === 'TEXTAREA') {
            return element.hasAttribute('onchange') || 
                   element.hasAttribute('oninput');
        }
        return true;
    }
};

/**
 * Validates an element against WCAG 2.1 Level AA guidelines
 * @param {HTMLElement} element - The element to validate
 * @returns {Object} - Validation results
 */
export const validateWCAG = (element) => {
    if (!element) return { valid: false, errors: ['Element is null or undefined'] };

    const results = {
        valid: true,
        errors: [],
        warnings: []
    };

    // Check each WCAG rule
    Object.entries(WCAG_RULES).forEach(([rule, validator]) => {
        try {
            const isValid = validator(element);
            if (!isValid) {
                results.valid = false;
                results.errors.push(`Failed WCAG rule: ${rule}`);
            }
        } catch (error) {
            results.warnings.push(`Error checking rule ${rule}: ${error.message}`);
        }
    });

    return results;
};

/**
 * Validates a page against WCAG 2.1 Level AA guidelines
 * @param {HTMLElement} root - The root element to start validation from
 * @returns {Object} - Validation results
 */
export const validatePage = (root = document.body) => {
    const results = {
        valid: true,
        errors: [],
        warnings: [],
        elements: new Map()
    };

    // Get all interactive and content elements
    const elements = root.querySelectorAll(
        'a, button, input, select, textarea, img, video, audio, [role], [aria-*]'
    );

    elements.forEach(element => {
        const elementResults = validateWCAG(element);
        if (!elementResults.valid) {
            results.valid = false;
            results.errors.push(...elementResults.errors);
            results.elements.set(element, elementResults);
        }
        if (elementResults.warnings.length > 0) {
            results.warnings.push(...elementResults.warnings);
        }
    });

    return results;
};

/**
 * Generates a WCAG compliance report
 * @param {Object} results - Validation results from validatePage
 * @returns {string} - HTML report
 */
export const generateWCAGReport = (results) => {
    const report = document.createElement('div');
    report.className = 'wcag-report';

    const summary = document.createElement('div');
    summary.className = 'wcag-summary';
    summary.innerHTML = `
        <h2>WCAG 2.1 Level AA Compliance Report</h2>
        <p>Overall Status: ${results.valid ? 'Compliant' : 'Non-compliant'}</p>
        <p>Total Errors: ${results.errors.length}</p>
        <p>Total Warnings: ${results.warnings.length}</p>
    `;
    report.appendChild(summary);

    if (results.errors.length > 0) {
        const errorsList = document.createElement('div');
        errorsList.className = 'wcag-errors';
        errorsList.innerHTML = `
            <h3>Errors</h3>
            <ul>
                ${results.errors.map(error => `<li>${error}</li>`).join('')}
            </ul>
        `;
        report.appendChild(errorsList);
    }

    if (results.warnings.length > 0) {
        const warningsList = document.createElement('div');
        warningsList.className = 'wcag-warnings';
        warningsList.innerHTML = `
            <h3>Warnings</h3>
            <ul>
                ${results.warnings.map(warning => `<li>${warning}</li>`).join('')}
            </ul>
        `;
        report.appendChild(warningsList);
    }

    return report.outerHTML;
}; 