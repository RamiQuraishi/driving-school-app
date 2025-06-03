/**
 * LogExporter component for exporting application logs.
 * Provides UI for selecting and exporting log files.
 */

import React, { useState, useEffect } from 'react';
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
    ListItemSecondaryAction,
    IconButton,
    Checkbox,
    FormControlLabel,
    TextField,
    useTheme
} from '@mui/material';
import {
    Download as DownloadIcon,
    Delete as DeleteIcon,
    Refresh as RefreshIcon
} from '@mui/icons-material';

const LogExporter = ({ open, onClose }) => {
    const theme = useTheme();
    const [logs, setLogs] = useState([]);
    const [selectedLogs, setSelectedLogs] = useState([]);
    const [dateRange, setDateRange] = useState({
        start: '',
        end: ''
    });
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (open) {
            fetchLogs();
        }
    }, [open]);

    const fetchLogs = async () => {
        setLoading(true);
        try {
            const logFiles = await window.electron.ipcRenderer.invoke('logs:get-files');
            setLogs(logFiles);
        } catch (error) {
            console.error('Failed to fetch logs:', error);
        }
        setLoading(false);
    };

    const handleLogSelect = (logId) => {
        setSelectedLogs(prev =>
            prev.includes(logId)
                ? prev.filter(id => id !== logId)
                : [...prev, logId]
        );
    };

    const handleSelectAll = () => {
        setSelectedLogs(prev =>
            prev.length === logs.length ? [] : logs.map(log => log.id)
        );
    };

    const handleExport = async () => {
        try {
            const exportOptions = {
                logIds: selectedLogs,
                dateRange: dateRange.start && dateRange.end ? dateRange : null
            };

            await window.electron.ipcRenderer.invoke('logs:export', exportOptions);
            onClose();
        } catch (error) {
            console.error('Failed to export logs:', error);
        }
    };

    const handleDelete = async (logId) => {
        try {
            await window.electron.ipcRenderer.invoke('logs:delete', logId);
            fetchLogs();
        } catch (error) {
            console.error('Failed to delete log:', error);
        }
    };

    return (
        <Dialog
            open={open}
            onClose={onClose}
            maxWidth="md"
            fullWidth
        >
            <DialogTitle>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Typography variant="h6">Export Logs</Typography>
                    <IconButton onClick={fetchLogs} disabled={loading}>
                        <RefreshIcon />
                    </IconButton>
                </Box>
            </DialogTitle>
            <DialogContent>
                <Box sx={{ mb: 3 }}>
                    <Typography variant="subtitle1" gutterBottom>
                        Date Range (Optional)
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 2 }}>
                        <TextField
                            label="Start Date"
                            type="date"
                            value={dateRange.start}
                            onChange={(e) => setDateRange(prev => ({ ...prev, start: e.target.value }))}
                            InputLabelProps={{ shrink: true }}
                            fullWidth
                        />
                        <TextField
                            label="End Date"
                            type="date"
                            value={dateRange.end}
                            onChange={(e) => setDateRange(prev => ({ ...prev, end: e.target.value }))}
                            InputLabelProps={{ shrink: true }}
                            fullWidth
                        />
                    </Box>
                </Box>

                <Box sx={{ mb: 2 }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={selectedLogs.length === logs.length}
                                indeterminate={selectedLogs.length > 0 && selectedLogs.length < logs.length}
                                onChange={handleSelectAll}
                            />
                        }
                        label="Select All Logs"
                    />
                </Box>

                <List>
                    {logs.map((log) => (
                        <ListItem
                            key={log.id}
                            divider
                            secondaryAction={
                                <IconButton
                                    edge="end"
                                    onClick={() => handleDelete(log.id)}
                                    disabled={loading}
                                >
                                    <DeleteIcon />
                                </IconButton>
                            }
                        >
                            <Checkbox
                                edge="start"
                                checked={selectedLogs.includes(log.id)}
                                onChange={() => handleLogSelect(log.id)}
                                disabled={loading}
                            />
                            <ListItemText
                                primary={log.name}
                                secondary={
                                    <>
                                        <Typography
                                            component="span"
                                            variant="body2"
                                            color="text.secondary"
                                        >
                                            Size: {log.size}
                                        </Typography>
                                        <br />
                                        <Typography
                                            component="span"
                                            variant="body2"
                                            color="text.secondary"
                                        >
                                            Last modified: {new Date(log.modified).toLocaleString()}
                                        </Typography>
                                    </>
                                }
                            />
                        </ListItem>
                    ))}
                </List>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>
                    Cancel
                </Button>
                <Button
                    variant="contained"
                    color="primary"
                    startIcon={<DownloadIcon />}
                    onClick={handleExport}
                    disabled={selectedLogs.length === 0 || loading}
                >
                    Export Selected
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default LogExporter; 