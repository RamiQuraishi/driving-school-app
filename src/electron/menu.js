/**
 * Application menu configuration.
 * Defines the main menu structure and keyboard shortcuts.
 */

const { Menu, app, shell } = require('electron');
const isDev = process.env.NODE_ENV === 'development';

class AppMenu {
    constructor() {
        this.menu = null;
        this.createMenu();
    }

    /**
     * Create the application menu
     */
    createMenu() {
        const template = [
            {
                label: 'File',
                submenu: [
                    {
                        label: 'New Window',
                        accelerator: 'CmdOrCtrl+N',
                        click: () => {
                            // Handle new window creation
                        }
                    },
                    { type: 'separator' },
                    {
                        label: 'Exit',
                        accelerator: 'CmdOrCtrl+Q',
                        click: () => app.quit()
                    }
                ]
            },
            {
                label: 'Edit',
                submenu: [
                    { role: 'undo' },
                    { role: 'redo' },
                    { type: 'separator' },
                    { role: 'cut' },
                    { role: 'copy' },
                    { role: 'paste' },
                    { role: 'delete' },
                    { type: 'separator' },
                    { role: 'selectAll' }
                ]
            },
            {
                label: 'View',
                submenu: [
                    { role: 'reload' },
                    { role: 'forceReload' },
                    { role: 'toggleDevTools', visible: isDev },
                    { type: 'separator' },
                    { role: 'resetZoom' },
                    { role: 'zoomIn' },
                    { role: 'zoomOut' },
                    { type: 'separator' },
                    { role: 'togglefullscreen' }
                ]
            },
            {
                label: 'Window',
                submenu: [
                    { role: 'minimize' },
                    { role: 'zoom' },
                    { type: 'separator' },
                    { role: 'front' },
                    { type: 'separator' },
                    { role: 'close' }
                ]
            },
            {
                label: 'Help',
                submenu: [
                    {
                        label: 'Documentation',
                        click: () => shell.openExternal('https://docs.example.com')
                    },
                    {
                        label: 'Report Issue',
                        click: () => shell.openExternal('https://github.com/example/repo/issues')
                    },
                    { type: 'separator' },
                    {
                        label: 'About',
                        click: () => {
                            // Show about dialog
                        }
                    }
                ]
            }
        ];

        // Add development menu items
        if (isDev) {
            template.push({
                label: 'Development',
                submenu: [
                    {
                        label: 'Toggle DevTools',
                        accelerator: 'F12',
                        click: (item, focusedWindow) => {
                            if (focusedWindow) {
                                focusedWindow.webContents.toggleDevTools();
                            }
                        }
                    },
                    {
                        label: 'Reload',
                        accelerator: 'CmdOrCtrl+R',
                        click: (item, focusedWindow) => {
                            if (focusedWindow) {
                                focusedWindow.reload();
                            }
                        }
                    }
                ]
            });
        }

        this.menu = Menu.buildFromTemplate(template);
        Menu.setApplicationMenu(this.menu);
    }

    /**
     * Update menu items based on application state
     * @param {Object} state - Application state
     */
    updateMenu(state) {
        // Update menu items based on state
        // This can be used to enable/disable menu items
        // or update their labels based on application state
    }
}

module.exports = new AppMenu(); 