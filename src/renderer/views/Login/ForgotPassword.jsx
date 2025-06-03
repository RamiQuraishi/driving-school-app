/**
 * ForgotPassword component.
 * Handles password reset requests and email verification.
 */

import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import {
    Box,
    Button,
    TextField,
    Typography,
    useTheme,
    CircularProgress,
    Alert
} from '@mui/material';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { requestPasswordReset } from '../../store/actions';

// Form validation schema
const schema = yup.object().shape({
    email: yup
        .string()
        .email('Please enter a valid email address')
        .required('Email is required')
});

const ForgotPassword = ({ onBack }) => {
    const theme = useTheme();
    const dispatch = useDispatch();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    const {
        register,
        handleSubmit,
        formState: { errors }
    } = useForm({
        resolver: yupResolver(schema),
        defaultValues: {
            email: ''
        }
    });

    const handleFormSubmit = async (data) => {
        try {
            setIsSubmitting(true);
            setError(null);
            setSuccess(false);

            await dispatch(requestPasswordReset(data.email)).unwrap();
            setSuccess(true);
        } catch (error) {
            setError(error.message || 'Failed to send reset instructions. Please try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    if (success) {
        return (
            <Box
                sx={{
                    width: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: theme.spacing(2)
                }}
            >
                <Alert severity="success" sx={{ mb: 2 }}>
                    Password reset instructions have been sent to your email.
                </Alert>

                <Typography variant="body2" color="textSecondary" align="center">
                    Please check your email for instructions to reset your password.
                    If you don't see the email, please check your spam folder.
                </Typography>

                <Button
                    onClick={onBack}
                    fullWidth
                    variant="outlined"
                    sx={{ mt: 2 }}
                >
                    Back to Login
                </Button>
            </Box>
        );
    }

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
            <Typography variant="h6" align="center" gutterBottom>
                Reset Password
            </Typography>

            <Typography variant="body2" color="textSecondary" align="center" paragraph>
                Enter your email address and we'll send you instructions to reset your password.
            </Typography>

            {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                </Alert>
            )}

            <TextField
                fullWidth
                label="Email"
                type="email"
                autoComplete="email"
                error={!!errors.email}
                helperText={errors.email?.message}
                {...register('email')}
            />

            <Box
                sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    mt: 2
                }}
            >
                <Button
                    onClick={onBack}
                    disabled={isSubmitting}
                >
                    Back to Login
                </Button>

                <Button
                    type="submit"
                    variant="contained"
                    disabled={isSubmitting}
                >
                    {isSubmitting ? (
                        <CircularProgress size={24} color="inherit" />
                    ) : (
                        'Send Instructions'
                    )}
                </Button>
            </Box>
        </Box>
    );
};

export default ForgotPassword; 