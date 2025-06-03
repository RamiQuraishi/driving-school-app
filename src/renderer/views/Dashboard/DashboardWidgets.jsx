/**
 * DashboardWidgets component.
 * Displays various data visualizations and information cards.
 */

import React from 'react';
import {
    Box,
    Grid,
    Paper,
    Typography,
    useTheme,
    useMediaQuery
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    PieChart,
    Pie,
    Cell
} from 'recharts';

// Styled components
const WidgetPaper = styled(Paper)(({ theme }) => ({
    padding: theme.spacing(3),
    height: '100%'
}));

const WidgetTitle = styled(Typography)(({ theme }) => ({
    marginBottom: theme.spacing(2)
}));

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const DashboardWidgets = ({ data }) => {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

    // Sample data - replace with actual data from props
    const enrollmentData = [
        { month: 'Jan', students: 65 },
        { month: 'Feb', students: 75 },
        { month: 'Mar', students: 85 },
        { month: 'Apr', students: 95 },
        { month: 'May', students: 105 },
        { month: 'Jun', students: 115 }
    ];

    const passRateData = [
        { name: 'Passed', value: 75 },
        { name: 'Failed', value: 25 }
    ];

    const recentActivity = [
        { id: 1, type: 'New Student', name: 'John Doe', time: '2 hours ago' },
        { id: 2, type: 'Lesson Completed', name: 'Jane Smith', time: '3 hours ago' },
        { id: 3, type: 'Test Passed', name: 'Mike Johnson', time: '5 hours ago' }
    ];

    return (
        <Grid container spacing={3}>
            {/* Enrollment Trend */}
            <Grid item xs={12} md={8}>
                <WidgetPaper elevation={2}>
                    <WidgetTitle variant="h6">
                        Student Enrollment Trend
                    </WidgetTitle>
                    <Box sx={{ height: 300 }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={enrollmentData}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="month" />
                                <YAxis />
                                <Tooltip />
                                <Line
                                    type="monotone"
                                    dataKey="students"
                                    stroke={theme.palette.primary.main}
                                    strokeWidth={2}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </Box>
                </WidgetPaper>
            </Grid>

            {/* Pass Rate Distribution */}
            <Grid item xs={12} md={4}>
                <WidgetPaper elevation={2}>
                    <WidgetTitle variant="h6">
                        Pass Rate Distribution
                    </WidgetTitle>
                    <Box sx={{ height: 300 }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={passRateData}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={80}
                                    fill="#8884d8"
                                    paddingAngle={5}
                                    dataKey="value"
                                    label
                                >
                                    {passRateData.map((entry, index) => (
                                        <Cell
                                            key={`cell-${index}`}
                                            fill={COLORS[index % COLORS.length]}
                                        />
                                    ))}
                                </Pie>
                                <Tooltip />
                            </PieChart>
                        </ResponsiveContainer>
                    </Box>
                </WidgetPaper>
            </Grid>

            {/* Recent Activity */}
            <Grid item xs={12}>
                <WidgetPaper elevation={2}>
                    <WidgetTitle variant="h6">
                        Recent Activity
                    </WidgetTitle>
                    <Grid container spacing={2}>
                        {recentActivity.map((activity) => (
                            <Grid item xs={12} sm={4} key={activity.id}>
                                <Paper
                                    sx={{
                                        p: 2,
                                        backgroundColor: theme.palette.background.default
                                    }}
                                >
                                    <Typography variant="subtitle2" color="primary">
                                        {activity.type}
                                    </Typography>
                                    <Typography variant="body1">
                                        {activity.name}
                                    </Typography>
                                    <Typography variant="body2" color="textSecondary">
                                        {activity.time}
                                    </Typography>
                                </Paper>
                            </Grid>
                        ))}
                    </Grid>
                </WidgetPaper>
            </Grid>

            {/* Quick Stats */}
            <Grid item xs={12} md={6}>
                <WidgetPaper elevation={2}>
                    <WidgetTitle variant="h6">
                        Upcoming Lessons
                    </WidgetTitle>
                    <Box sx={{ height: 200, overflow: 'auto' }}>
                        {data?.upcomingLessons?.map((lesson, index) => (
                            <Box
                                key={index}
                                sx={{
                                    p: 2,
                                    borderBottom: 1,
                                    borderColor: 'divider'
                                }}
                            >
                                <Typography variant="subtitle1">
                                    {lesson.title}
                                </Typography>
                                <Typography variant="body2" color="textSecondary">
                                    {lesson.time} - {lesson.instructor}
                                </Typography>
                            </Box>
                        ))}
                    </Box>
                </WidgetPaper>
            </Grid>

            {/* Notifications */}
            <Grid item xs={12} md={6}>
                <WidgetPaper elevation={2}>
                    <WidgetTitle variant="h6">
                        Notifications
                    </WidgetTitle>
                    <Box sx={{ height: 200, overflow: 'auto' }}>
                        {data?.notifications?.map((notification, index) => (
                            <Box
                                key={index}
                                sx={{
                                    p: 2,
                                    borderBottom: 1,
                                    borderColor: 'divider'
                                }}
                            >
                                <Typography variant="subtitle1">
                                    {notification.title}
                                </Typography>
                                <Typography variant="body2" color="textSecondary">
                                    {notification.message}
                                </Typography>
                            </Box>
                        ))}
                    </Box>
                </WidgetPaper>
            </Grid>
        </Grid>
    );
};

export default DashboardWidgets; 