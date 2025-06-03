/**
 * API bridge for connecting with the local FastAPI backend.
 * Handles HTTP requests and WebSocket streams.
 */

const axios = require('axios');
const WebSocket = require('ws');
const logManager = require('../log-manager');
const security = require('./security');

class ApiBridge {
    constructor() {
        this.baseUrl = process.env.API_URL || 'http://localhost:8000';
        this.wsUrl = process.env.WS_URL || 'ws://localhost:8000/ws';
        this.axios = this.createAxiosInstance();
        this.wsConnections = new Map();
    }

    /**
     * Create an axios instance with default configuration
     * @returns {Object} - Axios instance
     */
    createAxiosInstance() {
        return axios.create({
            baseURL: this.baseUrl,
            timeout: 30000,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
    }

    /**
     * Handle an API request
     * @param {Object} request - Request object
     * @returns {Promise<Object>} - Response data
     */
    async handleRequest(request) {
        try {
            // Validate and sanitize request
            const sanitizedRequest = security.sanitizeData(request);
            
            // Log the request
            logManager.log('api', `Making API request: ${request.method} ${request.path}`, {
                request: sanitizedRequest
            });

            // Make the request
            const response = await this.axios({
                method: sanitizedRequest.method,
                url: sanitizedRequest.path,
                data: sanitizedRequest.body,
                headers: sanitizedRequest.headers,
                params: sanitizedRequest.params
            });

            // Log the response
            logManager.log('api', `Received API response: ${request.method} ${request.path}`, {
                status: response.status,
                data: response.data
            });

            return response.data;
        } catch (error) {
            // Log the error
            logManager.error('api', `API request failed: ${request.method} ${request.path}`, error);

            // Return error response
            return {
                success: false,
                error: {
                    message: error.message,
                    code: error.response?.status || 'UNKNOWN_ERROR',
                    data: error.response?.data
                }
            };
        }
    }

    /**
     * Handle a WebSocket stream
     * @param {Object} request - Stream request object
     * @returns {Promise<Object>} - Stream connection info
     */
    async handleStream(request) {
        try {
            // Generate unique connection ID
            const connectionId = `ws_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

            // Create WebSocket connection
            const ws = new WebSocket(`${this.wsUrl}${request.path}`);

            // Set up connection handlers
            ws.on('open', () => {
                logManager.log('api', `WebSocket connection opened: ${connectionId}`);
                
                // Send initial message if provided
                if (request.initialMessage) {
                    ws.send(JSON.stringify(request.initialMessage));
                }
            });

            ws.on('message', (data) => {
                try {
                    const message = JSON.parse(data);
                    logManager.log('api', `WebSocket message received: ${connectionId}`, { message });
                } catch (error) {
                    logManager.error('api', `Error parsing WebSocket message: ${connectionId}`, error);
                }
            });

            ws.on('error', (error) => {
                logManager.error('api', `WebSocket error: ${connectionId}`, error);
            });

            ws.on('close', () => {
                logManager.log('api', `WebSocket connection closed: ${connectionId}`);
                this.wsConnections.delete(connectionId);
            });

            // Store connection
            this.wsConnections.set(connectionId, {
                ws,
                path: request.path,
                options: request.options
            });

            return {
                success: true,
                connectionId,
                status: 'connected'
            };
        } catch (error) {
            logManager.error('api', `Failed to establish WebSocket connection: ${request.path}`, error);
            return {
                success: false,
                error: {
                    message: error.message,
                    code: 'WS_CONNECTION_ERROR'
                }
            };
        }
    }

    /**
     * Send a message through a WebSocket connection
     * @param {string} connectionId - Connection ID
     * @param {Object} message - Message to send
     * @returns {Promise<Object>} - Send result
     */
    async sendWebSocketMessage(connectionId, message) {
        try {
            const connection = this.wsConnections.get(connectionId);
            if (!connection) {
                throw new Error('WebSocket connection not found');
            }

            // Sanitize message
            const sanitizedMessage = security.sanitizeData(message);

            // Send message
            connection.ws.send(JSON.stringify(sanitizedMessage));

            return {
                success: true,
                connectionId
            };
        } catch (error) {
            logManager.error('api', `Failed to send WebSocket message: ${connectionId}`, error);
            return {
                success: false,
                error: {
                    message: error.message,
                    code: 'WS_SEND_ERROR'
                }
            };
        }
    }

    /**
     * Close a WebSocket connection
     * @param {string} connectionId - Connection ID
     * @returns {Promise<Object>} - Close result
     */
    async closeWebSocketConnection(connectionId) {
        try {
            const connection = this.wsConnections.get(connectionId);
            if (!connection) {
                throw new Error('WebSocket connection not found');
            }

            // Close connection
            connection.ws.close();
            this.wsConnections.delete(connectionId);

            return {
                success: true,
                connectionId
            };
        } catch (error) {
            logManager.error('api', `Failed to close WebSocket connection: ${connectionId}`, error);
            return {
                success: false,
                error: {
                    message: error.message,
                    code: 'WS_CLOSE_ERROR'
                }
            };
        }
    }

    /**
     * Clean up all resources
     */
    cleanup() {
        // Close all WebSocket connections
        for (const [connectionId, connection] of this.wsConnections) {
            try {
                connection.ws.close();
            } catch (error) {
                logManager.error('api', `Error closing WebSocket connection: ${connectionId}`, error);
            }
        }
        this.wsConnections.clear();
    }
}

module.exports = new ApiBridge(); 