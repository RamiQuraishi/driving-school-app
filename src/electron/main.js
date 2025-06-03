const { app, BrowserWindow } = require('electron');
const path = require('path');
const isDev = process.env.NODE_ENV === 'development';

// Keep a global reference of the window object to prevent garbage collection
let mainWindow;

function createWindow() {
    // Create the browser window
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true
        }
    });

    // Load the index.html file
    if (isDev) {
        // In development, load from React dev server
        mainWindow.loadURL('http://localhost:3000');
        // Open DevTools
        mainWindow.webContents.openDevTools();
    } else {
        // In production, load the built index.html
        mainWindow.loadFile(path.join(__dirname, '../renderer/build/index.html'));
    }

    // Emitted when the window is closed
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

// Create window when Electron has finished initialization
app.whenReady().then(createWindow);

// Quit when all windows are closed
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
}); 