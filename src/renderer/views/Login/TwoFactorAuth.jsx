/**
 * TwoFactorAuth component.
 * Handles two-factor authentication verification.
 */

import React, { useState, useRef, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import {
    Box,
    Button,
    TextField,
    Typography,
    useTheme,
    CircularProgress
} from '@mui/material';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { verifyTwoFactor } from '../../store/actions';

// Form validation schema
const schema = yup.object().shape({
    code: yup
        .string()
        .matches(/^\d{6}$/, 'Please enter a valid 6-digit code')
        .required('Verification code is required')
});

const TwoFactorAuth = ({ loginData, onSuccess, onBack }) => {
    const theme = useTheme();
    const dispatch = useDispatch();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState(null);
    const [timeLeft, setTimeLeft] = useState(30);
    const timerRef = useRef(null);

    const {
        register,
        handleSubmit,
        formState: { errors },
        setValue
    } = useForm({
        resolver: yupResolver(schema),
        defaultValues: {
            code: ''
        }
    });

    // Handle code input with auto-formatting
    const handleCodeChange = (e) => {
        const value = e.target.value.replace(/\D/g, '').slice(0, 6);
        setValue('code', value);
    };

    // Start countdown timer
    useEffect(() => {
        timerRef.current = setInterval(() => {
            setTimeLeft((prev) => {
                if (prev <= 1) {
                    clearInterval(timerRef.current);
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);

        return () => {
            if (timerRef.current) {
                clearInterval(timerRef.current);
            }
        };
    }, []);

    const handleFormSubmit = async (data) => {
        try {
            setIsSubmitting(true);
            setError(null);

            const result = await dispatch(verifyTwoFactor({
                ...loginData,
                code: data.code
            })).unwrap();

            onSuccess(result);
        } catch (error) {
            setError(error.message || 'Verification failed. Please try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleResendCode = async () => {
        try {
            setIsSubmitting(true);
            setError(null);
            // Implement resend code logic here
            setTimeLeft(30);
        } catch (error) {
            setError('Failed to resend code. Please try again.');
        } finally {
            setIsSubmitting(false);
        }
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
            <Typography variant="h6" align="center" gutterBottom>
                Two-Factor Authentication
            </Typography>

            <Typography variant="body2" color="textSecondary" align="center" paragraph>
                Please enter the 6-digit verification code sent to your email
            </Typography>

            {error && (
                <Typography color="error" align="center" paragraph>
                    {error}
                </Typography>
            )}

            <TextField
                fullWidth
                label="Verification Code"
                type="text"
                inputMode="numeric"
                autoComplete="one-time-code"
                error={!!errors.code}
                helperText={errors.code?.message}
                onChange={handleCodeChange}
                {...register('code')}
            />

            <Box
                sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                }}
            >
                <Button
                    onClick={onBack}
                    disabled={isSubmitting}
                >
                    Back to Login
                </Button>

                <Button
                    onClick={handleResendCode}
                    disabled={isSubmitting || timeLeft > 0}
                >
                    {timeLeft > 0 ? `Resend in ${timeLeft}s` : 'Resend Code'}
                </Button>
            </Box>

            <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={isSubmitting}
                sx={{ mt: 2 }}
            >
                {isSubmitting ? (
                    <CircularProgress size={24} color="inherit" />
                ) : (
                    'Verify'
                )}
            </Button>
        </Box>
    );
};

export default TwoFactorAuth; 