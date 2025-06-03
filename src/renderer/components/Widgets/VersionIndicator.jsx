/**
 * VersionIndicator component.
 * Displays record versions and change history with a clean, interactive interface.
 */

import React, { useState } from 'react';
import {
    Box,
    IconButton,
    Tooltip,
    Popover,
    Typography,
    List,
    ListItem,
    ListItemText,
    ListItemIcon,
    Divider,
    Chip,
    useTheme,
    useMediaQuery
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
    History as HistoryIcon,
    Restore as RestoreIcon,
    Compare as CompareIcon,
    Person as PersonIcon,
    AccessTime as TimeIcon
} from '@mui/icons-material';

const VersionChip = styled(Chip)(({ theme }) => ({
    marginLeft: theme.spacing(1)
}));

const VersionIndicator = ({
    versions = [],
    currentVersion,
    onVersionSelect,
    onCompare,
    onRestore,
    disabled = false,
    size = 'medium'
}) => {
    const [anchorEl, setAnchorEl] = useState(null);
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleVersionSelect = (version) => {
        onVersionSelect(version);
        handleClose();
    };

    const handleCompare = (version) => {
        onCompare(version);
        handleClose();
    };

    const handleRestore = (version) => {
        onRestore(version);
        handleClose();
    };

    const formatDate = (date) => {
        return new Date(date).toLocaleString();
    };

    const getVersionStatus = (version) => {
        if (version.id === currentVersion) return 'Current';
        if (version.isLatest) return 'Latest';
        return 'Previous';
    };

    const getVersionColor = (version) => {
        if (version.id === currentVersion) return 'primary';
        if (version.isLatest) return 'success';
        return 'default';
    };

    return (
        <Box>
            <Tooltip title="Version History">
                <span>
                    <IconButton
                        onClick={handleClick}
                        disabled={disabled}
                        size={size}
                        color="primary"
                    >
                        <HistoryIcon />
                    </IconButton>
                </span>
            </Tooltip>

            <Popover
                open={Boolean(anchorEl)}
                anchorEl={anchorEl}
                onClose={handleClose}
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'right'
                }}
                transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right'
                }}
                PaperProps={{
                    sx: {
                        minWidth: isMobile ? '100%' : 400,
                        maxHeight: 400
                    }
                }}
            >
                <Box sx={{ p: 2 }}>
                    <Typography variant="subtitle1" gutterBottom>
                        Version History
                    </Typography>
                    <List>
                        {versions.map((version, index) => (
                            <React.Fragment key={version.id}>
                                {index > 0 && <Divider />}
                                <ListItem
                                    secondaryAction={
                                        <Box>
                                            {version.id !== currentVersion && (
                                                <>
                                                    <Tooltip title="Compare">
                                                        <IconButton
                                                            edge="end"
                                                            onClick={() => handleCompare(version)}
                                                            size="small"
                                                        >
                                                            <CompareIcon />
                                                        </IconButton>
                                                    </Tooltip>
                                                    <Tooltip title="Restore">
                                                        <IconButton
                                                            edge="end"
                                                            onClick={() => handleRestore(version)}
                                                            size="small"
                                                        >
                                                            <RestoreIcon />
                                                        </IconButton>
                                                    </Tooltip>
                                                </>
                                            )}
                                        </Box>
                                    }
                                >
                                    <ListItemIcon>
                                        <TimeIcon color="action" />
                                    </ListItemIcon>
                                    <ListItemText
                                        primary={
                                            <Box display="flex" alignItems="center">
                                                <Typography variant="body2">
                                                    {formatDate(version.timestamp)}
                                                </Typography>
                                                <VersionChip
                                                    label={getVersionStatus(version)}
                                                    size="small"
                                                    color={getVersionColor(version)}
                                                />
                                            </Box>
                                        }
                                        secondary={
                                            <Box>
                                                <Typography variant="caption" display="block">
                                                    Modified by: {version.modifiedBy}
                                                </Typography>
                                                <Typography variant="caption" color="textSecondary">
                                                    {version.changes}
                                                </Typography>
                                            </Box>
                                        }
                                    />
                                </ListItem>
                            </React.Fragment>
                        ))}
                    </List>
                </Box>
            </Popover>
        </Box>
    );
};

export default VersionIndicator; 