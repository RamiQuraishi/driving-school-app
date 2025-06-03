/**
 * Toolbar component for both mobile and desktop views.
 * Provides app bar with actions and navigation controls.
 */

import React from 'react';
import {
    AppBar,
    Toolbar as MuiToolbar,
    IconButton,
    Typography,
    Box,
    useTheme,
    useMediaQuery,
    Button,
    Avatar,
    Menu,
    MenuItem
} from '@mui/material';
import {
    Menu as MenuIcon,
    Notifications as NotificationsIcon,
    Search as SearchIcon,
    Brightness4 as DarkModeIcon,
    Brightness7 as LightModeIcon,
    MoreVert as MoreIcon
} from '@mui/icons-material';
import { useAppContext } from '../../context/AppContext';

const Toolbar = ({ onMenuClick, onQuickActionsClick, variant = 'desktop' }) => {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    const { isDarkMode, toggleTheme } = useAppContext();
    const [anchorEl, setAnchorEl] = React.useState(null);

    const handleMenuOpen = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleMenuClose = () => {
        setAnchorEl(null);
    };

    return (
        <AppBar
            position="fixed"
            sx={{
                zIndex: theme.zIndex.drawer + 1,
                backgroundColor: theme.palette.background.paper,
                color: theme.palette.text.primary,
                boxShadow: theme.shadows[1]
            }}
        >
            <MuiToolbar>
                {variant === 'mobile' && (
                    <IconButton
                        edge="start"
                        color="inherit"
                        aria-label="menu"
                        onClick={onMenuClick}
                        sx={{ mr: 2 }}
                    >
                        <MenuIcon />
                    </IconButton>
                )}

                <Typography
                    variant="h6"
                    component="div"
                    sx={{ flexGrow: 1, display: 'flex', alignItems: 'center' }}
                >
                    Rami Drive School
                </Typography>

                {!isMobile && (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <IconButton
                            color="inherit"
                            onClick={() => {/* Handle search */}}
                        >
                            <SearchIcon />
                        </IconButton>
                        <IconButton
                            color="inherit"
                            onClick={() => {/* Handle notifications */}}
                        >
                            <NotificationsIcon />
                        </IconButton>
                        <IconButton
                            color="inherit"
                            onClick={toggleTheme}
                        >
                            {isDarkMode ? <LightModeIcon /> : <DarkModeIcon />}
                        </IconButton>
                    </Box>
                )}

                {isMobile && (
                    <IconButton
                        color="inherit"
                        onClick={handleMenuOpen}
                    >
                        <MoreIcon />
                    </IconButton>
                )}

                <Menu
                    anchorEl={anchorEl}
                    open={Boolean(anchorEl)}
                    onClose={handleMenuClose}
                >
                    <MenuItem onClick={() => {/* Handle search */}}>
                        <SearchIcon sx={{ mr: 1 }} />
                        Search
                    </MenuItem>
                    <MenuItem onClick={() => {/* Handle notifications */}}>
                        <NotificationsIcon sx={{ mr: 1 }} />
                        Notifications
                    </MenuItem>
                    <MenuItem onClick={toggleTheme}>
                        {isDarkMode ? (
                            <>
                                <LightModeIcon sx={{ mr: 1 }} />
                                Light Mode
                            </>
                        ) : (
                            <>
                                <DarkModeIcon sx={{ mr: 1 }} />
                                Dark Mode
                            </>
                        )}
                    </MenuItem>
                </Menu>
            </MuiToolbar>
        </AppBar>
    );
};

export default Toolbar; 