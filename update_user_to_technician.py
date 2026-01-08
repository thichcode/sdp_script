#!/usr/bin/env python3
"""
Service Desk Plus User to Technician Update Script

This script updates users to become technicians and assigns sites, groups, and roles
in Service Desk Plus On-Prem using the REST API.

Requirements:
- Python 3.6+
- requests library (pip install requests)
"""

import json
import logging
import sys
from typing import Dict, List, Optional, Any

import requests
from requests.auth import HTTPBasicAuth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SDPTechnicianUpdater:
    """Service Desk Plus Technician Updater class"""

    def __init__(self, base_url: str, username: str, password: str, technician_key: str = None):
        """
        Initialize the technician updater

        Args:
            base_url: Service Desk Plus base URL (e.g., https://sdp.company.com)
            username: API username
            password: API password or API key
            technician_key: Technician key for authentication (optional)
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.technician_key = technician_key
        self.session = requests.Session()

        # Set up authentication
        if technician_key:
            self.session.headers.update({
                'TECHNICIAN_KEY': technician_key,
                'Content-Type': 'application/json'
            })
        else:
            self.session.auth = HTTPBasicAuth(username, password)
            self.session.headers.update({'Content-Type': 'application/json'})

    def get_user_details(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user details by ID

        Args:
            user_id: User ID

        Returns:
            User details as dictionary or None if not found
        """
        try:
            url = f"{self.base_url}/api/v3/users/{user_id}"
            response = self.session.get(url)

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully retrieved user {user_id}")
                return data.get('user', data)
            elif response.status_code == 404:
                logger.warning(f"User {user_id} not found")
                return None
            else:
                logger.error(f"Failed to get user {user_id}: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error retrieving user {user_id}: {str(e)}")
            return None

    def get_technician_details(self, technician_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve technician details by ID

        Args:
            technician_id: Technician ID

        Returns:
            Technician details as dictionary or None if not found
        """
        try:
            url = f"{self.base_url}/api/v3/technicians/{technician_id}"
            response = self.session.get(url)

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully retrieved technician {technician_id}")
                return data.get('technician', data)
            elif response.status_code == 404:
                logger.warning(f"Technician {technician_id} not found")
                return None
            else:
                logger.error(f"Failed to get technician {technician_id}: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error retrieving technician {technician_id}: {str(e)}")
            return None

    def convert_user_to_technician(self, user_id: str, technician_data: Dict[str, Any]) -> Optional[str]:
        """
        Convert a user to technician

        Args:
            user_id: User ID to convert
            technician_data: Technician configuration data

        Returns:
            Technician ID if successful, None otherwise
        """
        try:
            url = f"{self.base_url}/api/v3/users/{user_id}/convert_to_technician"
            response = self.session.post(url, json=technician_data)

            if response.status_code in [200, 201]:
                data = response.json()
                technician_id = data.get('technician', {}).get('id')
                logger.info(f"Successfully converted user {user_id} to technician {technician_id}")
                return technician_id
            else:
                logger.error(f"Failed to convert user {user_id}: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error converting user {user_id} to technician: {str(e)}")
            return None

    def update_technician(self, technician_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update technician details

        Args:
            technician_id: Technician ID
            updates: Dictionary of fields to update

        Returns:
            True if update successful, False otherwise
        """
        try:
            url = f"{self.base_url}/api/v3/technicians/{technician_id}"
            response = self.session.put(url, json={"technician": updates})

            if response.status_code in [200, 201]:
                logger.info(f"Successfully updated technician {technician_id}")
                return True
            else:
                logger.error(f"Failed to update technician {technician_id}: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error updating technician {technician_id}: {str(e)}")
            return None

    def assign_technician_to_sites(self, technician_id: str, site_ids: List[str]) -> bool:
        """
        Assign technician to sites

        Args:
            technician_id: Technician ID
            site_ids: List of site IDs

        Returns:
            True if assignment successful, False otherwise
        """
        try:
            url = f"{self.base_url}/api/v3/technicians/{technician_id}/sites"
            payload = {"site_ids": site_ids}
            response = self.session.post(url, json=payload)

            if response.status_code in [200, 201]:
                logger.info(f"Successfully assigned technician {technician_id} to sites {site_ids}")
                return True
            else:
                logger.error(f"Failed to assign technician {technician_id} to sites: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error assigning technician {technician_id} to sites: {str(e)}")
            return False

    def assign_technician_to_groups(self, technician_id: str, group_ids: List[str]) -> bool:
        """
        Assign technician to groups

        Args:
            technician_id: Technician ID
            group_ids: List of group IDs

        Returns:
            True if assignment successful, False otherwise
        """
        try:
            url = f"{self.base_url}/api/v3/technicians/{technician_id}/groups"
            payload = {"group_ids": group_ids}
            response = self.session.post(url, json=payload)

            if response.status_code in [200, 201]:
                logger.info(f"Successfully assigned technician {technician_id} to groups {group_ids}")
                return True
            else:
                logger.error(f"Failed to assign technician {technician_id} to groups: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error assigning technician {technician_id} to groups: {str(e)}")
            return False

    def assign_technician_roles(self, technician_id: str, role_ids: List[str]) -> bool:
        """
        Assign roles to technician

        Args:
            technician_id: Technician ID
            role_ids: List of role IDs

        Returns:
            True if assignment successful, False otherwise
        """
        try:
            url = f"{self.base_url}/api/v3/technicians/{technician_id}/roles"
            payload = {"role_ids": role_ids}
            response = self.session.post(url, json=payload)

            if response.status_code in [200, 201]:
                logger.info(f"Successfully assigned roles {role_ids} to technician {technician_id}")
                return True
            else:
                logger.error(f"Failed to assign roles to technician {technician_id}: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error assigning roles to technician {technician_id}: {str(e)}")
            return False

    def get_sites(self) -> List[Dict[str, Any]]:
        """Get all available sites"""
        try:
            url = f"{self.base_url}/api/v3/sites"
            response = self.session.get(url)

            if response.status_code == 200:
                data = response.json()
                return data.get('sites', [])
            else:
                logger.error(f"Failed to get sites: {response.status_code} - {response.text}")
                return []

        except Exception as e:
            logger.error(f"Error getting sites: {str(e)}")
            return []

    def get_groups(self) -> List[Dict[str, Any]]:
        """Get all available groups"""
        try:
            url = f"{self.base_url}/api/v3/groups"
            response = self.session.get(url)

            if response.status_code == 200:
                data = response.json()
                return data.get('groups', [])
            else:
                logger.error(f"Failed to get groups: {response.status_code} - {response.text}")
                return []

        except Exception as e:
            logger.error(f"Error getting groups: {str(e)}")
            return []

    def get_roles(self) -> List[Dict[str, Any]]:
        """Get all available roles"""
        try:
            url = f"{self.base_url}/api/v3/roles"
            response = self.session.get(url)

            if response.status_code == 200:
                data = response.json()
                return data.get('roles', [])
            else:
                logger.error(f"Failed to get roles: {response.status_code} - {response.text}")
                return []

        except Exception as e:
            logger.error(f"Error getting roles: {str(e)}")
            return []

    def search_users(self, search_criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search for users based on criteria

        Args:
            search_criteria: Search parameters

        Returns:
            List of matching users
        """
        try:
            url = f"{self.base_url}/api/v3/users"
            response = self.session.get(url, params=search_criteria)

            if response.status_code == 200:
                data = response.json()
                users = data.get('users', [])
                logger.info(f"Found {len(users)} users matching criteria")
                return users
            else:
                logger.error(f"Failed to search users: {response.status_code} - {response.text}")
                return []

        except Exception as e:
            logger.error(f"Error searching users: {str(e)}")
            return []

    def process_user_to_technician(self, user_config: Dict[str, Any]) -> bool:
        """
        Process complete user to technician conversion with assignments

        Args:
            user_config: Configuration containing user_id and assignments

        Returns:
            True if successful, False otherwise
        """
        user_id = user_config.get('user_id')
        technician_data = user_config.get('technician_data', {})
        site_ids = user_config.get('site_ids', [])
        group_ids = user_config.get('group_ids', [])
        role_ids = user_config.get('role_ids', [])

        if not user_id:
            logger.error("User ID is required")
            return False

        try:
            # Step 1: Convert user to technician
            technician_id = self.convert_user_to_technician(user_id, technician_data)
            if not technician_id:
                return False

            success = True

            # Step 2: Assign to sites
            if site_ids and not self.assign_technician_to_sites(technician_id, site_ids):
                success = False

            # Step 3: Assign to groups
            if group_ids and not self.assign_technician_to_groups(technician_id, group_ids):
                success = False

            # Step 4: Assign roles
            if role_ids and not self.assign_technician_roles(technician_id, role_ids):
                success = False

            if success:
                logger.info(f"Successfully processed user {user_id} to technician {technician_id} with all assignments")
            else:
                logger.warning(f"User {user_id} converted to technician {technician_id} but some assignments failed")

            return success

        except Exception as e:
            logger.error(f"Error processing user {user_id} to technician: {str(e)}")
            return False

    def bulk_process_users_to_technicians(self, user_configs: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Bulk process multiple users to technicians

        Args:
            user_configs: List of user configurations

        Returns:
            Dictionary with success/failure counts
        """
        results = {'successful': 0, 'failed': 0}

        for user_config in user_configs:
            if self.process_user_to_technician(user_config):
                results['successful'] += 1
            else:
                results['failed'] += 1

        logger.info(f"Bulk processing completed: {results['successful']} successful, {results['failed']} failed")
        return results


def load_config_from_file(config_file: str) -> Dict[str, Any]:
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading config file {config_file}: {str(e)}")
        return {}


def main():
    """Main function to run the user to technician update script"""

    # Default configuration - modify these or use config file
    config = {
        "base_url": "https://your-sdp-server.com",
        "username": "your-api-user",
        "password": "your-api-password",
        "technician_key": None,
        "user_conversions": [
            {
                "user_id": "USER001",
                "technician_data": {
                    "employee_id": "EMP001",
                    "department": "IT Support",
                    "phone": "+1-234-567-8900",
                    "mobile": "+1-234-567-8901",
                    "job_title": "IT Technician",
                    "cost_per_hour": 50.00,
                    "reporting_manager": "MANAGER_ID"
                },
                "site_ids": ["SITE001", "SITE002"],
                "group_ids": ["GROUP001", "GROUP002"],
                "role_ids": ["ROLE001", "ROLE002"]
            }
        ]
    }

    # Load config from file if provided
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        file_config = load_config_from_file(config_file)
        config.update(file_config)

    # Initialize updater
    updater = SDPTechnicianUpdater(
        base_url=config['base_url'],
        username=config['username'],
        password=config['password'],
        technician_key=config.get('technician_key')
    )

    # Process conversions
    user_conversions = config.get('user_conversions', [])
    if user_conversions:
        results = updater.bulk_process_users_to_technicians(user_conversions)
        print(f"Conversion Results: {results['successful']} successful, {results['failed']} failed")
    else:
        print("No user conversions specified in configuration")


if __name__ == "__main__":
    main()