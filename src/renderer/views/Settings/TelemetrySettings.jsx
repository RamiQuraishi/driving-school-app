/**
 * TelemetrySettings component.
 * Manages telemetry and analytics opt-in/out settings.
 */

import React from 'react';
import {
    Box,
    Grid,
    Typography,
    Switch,
    FormControlLabel,
    Paper,
    Divider,
    Alert,
    AlertTitle
} from '@mui/material';
import { styled } from '@mui/material/styles';

const SettingsPaper = styled(Paper)(({ theme }) => ({
    padding: theme.spacing(3),
    marginBottom: theme.spacing(3)
}));

const TelemetrySettings = ({ data = {}, onChange }) => {
    const {
        enabled = false,
        crashReporting = false,
        usageAnalytics = false,
        performanceMetrics = false,
        lastUpdated = null
    } = data;

    const handleChange = (setting) => (event) => {
        onChange(setting, event.target.checked);
    };

    return (
        <Box>
            <Typography variant="h6" gutterBottom>
                Telemetry & Analytics Settings
            </Typography>

            <Alert severity="info" sx={{ mb: 3 }}>
                <AlertTitle>About Telemetry</AlertTitle>
                We collect anonymous usage data to improve your experience and help us identify and fix issues.
                You can opt out of any or all telemetry collection at any time.
            </Alert>

            <SettingsPaper elevation={1}>
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <FormControlLabel
                            control={
                                <Switch
                                    checked={enabled}
                                    onChange={handleChange('enabled')}
                                    color="primary"
                                />
                            }
                            label="Enable Telemetry"
                        />
                        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                            Master switch for all telemetry collection
                        </Typography>
                    </Grid>

                    <Grid item xs={12}>
                        <Divider />
                    </Grid>

                    <Grid item xs={12}>
                        <FormControlLabel
                            control={
                                <Switch
                                    checked={crashReporting}
                                    onChange={handleChange('crashReporting')}
                                    disabled={!enabled}
                                    color="primary"
                                />
                            }
                            label="Crash Reporting"
                        />
                        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                            Automatically send crash reports to help us improve stability
                        </Typography>
                    </Grid>

                    <Grid item xs={12}>
                        <FormControlLabel
                            control={
                                <Switch
                                    checked={usageAnalytics}
                                    onChange={handleChange('usageAnalytics')}
                                    disabled={!enabled}
                                    color="primary"
                                />
                            }
                            label="Usage Analytics"
                        />
                        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                            Collect anonymous usage data to improve features and user experience
                        </Typography>
                    </Grid>

                    <Grid item xs={12}>
                        <FormControlLabel
                            control={
                                <Switch
                                    checked={performanceMetrics}
                                    onChange={handleChange('performanceMetrics')}
                                    disabled={!enabled}
                                    color="primary"
                                />
                            }
                            label="Performance Metrics"
                        />
                        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                            Track application performance to optimize speed and resource usage
                        </Typography>
                    </Grid>
                </Grid>
            </SettingsPaper>

            {lastUpdated && (
                <Typography variant="caption" color="textSecondary">
                    Last updated: {new Date(lastUpdated).toLocaleString()}
                </Typography>
            )}
        </Box>
    );
};

export default TelemetrySettings; 