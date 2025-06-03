/**
 * LoginForm component.
 * Handles user credentials input and validation.
 */

import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import {
    Box,
    Button,
    TextField,
    IconButton,
    InputAdornment,
    Link,
    Typography,
    useTheme
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';

// Form validation schema
const schema = yup.object().shape({
    email: yup
        .string()
        .email('Please enter a valid email address')
        .required('Email is required'),
    password: yup
        .string()
        .min(8, 'Password must be at least 8 characters')
        .required('Password is required')
});

const LoginForm = ({ onSubmit, onForgotPassword }) => {
    const theme = useTheme();
    const [showPassword, setShowPassword] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const {
        register,
        handleSubmit,
        formState: { errors }
    } = useForm({
        resolver: yupResolver(schema),
        defaultValues: {
            email: '',
            password: ''
        }
    });

    const handleFormSubmit = async (data) => {
        try {
            setIsSubmitting(true);
            await onSubmit(data);
        } catch (error) {
            console.error('Form submission failed:', error);
        } finally {
            setIsSubmitting(false);
        }
    };

    const togglePasswordVisibility = () => {
        setShowPassword(!showPassword);
    };

    return (
        <Box
            component="form"
            onSubmit={handleSubmit(handleFormSubmit)}
            sx={{
                width: '100%',
                display: 'flex',
                flexDirection: 'column',
                gap: theme.spacing(2)
            }}
        >
            <TextField
                fullWidth
                label="Email"
                type="email"
                autoComplete="email"
                error={!!errors.email}
                helperText={errors.email?.message}
                {...register('email')}
            />

            <TextField
                fullWidth
                label="Password"
                type={showPassword ? 'text' : 'password'}
                autoComplete="current-password"
                error={!!errors.password}
                helperText={errors.password?.message}
                InputProps={{
                    endAdornment: (
                        <InputAdornment position="end">
                            <IconButton
                                onClick={togglePasswordVisibility}
                                edge="end"
                            >
                                {showPassword ? <VisibilityOff /> : <Visibility />}
                            </IconButton>
                        </InputAdornment>
                    )
                }}
                {...register('password')}
            />

            <Box
                sx={{
                    display: 'flex',
                    justifyContent: 'flex-end',
                    alignItems: 'center'
                }}
            >
                <Link
                    component="button"
                    variant="body2"
                    onClick={onForgotPassword}
                    sx={{ textDecoration: 'none' }}
                >
                    Forgot password?
                </Link>
            </Box>

            <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={isSubmitting}
                sx={{ mt: 2 }}
            >
                {isSubmitting ? 'Signing in...' : 'Sign In'}
            </Button>

            <Typography variant="body2" color="textSecondary" align="center" sx={{ mt: 2 }}>
                Don't have an account?{' '}
                <Link href="/register" sx={{ textDecoration: 'none' }}>
                    Sign up
                </Link>
            </Typography>
        </Box>
    );
};

export default LoginForm; 