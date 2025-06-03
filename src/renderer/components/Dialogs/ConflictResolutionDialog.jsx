/**
 * ConflictResolutionDialog component.
 * Handles data synchronization conflicts between local and remote data.
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
    Divider,
    RadioGroup,
    FormControlLabel,
    Radio,
    Paper,
    IconButton,
    Tooltip
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
    Close as CloseIcon,
    Info as InfoIcon,
    Sync as SyncIcon,
    Storage as StorageIcon,
    Computer as ComputerIcon
} from '@mui/icons-material';

const CloseButton = styled(IconButton)(({ theme }) => ({
    position: 'absolute',
    right: theme.spacing(1),
    top: theme.spacing(1)
}));

const ConflictBox = styled(Paper)(({ theme }) => ({
    padding: theme.spacing(2),
    marginBottom: theme.spacing(2),
    backgroundColor: theme.palette.background.default
}));

const ConflictResolutionDialog = ({
    open,
    onClose,
    conflicts = [],
    onResolve,
    onResolveAll
}) => {
    const [resolutions, setResolutions] = useState({});

    const handleResolutionChange = (conflictId, resolution) => {
        setResolutions(prev => ({
            ...prev,
            [conflictId]: resolution
        }));
    };

    const handleResolve = () => {
        onResolve(resolutions);
        setResolutions({});
    };

    const handleResolveAll = (resolution) => {
        const allResolutions = conflicts.reduce((acc, conflict) => ({
            ...acc,
            [conflict.id]: resolution
        }), {});
        onResolveAll(allResolutions);
        setResolutions({});
    };

    const getConflictTypeIcon = (type) => {
        switch (type) {
            case 'sync':
                return <SyncIcon color="primary" />;
            case 'storage':
                return <StorageIcon color="primary" />;
            default:
                return <ComputerIcon color="primary" />;
        }
    };

    return (
        <Dialog
            open={open}
            onClose={onClose}
            aria-labelledby="conflict-resolution-dialog-title"
            maxWidth="md"
            fullWidth
        >
            <DialogTitle id="conflict-resolution-dialog-title">
                Resolve Conflicts
                <CloseButton
                    aria-label="close"
                    onClick={onClose}
                    size="small"
                >
                    <CloseIcon />
                </CloseButton>
            </DialogTitle>
            <DialogContent>
                <Box mb={3}>
                    <Typography variant="body2" color="textSecondary" paragraph>
                        There are {conflicts.length} conflicts that need to be resolved.
                        Choose which version to keep for each conflict.
                    </Typography>
                    <Box display="flex" gap={1}>
                        <Button
                            variant="outlined"
                            size="small"
                            onClick={() => handleResolveAll('local')}
                            startIcon={<ComputerIcon />}
                        >
                            Keep All Local
                        </Button>
                        <Button
                            variant="outlined"
                            size="small"
                            onClick={() => handleResolveAll('remote')}
                            startIcon={<StorageIcon />}
                        >
                            Keep All Remote
                        </Button>
                    </Box>
                </Box>

                <Divider sx={{ my: 2 }} />

                {conflicts.map((conflict) => (
                    <ConflictBox key={conflict.id} elevation={1}>
                        <Box display="flex" alignItems="center" mb={2}>
                            {getConflictTypeIcon(conflict.type)}
                            <Typography variant="subtitle1" sx={{ ml: 1 }}>
                                {conflict.title}
                            </Typography>
                            <Tooltip title={conflict.description}>
                                <IconButton size="small">
                                    <InfoIcon fontSize="small" />
                                </IconButton>
                            </Tooltip>
                        </Box>

                        <RadioGroup
                            value={resolutions[conflict.id] || ''}
                            onChange={(e) => handleResolutionChange(conflict.id, e.target.value)}
                        >
                            <FormControlLabel
                                value="local"
                                control={<Radio />}
                                label={
                                    <Box>
                                        <Typography variant="body2">
                                            Local Version
                                        </Typography>
                                        <Typography variant="caption" color="textSecondary">
                                            Last modified: {new Date(conflict.local.lastModified).toLocaleString()}
                                        </Typography>
                                    </Box>
                                }
                            />
                            <FormControlLabel
                                value="remote"
                                control={<Radio />}
                                label={
                                    <Box>
                                        <Typography variant="body2">
                                            Remote Version
                                        </Typography>
                                        <Typography variant="caption" color="textSecondary">
                                            Last modified: {new Date(conflict.remote.lastModified).toLocaleString()}
                                        </Typography>
                                    </Box>
                                }
                            />
                        </RadioGroup>

                        <Box mt={2}>
                            <Typography variant="caption" color="textSecondary">
                                Changes:
                            </Typography>
                            <Typography variant="body2" component="pre" sx={{ mt: 1 }}>
                                {JSON.stringify(conflict.diff, null, 2)}
                            </Typography>
                        </Box>
                    </ConflictBox>
                ))}
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose} color="inherit">
                    Cancel
                </Button>
                <Button
                    onClick={handleResolve}
                    color="primary"
                    variant="contained"
                    disabled={Object.keys(resolutions).length !== conflicts.length}
                >
                    Resolve Conflicts
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default ConflictResolutionDialog; 