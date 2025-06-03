/**
 * Login view component.
 * Handles the main authentication flow and layout.
 */

import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { Box, Container, Paper, Typography, useTheme } from '@mui/material';
import { styled } from '@mui/material/styles';
import { selectAuth } from '../../store/reducers/auth';
import { setCredentials } from '../../store/actions';
import LoginForm from './LoginForm';
import TwoFactorAuth from './TwoFactorAuth';
import ForgotPassword from './ForgotPassword';
import { LoadingSpinner } from '../../components/Common';

// Styled components
const LoginContainer = styled(Container)(({ theme }) => ({
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: theme.spacing(2)
}));

const LoginPaper = styled(Paper)(({ theme }) => ({
    padding: theme.spacing(4),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    maxWidth: 400,
    width: '100%'
}));

const Logo = styled('img')({
    width: 120,
    height: 'auto',
    marginBottom: 24
});

const Login = () => {
    const theme = useTheme();
    const navigate = useNavigate();
    const location = useLocation();
    const dispatch = useDispatch();
    const { isAuthenticated, isLoading, error } = useSelector(selectAuth);
    const [showTwoFactor, setShowTwoFactor] = useState(false);
    const [showForgotPassword, setShowForgotPassword] = useState(false);
    const [loginData, setLoginData] = useState(null);

    // Redirect if already authenticated
    useEffect(() => {
        if (isAuthenticated) {
            const from = location.state?.from?.pathname || '/dashboard';
            navigate(from, { replace: true });
        }
    }, [isAuthenticated, navigate, location]);

    const handleLogin = async (credentials) => {
        try {
            const result = await dispatch(setCredentials(credentials)).unwrap();
            
            if (result.requiresTwoFactor) {
                setLoginData(result);
                setShowTwoFactor(true);
            } else {
                navigate('/dashboard');
            }
        } catch (error) {
            console.error('Login failed:', error);
        }
    };

    const handleTwoFactorSuccess = () => {
        setShowTwoFactor(false);
        navigate('/dashboard');
    };

    const handleForgotPassword = () => {
        setShowForgotPassword(true);
    };

    const handleBackToLogin = () => {
        setShowForgotPassword(false);
        setShowTwoFactor(false);
    };

    if (isLoading) {
        return <LoadingSpinner />;
    }

    return (
        <LoginContainer>
            <LoginPaper elevation={3}>
                <Logo src="/assets/logo.png" alt="Rami Drive School" />
                
                <Typography variant="h4" component="h1" gutterBottom>
                    Welcome Back
                </Typography>
                
                <Typography variant="body2" color="textSecondary" align="center" paragraph>
                    Please sign in to continue
                </Typography>

                {error && (
                    <Typography color="error" align="center" paragraph>
                        {error}
                    </Typography>
                )}

                {showTwoFactor ? (
                    <TwoFactorAuth
                        loginData={loginData}
                        onSuccess={handleTwoFactorSuccess}
                        onBack={handleBackToLogin}
                    />
                ) : showForgotPassword ? (
                    <ForgotPassword onBack={handleBackToLogin} />
                ) : (
                    <LoginForm
                        onSubmit={handleLogin}
                        onForgotPassword={handleForgotPassword}
                    />
                )}
            </LoginPaper>
        </LoginContainer>
    );
};

export default Login; 