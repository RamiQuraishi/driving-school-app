import React, { useEffect, useState } from 'react';
import { apiClient } from '../electron/api-client';

function App() {
    const [message, setMessage] = useState('Loading...');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await apiClient.getHealth();
                setMessage(response.message);
            } catch (error) {
                setMessage('Error connecting to API');
                console.error('API Error:', error);
            }
        };

        fetchData();
    }, []);

    return (
        <div className="app">
            <h1>Ontario Driving School Manager</h1>
            <p>{message}</p>
        </div>
    );
}

export default App; 