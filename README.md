# Service Desk Plus CMDB CI Fields Update Script

This Python script provides functionality to update Configuration Item (CI) fields in Service Desk Plus On-Prem CMDB using the REST API.

## Features

- Update single or multiple CI fields in bulk
- Retrieve CI details before updating
- Search for CIs based on criteria
- Support for both Basic Authentication and Technician Key authentication
- Comprehensive logging and error handling
- Configurable via JSON files

## Requirements

- Python 3.6 or higher
- `requests` library (install via `pip install -r requirements.txt`)

## Installation

1. Clone or download the script files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Authentication Methods

Service Desk Plus supports two authentication methods:

1. **Basic Authentication**: Using username and password/API key
2. **Technician Key**: Using a technician key in headers

### Configuration File

Create a JSON configuration file (see `config_example.json`):

```json
{
  "base_url": "https://your-sdp-server.company.com",
  "username": "api_user",
  "password": "your_api_password_or_key",
  "technician_key": "your_technician_key_if_using_key_auth",
  "ci_updates": [
    {
      "ci_id": "CI001",
      "updates": {
        "name": "Updated Server Name",
        "description": "Updated description",
        "status": "Active",
        "location": "Data Center A"
      }
    }
  ]
}
```

## Usage

### Method 1: Using Configuration File

```bash
python update_ci_cmdb.py your_config.json
```

### Method 2: Direct Script Modification

Edit the `config` dictionary in the `main()` function and run:

```bash
python update_ci_cmdb.py
```

## API Endpoints Used

- `GET /api/v3/cmdb/ci/{ci_id}` - Retrieve CI details
- `PUT /api/v3/cmdb/ci/{ci_id}` - Update CI fields
- `GET /api/v3/cmdb/ci` - Search CIs

## Common CI Fields

The script can update any CI fields supported by your Service Desk Plus instance. Common fields include:

- `name` - CI name
- `description` - Description
- `status` - Status (Active, Inactive, etc.)
- `asset_tag` - Asset tag
- `serial_number` - Serial number
- `location` - Location
- `department` - Department
- `owner` - Owner
- `vendor` - Vendor
- `model` - Model
- `ip_address` - IP address
- `operating_system` - Operating system
- Custom fields as defined in your CMDB

## Examples

### Update Single CI

```python
from update_ci_cmdb import SDPCMDBUpdater

updater = SDPCMDBUpdater(
    base_url="https://sdp.company.com",
    username="api_user",
    password="api_password"
)

updater.update_ci_fields("CI001", {
    "status": "Inactive",
    "notes": "Decommissioned"
})
```

### Bulk Update from CSV/Excel

You can extend the script to read from CSV files:

```python
import csv

# Read from CSV
ci_updates = []
with open('ci_updates.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        ci_updates.append({
            'ci_id': row['CI_ID'],
            'updates': {k: v for k, v in row.items() if k != 'CI_ID' and v}
        })

results = updater.bulk_update_ci_fields(ci_updates)
```

### Search and Update

```python
# Search for servers
servers = updater.search_ci({"name": "Server*"})

# Update each server
for server in servers:
    updater.update_ci_fields(server['id'], {
        "status": "Active",
        "last_audit": "2024-01-08"
    })
```

## Logging

The script provides comprehensive logging:

- INFO: Successful operations
- WARNING: Non-critical issues
- ERROR: Failed operations

Logs are output to console with timestamps.

## Error Handling

- Network errors are caught and logged
- API errors return appropriate status codes
- Invalid configurations are reported
- Partial bulk update failures are tracked

## Security Notes

- Store API credentials securely (environment variables, secure config files)
- Use HTTPS for all API communications
- Consider IP restrictions in Service Desk Plus
- Rotate API keys regularly

## Troubleshooting

### Common Issues

1. **401 Unauthorized**: Check credentials and authentication method
2. **403 Forbidden**: Verify user permissions in Service Desk Plus
3. **404 Not Found**: Verify CI ID exists
4. **Connection errors**: Check network connectivity and SDP URL

### Debug Mode

Enable debug logging by modifying the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

## Extending the Script

The `SDPCMDBUpdater` class can be extended for additional functionality:

- Add new methods for CI creation/deletion
- Implement relationship management
- Add validation for specific field types
- Integrate with other ITSM tools

## Support

For Service Desk Plus API documentation, refer to:
- Service Desk Plus REST API documentation
- ManageEngine support portal

## License

This script is provided as-is for educational and operational use.