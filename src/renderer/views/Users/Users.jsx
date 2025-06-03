/**
 * Users view component.
 * Manages user accounts, roles, and permissions.
 */

import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
    Box,
    Container,
    Grid,
    Paper,
    Typography,
    Button,
    IconButton,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TablePagination,
    Chip,
    useTheme,
    useMediaQuery
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
    Add as AddIcon,
    Edit as EditIcon,
    Delete as DeleteIcon,
    Block as BlockIcon,
    CheckCircle as CheckCircleIcon
} from '@mui/icons-material';
import { LoadingSpinner } from '../../components/Common';
import { SearchWidget } from '../../components/Widgets/SearchWidget';
import { FilterWidget } from '../../components/Widgets/FilterWidget';
import { ConfirmDialog } from '../../components/Dialogs/ConfirmDialog';
import { ErrorDialog } from '../../components/Dialogs/ErrorDialog';
import { fetchUsers, deleteUser, updateUserStatus } from '../../store/actions';

// Styled components
const UsersContainer = styled(Container)(({ theme }) => ({
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4)
}));

const ActionButton = styled(IconButton)(({ theme }) => ({
    marginLeft: theme.spacing(1)
}));

const StatusChip = styled(Chip)(({ theme, status }) => ({
    backgroundColor: status === 'active' 
        ? theme.palette.success.light 
        : theme.palette.error.light,
    color: status === 'active' 
        ? theme.palette.success.contrastText 
        : theme.palette.error.contrastText
}));

const Users = () => {
    const theme = useTheme();
    const dispatch = useDispatch();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    const { data, isLoading, error } = useSelector(state => state.users);
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [searchQuery, setSearchQuery] = useState('');
    const [filters, setFilters] = useState({
        role: 'all',
        status: 'all'
    });
    const [confirmDialog, setConfirmDialog] = useState({
        open: false,
        title: '',
        message: '',
        onConfirm: null
    });
    const [errorDialog, setErrorDialog] = useState({
        open: false,
        message: ''
    });

    useEffect(() => {
        dispatch(fetchUsers());
    }, [dispatch]);

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    const handleSearch = (query) => {
        setSearchQuery(query);
        setPage(0);
    };

    const handleFilterChange = (newFilters) => {
        setFilters(newFilters);
        setPage(0);
    };

    const handleDeleteUser = async (userId) => {
        try {
            await dispatch(deleteUser(userId)).unwrap();
        } catch (error) {
            setErrorDialog({
                open: true,
                message: error.message || 'Failed to delete user'
            });
        }
    };

    const handleStatusChange = async (userId, newStatus) => {
        try {
            await dispatch(updateUserStatus({ userId, status: newStatus })).unwrap();
        } catch (error) {
            setErrorDialog({
                open: true,
                message: error.message || 'Failed to update user status'
            });
        }
    };

    const filteredUsers = data?.filter(user => {
        const matchesSearch = user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            user.email.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesRole = filters.role === 'all' || user.role === filters.role;
        const matchesStatus = filters.status === 'all' || user.status === filters.status;
        return matchesSearch && matchesRole && matchesStatus;
    });

    if (isLoading) {
        return <LoadingSpinner />;
    }

    if (error) {
        return (
            <Box sx={{ p: 3 }}>
                <Typography color="error">{error}</Typography>
            </Box>
        );
    }

    return (
        <UsersContainer maxWidth="lg">
            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
                        <Typography variant="h4" component="h1">
                            Users
                        </Typography>
                        <Button
                            variant="contained"
                            color="primary"
                            startIcon={<AddIcon />}
                            onClick={() => {/* Handle add user */}}
                        >
                            Add User
                        </Button>
                    </Box>
                </Grid>

                <Grid item xs={12}>
                    <Paper elevation={2} sx={{ p: 2, mb: 3 }}>
                        <Grid container spacing={2}>
                            <Grid item xs={12} md={6}>
                                <SearchWidget
                                    placeholder="Search users..."
                                    onSearch={handleSearch}
                                />
                            </Grid>
                            <Grid item xs={12} md={6}>
                                <FilterWidget
                                    filters={filters}
                                    onChange={handleFilterChange}
                                    options={{
                                        role: [
                                            { value: 'all', label: 'All Roles' },
                                            { value: 'admin', label: 'Administrator' },
                                            { value: 'instructor', label: 'Instructor' },
                                            { value: 'student', label: 'Student' }
                                        ],
                                        status: [
                                            { value: 'all', label: 'All Status' },
                                            { value: 'active', label: 'Active' },
                                            { value: 'inactive', label: 'Inactive' }
                                        ]
                                    }}
                                />
                            </Grid>
                        </Grid>
                    </Paper>
                </Grid>

                <Grid item xs={12}>
                    <TableContainer component={Paper}>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell>Name</TableCell>
                                    <TableCell>Email</TableCell>
                                    <TableCell>Role</TableCell>
                                    <TableCell>Status</TableCell>
                                    <TableCell>Last Login</TableCell>
                                    <TableCell align="right">Actions</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {filteredUsers
                                    ?.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                                    .map((user) => (
                                        <TableRow key={user.id}>
                                            <TableCell>{user.name}</TableCell>
                                            <TableCell>{user.email}</TableCell>
                                            <TableCell>
                                                <Chip
                                                    label={user.role}
                                                    size="small"
                                                    color="primary"
                                                    variant="outlined"
                                                />
                                            </TableCell>
                                            <TableCell>
                                                <StatusChip
                                                    label={user.status}
                                                    status={user.status}
                                                    size="small"
                                                />
                                            </TableCell>
                                            <TableCell>
                                                {new Date(user.lastLogin).toLocaleString()}
                                            </TableCell>
                                            <TableCell align="right">
                                                <ActionButton
                                                    color="primary"
                                                    onClick={() => {/* Handle edit */}}
                                                >
                                                    <EditIcon />
                                                </ActionButton>
                                                <ActionButton
                                                    color={user.status === 'active' ? 'error' : 'success'}
                                                    onClick={() => handleStatusChange(
                                                        user.id,
                                                        user.status === 'active' ? 'inactive' : 'active'
                                                    )}
                                                >
                                                    {user.status === 'active' ? <BlockIcon /> : <CheckCircleIcon />}
                                                </ActionButton>
                                                <ActionButton
                                                    color="error"
                                                    onClick={() => setConfirmDialog({
                                                        open: true,
                                                        title: 'Delete User',
                                                        message: `Are you sure you want to delete ${user.name}?`,
                                                        onConfirm: () => handleDeleteUser(user.id)
                                                    })}
                                                >
                                                    <DeleteIcon />
                                                </ActionButton>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                            </TableBody>
                        </Table>
                        <TablePagination
                            rowsPerPageOptions={[5, 10, 25]}
                            component="div"
                            count={filteredUsers?.length || 0}
                            rowsPerPage={rowsPerPage}
                            page={page}
                            onPageChange={handleChangePage}
                            onRowsPerPageChange={handleChangeRowsPerPage}
                        />
                    </TableContainer>
                </Grid>
            </Grid>

            <ConfirmDialog
                open={confirmDialog.open}
                title={confirmDialog.title}
                message={confirmDialog.message}
                onConfirm={() => {
                    confirmDialog.onConfirm?.();
                    setConfirmDialog({ ...confirmDialog, open: false });
                }}
                onCancel={() => setConfirmDialog({ ...confirmDialog, open: false })}
            />

            <ErrorDialog
                open={errorDialog.open}
                message={errorDialog.message}
                onClose={() => setErrorDialog({ ...errorDialog, open: false })}
            />
        </UsersContainer>
    );
};

export default Users; 