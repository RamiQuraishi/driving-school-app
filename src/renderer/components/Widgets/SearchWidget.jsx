/**
 * SearchWidget component.
 * A reusable search input with debouncing and clear functionality.
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
    TextField,
    InputAdornment,
    IconButton,
    Box,
    CircularProgress
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
    Search as SearchIcon,
    Clear as ClearIcon
} from '@mui/icons-material';
import debounce from 'lodash/debounce';

const SearchContainer = styled(Box)(({ theme }) => ({
    position: 'relative',
    width: '100%'
}));

const SearchWidget = ({
    placeholder = 'Search...',
    onSearch,
    debounceTime = 300,
    minLength = 2,
    initialValue = '',
    loading = false,
    disabled = false,
    fullWidth = true,
    size = 'medium',
    variant = 'outlined'
}) => {
    const [searchValue, setSearchValue] = useState(initialValue);
    const [isSearching, setIsSearching] = useState(false);

    // Debounced search function
    const debouncedSearch = useCallback(
        debounce((value) => {
            if (value.length >= minLength || value.length === 0) {
                onSearch(value);
            }
            setIsSearching(false);
        }, debounceTime),
        [onSearch, minLength, debounceTime]
    );

    // Handle search value changes
    const handleSearchChange = (event) => {
        const value = event.target.value;
        setSearchValue(value);
        setIsSearching(true);
        debouncedSearch(value);
    };

    // Clear search
    const handleClear = () => {
        setSearchValue('');
        onSearch('');
    };

    // Cleanup debounce on unmount
    useEffect(() => {
        return () => {
            debouncedSearch.cancel();
        };
    }, [debouncedSearch]);

    return (
        <SearchContainer>
            <TextField
                fullWidth={fullWidth}
                size={size}
                variant={variant}
                placeholder={placeholder}
                value={searchValue}
                onChange={handleSearchChange}
                disabled={disabled || loading}
                InputProps={{
                    startAdornment: (
                        <InputAdornment position="start">
                            {loading || isSearching ? (
                                <CircularProgress size={20} />
                            ) : (
                                <SearchIcon color="action" />
                            )}
                        </InputAdornment>
                    ),
                    endAdornment: searchValue && (
                        <InputAdornment position="end">
                            <IconButton
                                size="small"
                                onClick={handleClear}
                                disabled={disabled || loading}
                            >
                                <ClearIcon />
                            </IconButton>
                        </InputAdornment>
                    )
                }}
            />
        </SearchContainer>
    );
};

export default SearchWidget; 