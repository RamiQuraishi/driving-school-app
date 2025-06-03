/**
 * FilterWidget component.
 * A reusable filter component with multiple filter criteria.
 */

import React, { useState, useEffect } from 'react';
import {
    Box,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Chip,
    IconButton,
    Tooltip,
    Popover,
    Button,
    Divider,
    Typography
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
    FilterList as FilterIcon,
    Clear as ClearIcon
} from '@mui/icons-material';

const FilterContainer = styled(Box)(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    gap: theme.spacing(1)
}));

const FilterChip = styled(Chip)(({ theme }) => ({
    margin: theme.spacing(0.5)
}));

const FilterWidget = ({
    filters = {},
    options = {},
    onChange,
    disabled = false,
    size = 'medium',
    variant = 'outlined'
}) => {
    const [anchorEl, setAnchorEl] = useState(null);
    const [localFilters, setLocalFilters] = useState(filters);

    useEffect(() => {
        setLocalFilters(filters);
    }, [filters]);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleFilterChange = (filterKey, value) => {
        const newFilters = {
            ...localFilters,
            [filterKey]: value
        };
        setLocalFilters(newFilters);
    };

    const handleApply = () => {
        onChange(localFilters);
        handleClose();
    };

    const handleClear = () => {
        const clearedFilters = Object.keys(localFilters).reduce((acc, key) => ({
            ...acc,
            [key]: 'all'
        }), {});
        setLocalFilters(clearedFilters);
        onChange(clearedFilters);
    };

    const hasActiveFilters = Object.values(localFilters).some(value => value !== 'all');

    const open = Boolean(anchorEl);

    return (
        <FilterContainer>
            <Tooltip title="Filters">
                <IconButton
                    onClick={handleClick}
                    disabled={disabled}
                    color={hasActiveFilters ? 'primary' : 'default'}
                >
                    <FilterIcon />
                </IconButton>
            </Tooltip>

            {hasActiveFilters && (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {Object.entries(localFilters).map(([key, value]) => {
                        if (value === 'all') return null;
                        const option = options[key]?.find(opt => opt.value === value);
                        return (
                            <FilterChip
                                key={key}
                                label={`${key}: ${option?.label || value}`}
                                onDelete={() => handleFilterChange(key, 'all')}
                                size="small"
                            />
                        );
                    })}
                </Box>
            )}

            <Popover
                open={open}
                anchorEl={anchorEl}
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
                <Box sx={{ p: 2, minWidth: 300 }}>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                        <Typography variant="subtitle1">Filters</Typography>
                        {hasActiveFilters && (
                            <Button
                                size="small"
                                startIcon={<ClearIcon />}
                                onClick={handleClear}
                            >
                                Clear All
                            </Button>
                        )}
                    </Box>

                    <Divider sx={{ mb: 2 }} />

                    {Object.entries(options).map(([key, filterOptions]) => (
                        <FormControl
                            key={key}
                            fullWidth
                            size={size}
                            variant={variant}
                            sx={{ mb: 2 }}
                        >
                            <InputLabel>{key.charAt(0).toUpperCase() + key.slice(1)}</InputLabel>
                            <Select
                                value={localFilters[key] || 'all'}
                                onChange={(e) => handleFilterChange(key, e.target.value)}
                                label={key.charAt(0).toUpperCase() + key.slice(1)}
                            >
                                {filterOptions.map((option) => (
                                    <MenuItem key={option.value} value={option.value}>
                                        {option.label}
                                    </MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    ))}

                    <Box display="flex" justifyContent="flex-end" gap={1} mt={2}>
                        <Button onClick={handleClose}>
                            Cancel
                        </Button>
                        <Button
                            variant="contained"
                            onClick={handleApply}
                            disabled={!hasActiveFilters}
                        >
                            Apply
                        </Button>
                    </Box>
                </Box>
            </Popover>
        </FilterContainer>
    );
};

export default FilterWidget; 