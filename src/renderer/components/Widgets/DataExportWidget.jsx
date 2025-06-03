/**
 * DataExportWidget component.
 * A reusable component for exporting data in various formats with customizable options.
 */

import React, { useState } from 'react';
import {
    Box,
    Button,
    Menu,
    MenuItem,
    ListItemIcon,
    ListItemText,
    IconButton,
    Tooltip,
    CircularProgress,
    useTheme,
    useMediaQuery
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
    FileDownload as FileDownloadIcon,
    PictureAsPdf as PdfIcon,
    TableChart as ExcelIcon,
    Description as CsvIcon,
    Code as JsonIcon
} from '@mui/icons-material';

const ExportButton = styled(Button)(({ theme }) => ({
    [theme.breakpoints.down('sm')]: {
        minWidth: 'auto',
        padding: theme.spacing(1)
    }
}));

const DataExportWidget = ({
    onExport,
    formats = ['csv', 'excel', 'pdf', 'json'],
    disabled = false,
    loading = false,
    size = 'medium',
    variant = 'outlined',
    showIcon = true,
    showLabel = true,
    label = 'Export',
    tooltip = 'Export Data'
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

    const handleExport = async (format) => {
        try {
            await onExport(format);
        } finally {
            handleClose();
        }
    };

    const getFormatIcon = (format) => {
        switch (format) {
            case 'pdf':
                return <PdfIcon />;
            case 'excel':
                return <ExcelIcon />;
            case 'csv':
                return <CsvIcon />;
            case 'json':
                return <JsonIcon />;
            default:
                return <FileDownloadIcon />;
        }
    };

    const getFormatLabel = (format) => {
        return format.charAt(0).toUpperCase() + format.slice(1);
    };

    const buttonContent = (
        <>
            {showIcon && (loading ? <CircularProgress size={20} /> : <FileDownloadIcon />)}
            {showLabel && !isMobile && <Box component="span" sx={{ ml: 1 }}>{label}</Box>}
        </>
    );

    return (
        <Box>
            <Tooltip title={tooltip}>
                <span>
                    <ExportButton
                        variant={variant}
                        size={size}
                        onClick={handleClick}
                        disabled={disabled || loading}
                        startIcon={showIcon ? null : <FileDownloadIcon />}
                    >
                        {buttonContent}
                    </ExportButton>
                </span>
            </Tooltip>

            <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleClose}
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'right'
                }}
                transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right'
                }}
            >
                {formats.map((format) => (
                    <MenuItem
                        key={format}
                        onClick={() => handleExport(format)}
                        disabled={disabled || loading}
                    >
                        <ListItemIcon>
                            {getFormatIcon(format)}
                        </ListItemIcon>
                        <ListItemText>
                            Export as {getFormatLabel(format)}
                        </ListItemText>
                    </MenuItem>
                ))}
            </Menu>
        </Box>
    );
};

export default DataExportWidget; 