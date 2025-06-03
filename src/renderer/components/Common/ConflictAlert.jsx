/**
 * ConflictAlert component for displaying and resolving sync conflicts.
 * Shows conflicts between local and remote changes.
 */

import React, { useState } from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    Typography,
    Box,
    List,
    ListItem,
    ListItemText,
    ListItemIcon,
    Radio,
    useTheme
} from '@mui/material';
import {
    SyncProblem as ConflictIcon,
    CloudDownload as RemoteIcon,
    Computer as LocalIcon
} from '@mui/icons-material';

const ConflictAlert = ({ conflicts, onResolve, onDismiss }) => {
    const theme = useTheme();
    const [selectedVersions, setSelectedVersions] = useState({});

    const handleVersionSelect = (conflictId, version) => {
        setSelectedVersions(prev => ({
            ...prev,
            [conflictId]: version
        }));
    };

    const handleResolve = () => {
        const resolutions = Object.entries(selectedVersions).map(([conflictId, version]) => ({
            conflictId,
            version
        }));
        onResolve(resolutions);
    };

    const getConflictDetails = (conflict) => {
        switch (conflict.type) {
            case 'student':
                return `Student: ${conflict.data.name}`;
            case 'lesson':
                return `Lesson: ${conflict.data.title}`;
            case 'school':
                return `School: ${conflict.data.name}`;
            default:
                return 'Unknown conflict type';
        }
    };

    return (
        <Dialog
            open={conflicts.length > 0}
            onClose={onDismiss}
            maxWidth="md"
            fullWidth
        >
            <DialogTitle>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <ConflictIcon color="warning" />
                    <Typography variant="h6">
                        Sync Conflicts Detected
                    </Typography>
                </Box>
            </DialogTitle>
            <DialogContent>
                <Typography variant="body1" paragraph>
                    The following items have conflicting changes. Please choose which version to keep:
                </Typography>
                <List>
                    {conflicts.map((conflict) => (
                        <ListItem
                            key={conflict.id}
                            divider
                            sx={{
                                flexDirection: 'column',
                                alignItems: 'stretch',
                                gap: 1
                            }}
                        >
                            <Typography variant="subtitle1" color="primary">
                                {getConflictDetails(conflict)}
                            </Typography>
                            <Box sx={{ display: 'flex', gap: 2 }}>
                                <Box
                                    sx={{
                                        flex: 1,
                                        p: 2,
                                        border: `1px solid ${theme.palette.divider}`,
                                        borderRadius: 1
                                    }}
                                >
                                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                                        <LocalIcon color="primary" />
                                        <Typography variant="subtitle2">Local Version</Typography>
                                    </Box>
                                    <Radio
                                        checked={selectedVersions[conflict.id] === 'local'}
                                        onChange={() => handleVersionSelect(conflict.id, 'local')}
                                    />
                                    <Typography variant="body2" color="text.secondary">
                                        Last modified: {new Date(conflict.local.timestamp).toLocaleString()}
                                    </Typography>
                                </Box>
                                <Box
                                    sx={{
                                        flex: 1,
                                        p: 2,
                                        border: `1px solid ${theme.palette.divider}`,
                                        borderRadius: 1
                                    }}
                                >
                                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                                        <RemoteIcon color="secondary" />
                                        <Typography variant="subtitle2">Remote Version</Typography>
                                    </Box>
                                    <Radio
                                        checked={selectedVersions[conflict.id] === 'remote'}
                                        onChange={() => handleVersionSelect(conflict.id, 'remote')}
                                    />
                                    <Typography variant="body2" color="text.secondary">
                                        Last modified: {new Date(conflict.remote.timestamp).toLocaleString()}
                                    </Typography>
                                </Box>
                            </Box>
                        </ListItem>
                    ))}
                </List>
            </DialogContent>
            <DialogActions>
                <Button onClick={onDismiss}>
                    Cancel
                </Button>
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleResolve}
                    disabled={Object.keys(selectedVersions).length !== conflicts.length}
                >
                    Resolve Conflicts
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default ConflictAlert; 