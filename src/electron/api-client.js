/**
 * API Client
 * 
 * This module provides a client for the local FastAPI server.
 * It handles API requests and responses.
 * 
 * Author: Rami Drive School
 * Date: 2024
 */

const { API_BASE_URL, API_VERSION } = require('../shared/constants');

class ApiClient {
    constructor() {
        this.baseUrl = `${API_BASE_URL}/${API_VERSION}`;
    }
    
    // Health check
    async checkHealth() {
        return this.get('/health');
    }
    
    // Student operations
    async getStudents() {
        return this.get('/students');
    }
    
    async getStudent(id) {
        return this.get(`/students/${id}`);
    }
    
    async createStudent(data) {
        return this.post('/students', data);
    }
    
    async updateStudent(id, data) {
        return this.put(`/students/${id}`, data);
    }
    
    async deleteStudent(id) {
        return this.delete(`/students/${id}`);
    }
    
    // Instructor operations
    async getInstructors() {
        return this.get('/instructors');
    }
    
    async getInstructor(id) {
        return this.get(`/instructors/${id}`);
    }
    
    async createInstructor(data) {
        return this.post('/instructors', data);
    }
    
    async updateInstructor(id, data) {
        return this.put(`/instructors/${id}`, data);
    }
    
    async deleteInstructor(id) {
        return this.delete(`/instructors/${id}`);
    }
    
    // Lesson operations
    async getLessons() {
        return this.get('/lessons');
    }
    
    async getLesson(id) {
        return this.get(`/lessons/${id}`);
    }
    
    async createLesson(data) {
        return this.post('/lessons', data);
    }
    
    async updateLesson(id, data) {
        return this.put(`/lessons/${id}`, data);
    }
    
    async deleteLesson(id) {
        return this.delete(`/lessons/${id}`);
    }
    
    // Payment operations
    async getPayments() {
        return this.get('/payments');
    }
    
    async getPayment(id) {
        return this.get(`/payments/${id}`);
    }
    
    async createPayment(data) {
        return this.post('/payments', data);
    }
    
    async updatePayment(id, data) {
        return this.put(`/payments/${id}`, data);
    }
    
    async deletePayment(id) {
        return this.delete(`/payments/${id}`);
    }
    
    // Analytics operations
    async trackEvent(event) {
        return this.post('/analytics/events', event);
    }
    
    // Sync operations
    async syncData() {
        return this.post('/sync');
    }
    
    async getSyncStatus() {
        return this.get('/sync/status');
    }
    
    // Export operations
    async exportData(type) {
        return this.get(`/export/${type}`);
    }
    
    // Backup operations
    async createBackup() {
        return this.post('/backups');
    }
    
    async restoreBackup(id) {
        return this.post(`/backups/${id}/restore`);
    }
    
    // HTTP methods
    async get(endpoint) {
        const response = await fetch(`${this.baseUrl}${endpoint}`);
        return this.handleResponse(response);
    }
    
    async post(endpoint, data) {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return this.handleResponse(response);
    }
    
    async put(endpoint, data) {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return this.handleResponse(response);
    }
    
    async delete(endpoint) {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'DELETE'
        });
        return this.handleResponse(response);
    }
    
    // Response handler
    async handleResponse(response) {
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API request failed');
        }
        
        return response.json();
    }
}

module.exports = new ApiClient(); 