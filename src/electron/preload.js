/**
 * Preload Script
 * 
 * This module provides a secure bridge between the renderer process and main process.
 * It exposes specific APIs to the renderer process.
 * 
 * Author: Rami Drive School
 * Date: 2024
 */

const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld(
    'api', {
        // Health check
        checkHealth: () => ipcRenderer.invoke('check-health'),
        
        // Student operations
        getStudents: () => ipcRenderer.invoke('get-students'),
        getStudent: (id) => ipcRenderer.invoke('get-student', id),
        createStudent: (data) => ipcRenderer.invoke('create-student', data),
        updateStudent: (id, data) => ipcRenderer.invoke('update-student', id, data),
        deleteStudent: (id) => ipcRenderer.invoke('delete-student', id),
        
        // Instructor operations
        getInstructors: () => ipcRenderer.invoke('get-instructors'),
        getInstructor: (id) => ipcRenderer.invoke('get-instructor', id),
        createInstructor: (data) => ipcRenderer.invoke('create-instructor', data),
        updateInstructor: (id, data) => ipcRenderer.invoke('update-instructor', id, data),
        deleteInstructor: (id) => ipcRenderer.invoke('delete-instructor', id),
        
        // Lesson operations
        getLessons: () => ipcRenderer.invoke('get-lessons'),
        getLesson: (id) => ipcRenderer.invoke('get-lesson', id),
        createLesson: (data) => ipcRenderer.invoke('create-lesson', data),
        updateLesson: (id, data) => ipcRenderer.invoke('update-lesson', id, data),
        deleteLesson: (id) => ipcRenderer.invoke('delete-lesson', id),
        
        // Payment operations
        getPayments: () => ipcRenderer.invoke('get-payments'),
        getPayment: (id) => ipcRenderer.invoke('get-payment', id),
        createPayment: (data) => ipcRenderer.invoke('create-payment', data),
        updatePayment: (id, data) => ipcRenderer.invoke('update-payment', id, data),
        deletePayment: (id) => ipcRenderer.invoke('delete-payment', id),
        
        // Analytics operations
        trackEvent: (event) => ipcRenderer.invoke('track-event', event),
        
        // Sync operations
        syncData: () => ipcRenderer.invoke('sync-data'),
        getSyncStatus: () => ipcRenderer.invoke('get-sync-status'),
        
        // Export operations
        exportData: (type) => ipcRenderer.invoke('export-data', type),
        
        // Backup operations
        createBackup: () => ipcRenderer.invoke('create-backup'),
        restoreBackup: (id) => ipcRenderer.invoke('restore-backup', id)
    }
); 