/**
 * PerformanceSettings component.
 * Manages application performance tuning options.
 */

import React from 'react';
import {
    Box,
    Grid,
    Typography,
    Slider,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
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

const PerformanceSettings = ({ data = {}, onChange }) => {
    const {
        cacheSize = 100,
        maxConcurrentRequests = 5,
        autoOptimize = true,
        lowPowerMode = false,
        renderQuality = 'high',
        lastUpdated = null
    } = data;

    const handleSliderChange = (setting) => (event, newValue) => {
        onChange(setting, newValue);
    };

    const handleSelectChange = (setting) => (event) => {
        onChange(setting, event.target.value);
    };

    const handleSwitchChange = (setting) => (event) => {
        onChange(setting, event.target.checked);
    };

    return (
        <Box>
            <Typography variant="h6" gutterBottom>
                Performance Settings
            </Typography>

            <Alert severity="info" sx={{ mb: 3 }}>
                <AlertTitle>Performance Optimization</AlertTitle>
                Adjust these settings to optimize the application's performance based on your system capabilities
                and preferences.
            </Alert>

            <SettingsPaper elevation={1}>
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <Typography gutterBottom>
                            Cache Size (MB)
                        </Typography>
                        <Slider
                            value={cacheSize}
                            onChange={handleSliderChange('cacheSize')}
                            min={50}
                            max={500}
                            step={10}
                            marks={[
                                { value: 50, label: '50MB' },
                                { value: 250, label: '250MB' },
                                { value: 500, label: '500MB' }
                            ]}
                            valueLabelDisplay="auto"
                        />
                        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                            Adjust the amount of memory used for caching data
                        </Typography>
                    </Grid>

                    <Grid item xs={12}>
                        <Divider />
                    </Grid>

                    <Grid item xs={12}>
                        <Typography gutterBottom>
                            Maximum Concurrent Requests
                        </Typography>
                        <Slider
                            value={maxConcurrentRequests}
                            onChange={handleSliderChange('maxConcurrentRequests')}
                            min={1}
                            max={10}
                            step={1}
                            marks
                            valueLabelDisplay="auto"
                        />
                        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                            Control how many requests can be processed simultaneously
                        </Typography>
                    </Grid>

                    <Grid item xs={12}>
                        <Divider />
                    </Grid>

                    <Grid item xs={12}>
                        <FormControl fullWidth>
                            <InputLabel>Render Quality</InputLabel>
                            <Select
                                value={renderQuality}
                                onChange={handleSelectChange('renderQuality')}
                                label="Render Quality"
                            >
                                <MenuItem value="low">Low (Better Performance)</MenuItem>
                                <MenuItem value="medium">Medium (Balanced)</MenuItem>
                                <MenuItem value="high">High (Better Quality)</MenuItem>
                            </Select>
                        </FormControl>
                        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                            Adjust the visual quality of the application interface
                        </Typography>
                    </Grid>

                    <Grid item xs={12}>
                        <Divider />
                    </Grid>

                    <Grid item xs={12}>
                        <FormControlLabel
                            control={
                                <Switch
                                    checked={autoOptimize}
                                    onChange={handleSwitchChange('autoOptimize')}
                                    color="primary"
                                />
                            }
                            label="Automatic Optimization"
                        />
                        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                            Automatically adjust settings based on system performance
                        </Typography>
                    </Grid>

                    <Grid item xs={12}>
                        <FormControlLabel
                            control={
                                <Switch
                                    checked={lowPowerMode}
                                    onChange={handleSwitchChange('lowPowerMode')}
                                    color="primary"
                                />
                            }
                            label="Low Power Mode"
                        />
                        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                            Reduce resource usage for better battery life
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

export default PerformanceSettings; 