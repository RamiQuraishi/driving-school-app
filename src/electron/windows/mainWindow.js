/**
 * Main window handler for the Electron application.
 * This module manages the main application window with security and performance optimizations.
 */

const { BrowserWindow, screen } = require('electron');
const path = require('path');
const isDev = process.env.NODE_ENV === 'development';

class MainWindow {
    constructor() {
        this.window = null;
        this.isQuitting = false;
    }

    create() {
        const { width, height } = screen.getPrimaryDisplay().workAreaSize;
        
        // Create the browser window with security-focused options
        this.window = new BrowserWindow({
            width: Math.min(1200, width),
            height: Math.min(800, height),
            minWidth: 800,
            minHeight: 600,
            center: true,
            show: false, // Don't show until ready
            webPreferences: {
                nodeIntegration: false,
                contextIsolation: true,
                sandbox: true,
                preload: path.join(__dirname, '../preload.js'),
                webSecurity: true,
                allowRunningInsecureContent: false,
                spellcheck: true,
                enableWebSQL: false,
                backgroundThrottling: false, // Prevent throttling when in background
            },
            backgroundColor: '#ffffff',
            titleBarStyle: 'hiddenInset',
            frame: process.platform !== 'darwin',
            trafficLightPosition: { x: 20, y: 20 },
        });

        // Load the app
        if (isDev) {
            this.window.loadURL('http://localhost:3000');
            this.window.webContents.openDevTools();
        } else {
            this.window.loadFile(path.join(__dirname, '../../build/index.html'));
        }

        // Security headers
        this.window.webContents.session.webRequest.onHeadersReceived((details, callback) => {
            callback({
                responseHeaders: {
                    ...details.responseHeaders,
                    'Content-Security-Policy': [
                        "default-src 'self'",
                        "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
                        "style-src 'self' 'unsafe-inline'",
                        "img-src 'self' data: https:",
                        "connect-src 'self' https:",
                        "font-src 'self'",
                        "object-src 'none'",
                        "media-src 'self'",
                        "frame-src 'none'",
                    ].join('; '),
                    'X-Content-Type-Options': ['nosniff'],
                    'X-Frame-Options': ['DENY'],
                    'X-XSS-Protection': ['1; mode=block'],
                    'Referrer-Policy': ['strict-origin-when-cross-origin'],
                    'Permissions-Policy': [
                        'camera=()',
                        'microphone=()',
                        'geolocation=()',
                        'midi=()',
                        'sync-xhr=()',
                        'accelerometer=()',
                        'gyroscope=()',
                        'magnetometer=()',
                        'payment=()',
                        'usb=()',
                    ].join(', '),
                },
            });
        });

        // Window event handlers
        this.window.on('ready-to-show', () => {
            this.window.show();
            this.window.focus();
        });

        this.window.on('close', (event) => {
            if (!this.isQuitting) {
                event.preventDefault();
                this.window.hide();
            }
        });

        // Handle window state
        this.window.on('maximize', () => {
            this.window.webContents.send('window-state-changed', 'maximized');
        });

        this.window.on('unmaximize', () => {
            this.window.webContents.send('window-state-changed', 'normal');
        });

        // Handle window focus
        this.window.on('focus', () => {
            this.window.webContents.send('window-focus-changed', true);
        });

        this.window.on('blur', () => {
            this.window.webContents.send('window-focus-changed', false);
        });

        // Handle window errors
        this.window.webContents.on('crashed', () => {
            // Handle window crash
            require('../crash-reporter').reportCrash('main-window');
        });

        // Handle navigation
        this.window.webContents.on('will-navigate', (event, url) => {
            // Prevent navigation to external URLs
            if (!url.startsWith('file://') && !url.startsWith('http://localhost')) {
                event.preventDefault();
            }
        });

        return this.window;
    }

    show() {
        if (this.window) {
            this.window.show();
            this.window.focus();
        }
    }

    hide() {
        if (this.window) {
            this.window.hide();
        }
    }

    close() {
        this.isQuitting = true;
        if (this.window) {
            this.window.close();
        }
    }

    toggleDevTools() {
        if (this.window) {
            this.window.webContents.toggleDevTools();
        }
    }

    reload() {
        if (this.window) {
            this.window.reload();
        }
    }
}

module.exports = new MainWindow(); 