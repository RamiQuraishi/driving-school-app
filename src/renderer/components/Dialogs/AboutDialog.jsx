/**
 * AboutDialog component.
 * Displays application information, version, and credits.
 */

import React from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    Typography,
    Box,
    Divider,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    IconButton
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
    Close as CloseIcon,
    Code as CodeIcon,
    BugReport as BugReportIcon,
    Security as SecurityIcon,
    Info as InfoIcon
} from '@mui/icons-material';

const CloseButton = styled(IconButton)(({ theme }) => ({
    position: 'absolute',
    right: theme.spacing(1),
    top: theme.spacing(1)
}));

const Logo = styled('img')(({ theme }) => ({
    width: 120,
    height: 120,
    marginBottom: theme.spacing(2)
}));

const AboutDialog = ({
    open,
    onClose,
    appName = 'Rami Drive School',
    version = '1.0.0',
    logo,
    description,
    features = [],
    credits = []
}) => {
    return (
        <Dialog
            open={open}
            onClose={onClose}
            aria-labelledby="about-dialog-title"
            maxWidth="sm"
            fullWidth
        >
            <DialogTitle id="about-dialog-title">
                About {appName}
                <CloseButton
                    aria-label="close"
                    onClick={onClose}
                    size="small"
                >
                    <CloseIcon />
                </CloseButton>
            </DialogTitle>
            <DialogContent>
                <Box
                    display="flex"
                    flexDirection="column"
                    alignItems="center"
                    textAlign="center"
                    mb={3}
                >
                    {logo && <Logo src={logo} alt={`${appName} logo`} />}
                    <Typography variant="h6" gutterBottom>
                        {appName}
                    </Typography>
                    <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                        Version {version}
                    </Typography>
                    {description && (
                        <Typography variant="body2" color="textSecondary" paragraph>
                            {description}
                        </Typography>
                    )}
                </Box>

                <Divider sx={{ my: 2 }} />

                <Typography variant="subtitle1" gutterBottom>
                    Features
                </Typography>
                <List dense>
                    {features.map((feature, index) => (
                        <ListItem key={index}>
                            <ListItemIcon>
                                <InfoIcon color="primary" />
                            </ListItemIcon>
                            <ListItemText primary={feature} />
                        </ListItem>
                    ))}
                </List>

                <Divider sx={{ my: 2 }} />

                <Typography variant="subtitle1" gutterBottom>
                    Credits & Acknowledgments
                </Typography>
                <List dense>
                    {credits.map((credit, index) => (
                        <ListItem key={index}>
                            <ListItemIcon>
                                <CodeIcon color="primary" />
                            </ListItemIcon>
                            <ListItemText
                                primary={credit.name}
                                secondary={credit.role}
                            />
                        </ListItem>
                    ))}
                </List>

                <Box mt={3}>
                    <Typography variant="body2" color="textSecondary" align="center">
                        © {new Date().getFullYear()} {appName}. All rights reserved.
                    </Typography>
                </Box>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose} color="primary" variant="contained">
                    Close
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default AboutDialog; 