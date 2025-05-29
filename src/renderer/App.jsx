import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Box, CircularProgress } from '@mui/material';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Students from './pages/Students';
import Instructors from './pages/Instructors';
import Lessons from './pages/Lessons';
import Payments from './pages/Payments';
import Settings from './pages/Settings';

const App = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [isHealthy, setIsHealthy] = useState(false);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const health = await window.api.checkHealth();
        setIsHealthy(health.status === 'ok');
      } catch (error) {
        console.error('Health check failed:', error);
        setIsHealthy(false);
      } finally {
        setIsLoading(false);
      }
    };

    checkHealth();
  }, []);

  if (isLoading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  if (!isHealthy) {
    return (
      <Box
        display="flex"
        flexDirection="column"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
        p={3}
      >
        <h1>Service Unavailable</h1>
        <p>The application is currently unable to connect to the backend service.</p>
        <p>Please try again later or contact support if the problem persists.</p>
      </Box>
    );
  }

  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/students" element={<Students />} />
          <Route path="/instructors" element={<Instructors />} />
          <Route path="/lessons" element={<Lessons />} />
          <Route path="/payments" element={<Payments />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App; 