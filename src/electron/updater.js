/**
 * Auto-updater module for handling application updates.
 * Manages update checks, downloads, and installations.
 */

const { autoUpdater } = require('electron-updater');
const { app, dialog } = require('electron');
const logManager = require('./log-manager');

class Updater {
    constructor() {
        this.initialized = false;
        this.updateAvailable = false;
        this.updateDownloaded = false;
        this.initialize();
    }

    /**
     * Initialize the auto-updater
     */
    initialize() {
        if (this.initialized) {
            return;
        }

        // Configure auto-updater
        autoUpdater.autoDownload = false;
        autoUpdater.autoInstallOnAppQuit = true;

        // Set up event handlers
        autoUpdater.on('checking-for-update', () => {
            logManager.log('updater', 'Checking for updates...');
        });

        autoUpdater.on('update-available', (info) => {
            this.updateAvailable = true;
            logManager.log('updater', 'Update available', { version: info.version });
            this.showUpdateAvailableDialog(info);
        });

        autoUpdater.on('update-not-available', () => {
            this.updateAvailable = false;
            logManager.log('updater', 'No updates available');
        });

        autoUpdater.on('error', (error) => {
            logManager.error('updater', 'Update error', error);
            this.showErrorDialog(error);
        });

        autoUpdater.on('download-progress', (progress) => {
            logManager.log('updater', 'Download progress', {
                percent: progress.percent,
                transferred: progress.transferred,
                total: progress.total
            });
        });

        autoUpdater.on('update-downloaded', (info) => {
            this.updateDownloaded = true;
            logManager.log('updater', 'Update downloaded', { version: info.version });
            this.showUpdateReadyDialog(info);
        });

        this.initialized = true;
    }

    /**
     * Check for updates
     * @returns {Promise<boolean>} - Whether an update is available
     */
    async checkForUpdates() {
        try {
            if (!this.initialized) {
                this.initialize();
            }

            const result = await autoUpdater.checkForUpdates();
            return result !== null;
        } catch (error) {
            logManager.error('updater', 'Error checking for updates', error);
            throw error;
        }
    }

    /**
     * Download available update
     * @returns {Promise<void>}
     */
    async downloadUpdate() {
        try {
            if (!this.updateAvailable) {
                throw new Error('No update available');
            }

            await autoUpdater.downloadUpdate();
        } catch (error) {
            logManager.error('updater', 'Error downloading update', error);
            throw error;
        }
    }

    /**
     * Install downloaded update
     */
    installUpdate() {
        if (!this.updateDownloaded) {
            throw new Error('No update downloaded');
        }

        autoUpdater.quitAndInstall();
    }

    /**
     * Show update available dialog
     * @param {Object} info - Update info
     */
    showUpdateAvailableDialog(info) {
        dialog.showMessageBox({
            type: 'info',
            title: 'Update Available',
            message: `Version ${info.version} is available for download.`,
            detail: 'Would you like to download it now?',
            buttons: ['Download', 'Later'],
            defaultId: 0,
            cancelId: 1
        }).then(({ response }) => {
            if (response === 0) {
                this.downloadUpdate();
            }
        });
    }

    /**
     * Show update ready dialog
     * @param {Object} info - Update info
     */
    showUpdateReadyDialog(info) {
        dialog.showMessageBox({
            type: 'info',
            title: 'Update Ready',
            message: `Version ${info.version} has been downloaded.`,
            detail: 'Would you like to install it now?',
            buttons: ['Install', 'Later'],
            defaultId: 0,
            cancelId: 1
        }).then(({ response }) => {
            if (response === 0) {
                this.installUpdate();
            }
        });
    }

    /**
     * Show error dialog
     * @param {Error} error - Error object
     */
    showErrorDialog(error) {
        dialog.showErrorBox(
            'Update Error',
            `An error occurred while checking for updates: ${error.message}`
        );
    }
}

module.exports = new Updater(); 