# Driving School Software Migration Guide

This guide provides instructions for migrating data from Driving School Software to the Ontario Driving School Manager.

## Prerequisites

- Python 3.9 or higher
- Access to Driving School Software database or export files
- Required Python packages installed:
  ```bash
  pip install pandas sqlalchemy pydantic jinja2
  ```

## Data Export

1. Export data from Driving School Software:
   - Log in to Driving School Software
   - Navigate to Reports > Export
   - Select the following data types:
     - Students
     - Instructors
     - Vehicles
     - Lessons
     - Payments
   - Export as CSV files
   - Save files in a dedicated directory

## Data Import

1. Prepare the import:
   ```bash
   # Create reports directory
   mkdir -p reports
   
   # Run import script
   python scripts/import_competitor_data.py /path/to/export/files --type dss --output-dir reports
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

## Field Mapping

The following fields are mapped from Driving School Software to Ontario Driving School Manager:

### Students
| DSS Field | ODSM Field |
|-----------|------------|
| FirstName | first_name |
| LastName | last_name |
| Email | email |
| Phone | phone |
| Address | address |
| City | city |
| Province | province |
| PostalCode | postal_code |
| DateOfBirth | date_of_birth |
| LicenseNumber | license_number |

### Instructors
| DSS Field | ODSM Field |
|-----------|------------|
| FirstName | first_name |
| LastName | last_name |
| Email | email |
| Phone | phone |
| LicenseNumber | license_number |
| CertificationNumber | certification_number |

### Vehicles
| DSS Field | ODSM Field |
|-----------|------------|
| Make | make |
| Model | model |
| Year | year |
| LicensePlate | license_plate |
| VIN | vin |
| InspectionDate | inspection_date |

## Troubleshooting

### Common Issues

1. **Missing Required Fields**
   - Ensure all required fields are present in the export
   - Check field names match the mapping
   - Verify data format

2. **Data Format Issues**
   - Dates should be in YYYY-MM-DD format
   - Phone numbers should include area code
   - Email addresses should be valid

3. **Duplicate Records**
   - Check for duplicate email addresses
   - Verify unique identifiers
   - Review merge options

### Error Messages

- **"Required field missing"**: Export is missing a required field
- **"Invalid date format"**: Date field is not in correct format
- **"Duplicate record"**: Record with same unique identifier exists

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
4. Archive original export files 