/**
 * PaginationWidget component.
 * A reusable pagination component with customizable options and responsive design.
 */

import React from 'react';
import {
    Box,
    TablePagination,
    IconButton,
    Tooltip,
    useTheme,
    useMediaQuery
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
    FirstPage as FirstPageIcon,
    LastPage as LastPageIcon,
    KeyboardArrowLeft as KeyboardArrowLeftIcon,
    KeyboardArrowRight as KeyboardArrowRightIcon
} from '@mui/icons-material';

const PaginationContainer = styled(Box)(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(1),
    [theme.breakpoints.down('sm')]: {
        justifyContent: 'center'
    }
}));

const PaginationWidget = ({
    count,
    page,
    rowsPerPage,
    onPageChange,
    onRowsPerPageChange,
    rowsPerPageOptions = [5, 10, 25, 50],
    labelRowsPerPage = 'Rows per page:',
    labelDisplayedRows = ({ from, to, count }) => `${from}-${to} of ${count}`,
    showFirstLastButtons = true,
    disabled = false,
    size = 'medium'
}) => {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

    const handleFirstPageButtonClick = () => {
        onPageChange(0);
    };

    const handleBackButtonClick = () => {
        onPageChange(page - 1);
    };

    const handleNextButtonClick = () => {
        onPageChange(page + 1);
    };

    const handleLastPageButtonClick = () => {
        onPageChange(Math.max(0, Math.ceil(count / rowsPerPage) - 1));
    };

    return (
        <PaginationContainer>
            <TablePagination
                component="div"
                count={count}
                page={page}
                onPageChange={(event, newPage) => onPageChange(newPage)}
                rowsPerPage={rowsPerPage}
                onRowsPerPageChange={(event) => onRowsPerPageChange(parseInt(event.target.value, 10))}
                rowsPerPageOptions={rowsPerPageOptions}
                labelRowsPerPage={labelRowsPerPage}
                labelDisplayedRows={labelDisplayedRows}
                size={size}
                disabled={disabled}
                sx={{
                    '.MuiTablePagination-select': {
                        [theme.breakpoints.down('sm')]: {
                            padding: theme.spacing(1)
                        }
                    },
                    '.MuiTablePagination-displayedRows': {
                        [theme.breakpoints.down('sm')]: {
                            margin: 0
                        }
                    }
                }}
                ActionsComponent={({ onPageChange, ...other }) => (
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        {showFirstLastButtons && (
                            <Tooltip title="First Page">
                                <span>
                                    <IconButton
                                        onClick={handleFirstPageButtonClick}
                                        disabled={page === 0 || disabled}
                                        aria-label="first page"
                                        size={size}
                                    >
                                        <FirstPageIcon />
                                    </IconButton>
                                </span>
                            </Tooltip>
                        )}
                        <Tooltip title="Previous Page">
                            <span>
                                <IconButton
                                    onClick={handleBackButtonClick}
                                    disabled={page === 0 || disabled}
                                    aria-label="previous page"
                                    size={size}
                                >
                                    <KeyboardArrowLeftIcon />
                                </IconButton>
                            </span>
                        </Tooltip>
                        <Tooltip title="Next Page">
                            <span>
                                <IconButton
                                    onClick={handleNextButtonClick}
                                    disabled={page >= Math.ceil(count / rowsPerPage) - 1 || disabled}
                                    aria-label="next page"
                                    size={size}
                                >
                                    <KeyboardArrowRightIcon />
                                </IconButton>
                            </span>
                        </Tooltip>
                        {showFirstLastButtons && (
                            <Tooltip title="Last Page">
                                <span>
                                    <IconButton
                                        onClick={handleLastPageButtonClick}
                                        disabled={page >= Math.ceil(count / rowsPerPage) - 1 || disabled}
                                        aria-label="last page"
                                        size={size}
                                    >
                                        <LastPageIcon />
                                    </IconButton>
                                </span>
                            </Tooltip>
                        )}
                    </Box>
                )}
            />
        </PaginationContainer>
    );
};

export default PaginationWidget; 