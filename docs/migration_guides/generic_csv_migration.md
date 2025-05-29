# Generic CSV Migration Guide

This guide provides instructions for migrating data from generic CSV files to the Ontario Driving School Manager.

## Prerequisites

- Python 3.9 or higher
- CSV files with data to import
- Field mapping configuration
- Required Python packages installed:
  ```bash
  pip install pandas sqlalchemy pydantic jinja2
  ```

## CSV Format Requirements

1. File Format:
   - UTF-8 encoding
   - Comma-separated values
   - First row contains headers
   - No special characters in headers

2. Required Fields:
   - See field mapping section for required fields
   - All required fields must be present
   - Field names must match mapping

3. Data Types:
   - Dates: YYYY-MM-DD format
   - Numbers: No currency symbols
   - Text: No special formatting
   - Boolean: true/false or 1/0

## Field Mapping Configuration

1. Create a field mapping file (JSON format):
   ```json
   {
     "csv_field_name": "model_field_name",
     "FirstName": "first_name",
     "LastName": "last_name",
     "Email": "email"
   }
   ```

2. Required mappings for each entity type:

   ### Students
   ```json
   {
     "FirstName": "first_name",
     "LastName": "last_name",
     "Email": "email",
     "Phone": "phone",
     "Address": "address",
     "City": "city",
     "Province": "province",
     "PostalCode": "postal_code",
     "DateOfBirth": "date_of_birth",
     "LicenseNumber": "license_number"
   }
   ```

   ### Instructors
   ```json
   {
     "FirstName": "first_name",
     "LastName": "last_name",
     "Email": "email",
     "Phone": "phone",
     "LicenseNumber": "license_number",
     "CertificationNumber": "certification_number"
   }
   ```

   ### Vehicles
   ```json
   {
     "Make": "make",
     "Model": "model",
     "Year": "year",
     "LicensePlate": "license_plate",
     "VIN": "vin",
     "InspectionDate": "inspection_date"
   }
   ```

## Data Import

1. Prepare the import:
   ```bash
   # Create reports directory
   mkdir -p reports
   
   # Run import script
   python scripts/import_competitor_data.py /path/to/csv/file \
     --type csv \
     --field-mapping /path/to/mapping.json \
     --output-dir reports
   ```

2. Monitor the import:
   - Check the console output for progress
   - Review the generated report in the reports directory
   - Address any errors or warnings

## Data Validation

1. Validate imported data:
   ```bash
   python scripts/validate_imported_data.py --output-dir reports
   ```

2. Review validation results:
   - Check validation reports in the reports directory
   - Address any validation errors
   - Verify data integrity

## Data Cleaning

Before import, ensure your CSV data is clean:

1. Remove special characters
2. Standardize date formats
3. Validate email addresses
4. Format phone numbers
5. Check for duplicates

## Troubleshooting

### Common Issues

1. **CSV Format Issues**
   - Check file encoding
   - Verify delimiter
   - Remove BOM if present
   - Check line endings

2. **Field Mapping Issues**
   - Verify field names match exactly
   - Check for typos
   - Ensure all required fields are mapped

3. **Data Validation Issues**
   - Check date formats
   - Verify email formats
   - Validate phone numbers
   - Check for required fields

### Error Messages

- **"Invalid CSV format"**: CSV file is not properly formatted
- **"Missing required field"**: Required field is missing in CSV
- **"Invalid data type"**: Data does not match expected type
- **"Duplicate record"**: Record already exists in database

## Best Practices

1. **Data Preparation**
   - Clean data before import
   - Validate CSV format
   - Check field mappings
   - Test with sample data

2. **Import Process**
   - Use small batches for large files
   - Monitor progress
   - Check logs regularly
   - Backup before import

3. **Post-Import**
   - Verify data integrity
   - Check relationships
   - Test functionality
   - Archive original files

## Support

For additional support:
1. Check the error logs in the reports directory
2. Review the validation reports
3. Contact support with specific error messages

## Post-Migration

After successful migration:
1. Verify all data is imported correctly
2. Check relationships between records
3. Test system functionality
4. Archive original CSV files 