/**
 * Main Process
 * 
 * This module serves as the main process for the Electron application.
 * It handles window management and IPC communication.
 * 
 * Author: Rami Drive School
 * Date: 2024
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

// Global window reference
let mainWindow = null;
let pythonProcess = null;

// Start Python backend
function startPythonBackend() {
    const pythonPath = process.platform === 'win32' ? 'python' : 'python3';
    const scriptPath = path.join(__dirname, '..', 'ontario_driving_school_manager', '__main__.py');
    
    pythonProcess = spawn(pythonPath, [scriptPath], {
        stdio: 'pipe'
    });
    
    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python stdout: ${data}`);
    });
    
    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python stderr: ${data}`);
    });
    
    pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code ${code}`);
    });
}

// Create main window
function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')
        }
    });
    
    // Load app
    if (process.env.NODE_ENV === 'development') {
        mainWindow.loadURL('http://localhost:3000');
        mainWindow.webContents.openDevTools();
    } else {
        mainWindow.loadFile(path.join(__dirname, '..', 'renderer', 'index.html'));
    }
    
    // Handle window close
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

// App ready
app.whenReady().then(() => {
    startPythonBackend();
    createWindow();
    
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

// App quit
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        if (pythonProcess) {
            pythonProcess.kill();
        }
        app.quit();
    }
});

// Handle IPC messages
ipcMain.handle('check-health', async () => {
    try {
        const response = await fetch('http://localhost:8000/health');
        return await response.json();
    } catch (error) {
        console.error('Health check failed:', error);
        throw error;
    }
}); 