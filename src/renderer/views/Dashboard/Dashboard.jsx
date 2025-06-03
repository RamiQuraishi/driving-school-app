/**
 * Dashboard view component.
 * Displays overview of the application with various widgets and statistics.
 */

import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
    Box,
    Container,
    Grid,
    Paper,
    Typography,
    useTheme,
    useMediaQuery
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
    School as SchoolIcon,
    Person as PersonIcon,
    Event as EventIcon,
    Assessment as AssessmentIcon
} from '@mui/icons-material';
import { LoadingSpinner } from '../../components/Common';
import DashboardWidgets from './DashboardWidgets';
import { fetchDashboardData } from '../../store/actions';

// Styled components
const DashboardContainer = styled(Container)(({ theme }) => ({
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4)
}));

const StatCard = styled(Paper)(({ theme }) => ({
    padding: theme.spacing(3),
    display: 'flex',
    alignItems: 'center',
    gap: theme.spacing(2),
    height: '100%'
}));

const StatIcon = styled(Box)(({ theme, color }) => ({
    width: 48,
    height: 48,
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: theme.palette[color].light,
    color: theme.palette[color].main
}));

const Dashboard = () => {
    const theme = useTheme();
    const dispatch = useDispatch();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    const { data, isLoading, error } = useSelector(state => state.dashboard);

    useEffect(() => {
        dispatch(fetchDashboardData());
    }, [dispatch]);

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

    const stats = [
        {
            title: 'Total Schools',
            value: data?.stats?.schools || 0,
            icon: <SchoolIcon />,
            color: 'primary'
        },
        {
            title: 'Active Students',
            value: data?.stats?.students || 0,
            icon: <PersonIcon />,
            color: 'success'
        },
        {
            title: 'Upcoming Lessons',
            value: data?.stats?.lessons || 0,
            icon: <EventIcon />,
            color: 'warning'
        },
        {
            title: 'Pass Rate',
            value: `${data?.stats?.passRate || 0}%`,
            icon: <AssessmentIcon />,
            color: 'info'
        }
    ];

    return (
        <DashboardContainer maxWidth="xl">
            <Typography variant="h4" component="h1" gutterBottom>
                Dashboard
            </Typography>

            <Grid container spacing={3}>
                {/* Stats Cards */}
                {stats.map((stat, index) => (
                    <Grid item xs={12} sm={6} md={3} key={index}>
                        <StatCard elevation={2}>
                            <StatIcon color={stat.color}>
                                {stat.icon}
                            </StatIcon>
                            <Box>
                                <Typography variant="h6" component="div">
                                    {stat.value}
                                </Typography>
                                <Typography variant="body2" color="textSecondary">
                                    {stat.title}
                                </Typography>
                            </Box>
                        </StatCard>
                    </Grid>
                ))}

                {/* Dashboard Widgets */}
                <Grid item xs={12}>
                    <DashboardWidgets data={data?.widgets} />
                </Grid>
            </Grid>
        </DashboardContainer>
    );
};

export default Dashboard; 