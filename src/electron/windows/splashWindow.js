/**
 * Splash window handler for the Electron application.
 * This module manages the splash screen with loading animation and progress tracking.
 */

const { BrowserWindow, screen } = require('electron');
const path = require('path');
const isDev = process.env.NODE_ENV === 'development';

class SplashWindow {
    constructor() {
        this.window = null;
        this.progress = 0;
    }

    create() {
        const { width, height } = screen.getPrimaryDisplay().workAreaSize;
        const splashWidth = 400;
        const splashHeight = 300;

        this.window = new BrowserWindow({
            width: splashWidth,
            height: splashHeight,
            center: true,
            frame: false,
            transparent: true,
            resizable: false,
            alwaysOnTop: true,
            show: false,
            webPreferences: {
                nodeIntegration: false,
                contextIsolation: true,
                sandbox: true,
                preload: path.join(__dirname, '../preload.js'),
            },
        });

        // Load splash screen
        if (isDev) {
            this.window.loadURL('http://localhost:3000/splash');
        } else {
            this.window.loadFile(path.join(__dirname, '../../build/splash.html'));
        }

        // Show window when ready
        this.window.on('ready-to-show', () => {
            this.window.show();
        });

        // Prevent navigation
        this.window.webContents.on('will-navigate', (event) => {
            event.preventDefault();
        });

        return this.window;
    }

    /**
     * Update loading progress
     * @param {number} progress - Progress value between 0 and 100
     */
    updateProgress(progress) {
        this.progress = Math.min(100, Math.max(0, progress));
        if (this.window && !this.window.isDestroyed()) {
            this.window.webContents.send('splash-progress', this.progress);
        }
    }

    /**
     * Set loading message
     * @param {string} message - Loading message to display
     */
    setMessage(message) {
        if (this.window && !this.window.isDestroyed()) {
            this.window.webContents.send('splash-message', message);
        }
    }

    /**
     * Close the splash window
     */
    close() {
        if (this.window && !this.window.isDestroyed()) {
            this.window.close();
        }
    }

    /**
     * Check if splash window is visible
     * @returns {boolean} True if window is visible
     */
    isVisible() {
        return this.window && !this.window.isDestroyed() && this.window.isVisible();
    }
}

module.exports = new SplashWindow(); 