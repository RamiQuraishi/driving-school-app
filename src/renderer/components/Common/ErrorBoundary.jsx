/**
 * ErrorBoundary component for catching and handling React errors.
 * Provides a fallback UI and error reporting functionality.
 */

import React from 'react';
import {
    Box,
    Typography,
    Button,
    Paper,
    useTheme
} from '@mui/material';
import { Error as ErrorIcon } from '@mui/icons-material';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            hasError: false,
            error: null,
            errorInfo: null
        };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        this.setState({
            error,
            errorInfo
        });

        // Log error to monitoring service
        console.error('Error caught by boundary:', error, errorInfo);
        
        // Report error to main process
        if (window.electron?.ipcRenderer) {
            window.electron.ipcRenderer.send('error:report', {
                error: error.toString(),
                stack: errorInfo?.componentStack
            });
        }
    }

    handleReset = () => {
        this.setState({
            hasError: false,
            error: null,
            errorInfo: null
        });
    };

    render() {
        if (this.state.hasError) {
            return (
                <ErrorFallback
                    error={this.state.error}
                    errorInfo={this.state.errorInfo}
                    onReset={this.handleReset}
                />
            );
        }

        return this.props.children;
    }
}

const ErrorFallback = ({ error, errorInfo, onReset }) => {
    const theme = useTheme();

    return (
        <Box
            sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                minHeight: '100vh',
                padding: theme.spacing(2),
                backgroundColor: theme.palette.background.default
            }}
        >
            <Paper
                elevation={3}
                sx={{
                    padding: theme.spacing(3),
                    maxWidth: 600,
                    width: '100%',
                    textAlign: 'center'
                }}
            >
                <ErrorIcon
                    color="error"
                    sx={{ fontSize: 48, mb: 2 }}
                />
                <Typography
                    variant="h5"
                    component="h1"
                    gutterBottom
                >
                    Something went wrong
                </Typography>
                <Typography
                    variant="body1"
                    color="textSecondary"
                    paragraph
                >
                    {error?.toString()}
                </Typography>
                {process.env.NODE_ENV === 'development' && errorInfo && (
                    <Box
                        sx={{
                            mt: 2,
                            p: 2,
                            backgroundColor: theme.palette.background.paper,
                            borderRadius: 1,
                            overflow: 'auto',
                            maxHeight: 200
                        }}
                    >
                        <Typography
                            variant="caption"
                            component="pre"
                            sx={{
                                whiteSpace: 'pre-wrap',
                                wordBreak: 'break-word'
                            }}
                        >
                            {errorInfo.componentStack}
                        </Typography>
                    </Box>
                )}
                <Button
                    variant="contained"
                    color="primary"
                    onClick={onReset}
                    sx={{ mt: 3 }}
                >
                    Try Again
                </Button>
            </Paper>
        </Box>
    );
};

export default ErrorBoundary; 