# Service Desk Plus Automation Scripts

This repository contains Python scripts for automating Service Desk Plus On-Prem operations using the REST API.

## Available Scripts

### 1. CMDB CI Fields Update Script (`update_ci_cmdb.py`)

Updates Configuration Item (CI) fields in Service Desk Plus CMDB.

**Features:**
- Update single or multiple CI fields in bulk
- Retrieve CI details before updating
- Search for CIs based on criteria
- Support for both Basic Authentication and Technician Key authentication
- Comprehensive logging and error handling
- Configurable via JSON files

### 2. User to Technician Conversion Script (`update_user_to_technician.py`)

Converts users to technicians and assigns sites, groups, and roles.

**Features:**
- Convert users to technicians with full profile setup
- Assign technicians to multiple sites
- Add technicians to support groups
- Assign roles and permissions
- Bulk processing capabilities
- Complete audit trail with logging

## Requirements

- Python 3.6 or higher
- `requests` library (install via `pip install -r requirements.txt`)

## Installation

1. Clone or download the script files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Authentication

Service Desk Plus supports two authentication methods:

1. **Basic Authentication**: Using username and password/API key
2. **Technician Key**: Using a technician key in headers

## Usage

### CMDB CI Updates

#### Using Configuration File

```bash
python update_ci_cmdb.py config_example.json
```

#### Direct Script Usage

```bash
python update_ci_cmdb.py
```

#### Configuration Example

```json
{
  "base_url": "https://your-sdp-server.company.com",
  "username": "api_user",
  "password": "your_api_password_or_key",
  "ci_updates": [
    {
      "ci_id": "CI001",
      "updates": {
        "name": "Updated Server Name",
        "status": "Active",
        "location": "Data Center A"
      }
    }
  ]
}
```

### User to Technician Conversion

#### Using Configuration File

```bash
python update_user_to_technician.py technician_config_example.json
```

#### Direct Script Usage

```bash
python update_user_to_technician.py
```

#### Configuration Example

```json
{
  "base_url": "https://your-sdp-server.company.com",
  "username": "api_user",
  "password": "your_api_password_or_key",
  "user_conversions": [
    {
      "user_id": "USER001",
      "technician_data": {
        "employee_id": "EMP001",
        "department": "IT Support",
        "job_title": "Senior IT Technician",
        "cost_per_hour": 75.00
      },
      "site_ids": ["SITE001", "SITE002"],
      "group_ids": ["GROUP001"],
      "role_ids": ["ROLE001", "ROLE002"]
    }
  ]
}
```

## API Endpoints Used

### CMDB CI Script
- `GET /api/v3/cmdb/ci/{ci_id}` - Retrieve CI details
- `PUT /api/v3/cmdb/ci/{ci_id}` - Update CI fields
- `GET /api/v3/cmdb/ci` - Search CIs

### Technician Script
- `GET /api/v3/users/{user_id}` - Get user details
- `POST /api/v3/users/{user_id}/convert_to_technician` - Convert user to technician
- `POST /api/v3/technicians/{technician_id}/sites` - Assign sites
- `POST /api/v3/technicians/{technician_id}/groups` - Assign groups
- `POST /api/v3/technicians/{technician_id}/roles` - Assign roles
- `GET /api/v3/sites`, `GET /api/v3/groups`, `GET /api/v3/roles` - Get reference data

## Common Fields

### CI Fields
- `name`, `description`, `status`, `asset_tag`, `serial_number`
- `location`, `department`, `owner`, `vendor`, `model`
- `ip_address`, `operating_system`, custom fields

### Technician Fields
- `employee_id`, `department`, `phone`, `mobile`, `job_title`
- `cost_per_hour`, `reporting_manager`, `hire_date`, `work_schedule`
- `skills`, `certifications`, `notes`

## Code Examples

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

### Convert User to Technician

```python
from update_user_to_technician import SDPTechnicianUpdater

updater = SDPTechnicianUpdater(
    base_url="https://sdp.company.com",
    username="api_user",
    password="api_password"
)

updater.process_user_to_technician({
    "user_id": "USER001",
    "technician_data": {
        "employee_id": "EMP001",
        "department": "IT Support",
        "job_title": "Technician"
    },
    "site_ids": ["SITE001"],
    "group_ids": ["GROUP001"],
    "role_ids": ["ROLE001"]
})
```

## Logging

Both scripts provide comprehensive logging:
- INFO: Successful operations
- WARNING: Non-critical issues
- ERROR: Failed operations

## Security Notes

- Store API credentials securely (environment variables, secure config files)
- Use HTTPS for all API communications
- Consider IP restrictions in Service Desk Plus
- Rotate API keys regularly

## Troubleshooting

### Common Issues

1. **401 Unauthorized**: Check credentials and authentication method
2. **403 Forbidden**: Verify user permissions in Service Desk Plus
3. **404 Not Found**: Verify IDs exist
4. **Connection errors**: Check network connectivity and SDP URL

### Debug Mode

Enable debug logging by modifying the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

## Files in Repository

- `update_ci_cmdb.py` - CMDB CI update script
- `update_user_to_technician.py` - User to technician conversion script
- `config_example.json` - CMDB configuration example
- `technician_config_example.json` - Technician configuration example
- `requirements.txt` - Python dependencies
- `README.md` - This documentation

## Support

For Service Desk Plus API documentation, refer to:
- Service Desk Plus REST API documentation
- ManageEngine support portal

## License

This script is provided as-is for educational and operational use.
