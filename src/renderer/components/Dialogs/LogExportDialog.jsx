/**
 * LogExportDialog component.
 * Handles exporting application logs for support purposes.
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
    FormControl,
    FormControlLabel,
    Checkbox,
    TextField,
    Select,
    MenuItem,
    InputLabel,
    Divider,
    Alert,
    IconButton,
    CircularProgress
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
    Close as CloseIcon,
    Download as DownloadIcon,
    Description as DescriptionIcon
} from '@mui/icons-material';

const CloseButton = styled(IconButton)(({ theme }) => ({
    position: 'absolute',
    right: theme.spacing(1),
    top: theme.spacing(1)
}));

const LogExportDialog = ({
    open,
    onClose,
    onExport,
    logLevels = ['ERROR', 'WARN', 'INFO', 'DEBUG'],
    defaultLogLevel = 'INFO',
    defaultIncludeSystemInfo = true,
    defaultIncludePerformance = true,
    defaultIncludeTelemetry = false
}) => {
    const [logLevel, setLogLevel] = useState(defaultLogLevel);
    const [includeSystemInfo, setIncludeSystemInfo] = useState(defaultIncludeSystemInfo);
    const [includePerformance, setIncludePerformance] = useState(defaultIncludePerformance);
    const [includeTelemetry, setIncludeTelemetry] = useState(defaultIncludeTelemetry);
    const [description, setDescription] = useState('');
    const [isExporting, setIsExporting] = useState(false);
    const [error, setError] = useState(null);

    const handleExport = async () => {
        try {
            setIsExporting(true);
            setError(null);
            await onExport({
                logLevel,
                includeSystemInfo,
                includePerformance,
                includeTelemetry,
                description
            });
            onClose();
        } catch (err) {
            setError(err.message || 'Failed to export logs');
        } finally {
            setIsExporting(false);
        }
    };

    return (
        <Dialog
            open={open}
            onClose={onClose}
            aria-labelledby="log-export-dialog-title"
            maxWidth="sm"
            fullWidth
        >
            <DialogTitle id="log-export-dialog-title">
                Export Logs
                <CloseButton
                    aria-label="close"
                    onClick={onClose}
                    size="small"
                >
                    <CloseIcon />
                </CloseButton>
            </DialogTitle>
            <DialogContent>
                <Alert severity="info" sx={{ mb: 3 }}>
                    Export application logs for troubleshooting and support purposes.
                    Choose what information to include in the export.
                </Alert>

                <Box mb={3}>
                    <FormControl fullWidth sx={{ mb: 2 }}>
                        <InputLabel>Log Level</InputLabel>
                        <Select
                            value={logLevel}
                            onChange={(e) => setLogLevel(e.target.value)}
                            label="Log Level"
                        >
                            {logLevels.map((level) => (
                                <MenuItem key={level} value={level}>
                                    {level}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={includeSystemInfo}
                                onChange={(e) => setIncludeSystemInfo(e.target.checked)}
                            />
                        }
                        label="Include System Information"
                    />
                    <Typography variant="caption" color="textSecondary" display="block">
                        Operating system, hardware, and environment details
                    </Typography>

                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={includePerformance}
                                onChange={(e) => setIncludePerformance(e.target.checked)}
                            />
                        }
                        label="Include Performance Metrics"
                    />
                    <Typography variant="caption" color="textSecondary" display="block">
                        CPU, memory, and network usage statistics
                    </Typography>

                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={includeTelemetry}
                                onChange={(e) => setIncludeTelemetry(e.target.checked)}
                            />
                        }
                        label="Include Telemetry Data"
                    />
                    <Typography variant="caption" color="textSecondary" display="block">
                        Usage patterns and feature analytics
                    </Typography>
                </Box>

                <Divider sx={{ my: 2 }} />

                <TextField
                    fullWidth
                    multiline
                    rows={3}
                    label="Description"
                    placeholder="Describe the issue or reason for exporting logs..."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    InputProps={{
                        startAdornment: <DescriptionIcon color="action" sx={{ mr: 1 }} />
                    }}
                />

                {error && (
                    <Alert severity="error" sx={{ mt: 2 }}>
                        {error}
                    </Alert>
                )}
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose} color="inherit">
                    Cancel
                </Button>
                <Button
                    onClick={handleExport}
                    color="primary"
                    variant="contained"
                    startIcon={isExporting ? <CircularProgress size={20} /> : <DownloadIcon />}
                    disabled={isExporting}
                >
                    {isExporting ? 'Exporting...' : 'Export Logs'}
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default LogExportDialog; 