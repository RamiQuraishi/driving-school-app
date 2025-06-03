/**
 * Settings view component.
 * Manages application settings and preferences.
 */

import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
    Box,
    Container,
    Grid,
    Paper,
    Typography,
    Tabs,
    Tab,
    useTheme,
    useMediaQuery
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
    Settings as SettingsIcon,
    Speed as SpeedIcon,
    Analytics as AnalyticsIcon,
    Security as SecurityIcon,
    Notifications as NotificationsIcon,
    Language as LanguageIcon
} from '@mui/icons-material';
import { LoadingSpinner } from '../../components/Common';
import TelemetrySettings from './TelemetrySettings';
import PerformanceSettings from './PerformanceSettings';
import { updateSettings } from '../../store/actions';

// Styled components
const SettingsContainer = styled(Container)(({ theme }) => ({
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4)
}));

const SettingsPaper = styled(Paper)(({ theme }) => ({
    padding: theme.spacing(3),
    height: '100%'
}));

const TabPanel = ({ children, value, index, ...other }) => (
    <div
        role="tabpanel"
        hidden={value !== index}
        id={`settings-tabpanel-${index}`}
        aria-labelledby={`settings-tab-${index}`}
        {...other}
    >
        {value === index && (
            <Box sx={{ p: 3 }}>
                {children}
            </Box>
        )}
    </div>
);

const Settings = () => {
    const theme = useTheme();
    const dispatch = useDispatch();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    const { data, isLoading, error } = useSelector(state => state.settings);
    const [activeTab, setActiveTab] = useState(0);

    const handleTabChange = (event, newValue) => {
        setActiveTab(newValue);
    };

    const handleSettingChange = async (setting, value) => {
        try {
            await dispatch(updateSettings({ [setting]: value })).unwrap();
        } catch (error) {
            console.error('Failed to update setting:', error);
        }
    };

    if (isLoading) {
        return <LoadingSpinner />;
    }

    if (error) {
        return (
            <Box sx={{ p: 3 }}>
                <Typography color="error">{error}</Typography>
            </Box>
        );
    }

    const tabs = [
        {
            label: 'General',
            icon: <SettingsIcon />,
            content: (
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <Typography variant="h6" gutterBottom>
                            General Settings
                        </Typography>
                        {/* Add general settings controls */}
                    </Grid>
                </Grid>
            )
        },
        {
            label: 'Performance',
            icon: <SpeedIcon />,
            content: <PerformanceSettings data={data?.performance} onChange={handleSettingChange} />
        },
        {
            label: 'Telemetry',
            icon: <AnalyticsIcon />,
            content: <TelemetrySettings data={data?.telemetry} onChange={handleSettingChange} />
        },
        {
            label: 'Security',
            icon: <SecurityIcon />,
            content: (
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <Typography variant="h6" gutterBottom>
                            Security Settings
                        </Typography>
                        {/* Add security settings controls */}
                    </Grid>
                </Grid>
            )
        },
        {
            label: 'Notifications',
            icon: <NotificationsIcon />,
            content: (
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <Typography variant="h6" gutterBottom>
                            Notification Settings
                        </Typography>
                        {/* Add notification settings controls */}
                    </Grid>
                </Grid>
            )
        },
        {
            label: 'Language',
            icon: <LanguageIcon />,
            content: (
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <Typography variant="h6" gutterBottom>
                            Language Settings
                        </Typography>
                        {/* Add language settings controls */}
                    </Grid>
                </Grid>
            )
        }
    ];

    return (
        <SettingsContainer maxWidth="lg">
            <Typography variant="h4" component="h1" gutterBottom>
                Settings
            </Typography>

            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <SettingsPaper elevation={2}>
                        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                            <Tabs
                                value={activeTab}
                                onChange={handleTabChange}
                                variant={isMobile ? 'scrollable' : 'fullWidth'}
                                scrollButtons={isMobile ? 'auto' : false}
                                aria-label="settings tabs"
                            >
                                {tabs.map((tab, index) => (
                                    <Tab
                                        key={index}
                                        icon={tab.icon}
                                        label={tab.label}
                                        id={`settings-tab-${index}`}
                                        aria-controls={`settings-tabpanel-${index}`}
                                    />
                                ))}
                            </Tabs>
                        </Box>

                        {tabs.map((tab, index) => (
                            <TabPanel key={index} value={activeTab} index={index}>
                                {tab.content}
                            </TabPanel>
                        ))}
                    </SettingsPaper>
                </Grid>
            </Grid>
        </SettingsContainer>
    );
};

export default Settings; 