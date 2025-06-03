/**
 * ErrorDialog component.
 * A reusable dialog for displaying error messages.
 */

import React from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogContentText,
    DialogActions,
    Button,
    IconButton
} from '@mui/material';
import { Close as CloseIcon } from '@mui/icons-material';
import { styled } from '@mui/material/styles';

const CloseButton = styled(IconButton)(({ theme }) => ({
    position: 'absolute',
    right: theme.spacing(1),
    top: theme.spacing(1)
}));

const ErrorDialog = ({
    open,
    title = 'Error',
    message,
    details,
    onClose,
    showDetails = false
}) => {
    const [showFullDetails, setShowFullDetails] = React.useState(false);

    const handleClose = () => {
        setShowFullDetails(false);
        onClose();
    };

    return (
        <Dialog
            open={open}
            onClose={handleClose}
            aria-labelledby="error-dialog-title"
            aria-describedby="error-dialog-description"
            maxWidth="sm"
            fullWidth
        >
            <DialogTitle id="error-dialog-title">
                {title}
                <CloseButton
                    aria-label="close"
                    onClick={handleClose}
                    size="small"
                >
                    <CloseIcon />
                </CloseButton>
            </DialogTitle>
            <DialogContent>
                <DialogContentText id="error-dialog-description">
                    {message}
                </DialogContentText>
                {showDetails && details && (
                    <>
                        <Button
                            onClick={() => setShowFullDetails(!showFullDetails)}
                            color="primary"
                            size="small"
                            sx={{ mt: 2 }}
                        >
                            {showFullDetails ? 'Hide Details' : 'Show Details'}
                        </Button>
                        {showFullDetails && (
                            <DialogContentText
                                sx={{
                                    mt: 2,
                                    p: 2,
                                    bgcolor: 'background.default',
                                    borderRadius: 1,
                                    fontFamily: 'monospace',
                                    whiteSpace: 'pre-wrap'
                                }}
                            >
                                {details}
                            </DialogContentText>
                        )}
                    </>
                )}
            </DialogContent>
            <DialogActions>
                <Button onClick={handleClose} color="primary" variant="contained">
                    Close
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default ErrorDialog; 