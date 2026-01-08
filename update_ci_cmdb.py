#!/usr/bin/env python3
"""
Service Desk Plus On-Prem CMDB CI Fields Update Script

This script updates Configuration Item (CI) fields in Service Desk Plus CMDB
using the REST API.

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


class SDPCMDBUpdater:
    """Service Desk Plus CMDB CI Updater class"""

    def __init__(self, base_url: str, username: str, password: str, technician_key: str = None):
        """
        Initialize the CMDB updater

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

    def get_ci_details(self, ci_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve CI details by ID

        Args:
            ci_id: Configuration Item ID

        Returns:
            CI details as dictionary or None if not found
        """
        try:
            url = f"{self.base_url}/api/v3/cmdb/ci/{ci_id}"
            response = self.session.get(url)

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully retrieved CI {ci_id}")
                return data.get('ci', data)
            elif response.status_code == 404:
                logger.warning(f"CI {ci_id} not found")
                return None
            else:
                logger.error(f"Failed to get CI {ci_id}: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error retrieving CI {ci_id}: {str(e)}")
            return None

    def update_ci_fields(self, ci_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update CI fields

        Args:
            ci_id: Configuration Item ID
            updates: Dictionary of fields to update

        Returns:
            True if update successful, False otherwise
        """
        try:
            url = f"{self.base_url}/api/v3/cmdb/ci/{ci_id}"

            # Prepare update payload
            payload = {"ci": updates}

            response = self.session.put(url, json=payload)

            if response.status_code in [200, 201]:
                logger.info(f"Successfully updated CI {ci_id}")
                return True
            else:
                logger.error(f"Failed to update CI {ci_id}: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error updating CI {ci_id}: {str(e)}")
            return False

    def search_ci(self, search_criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search for CIs based on criteria

        Args:
            search_criteria: Search parameters

        Returns:
            List of matching CIs
        """
        try:
            url = f"{self.base_url}/api/v3/cmdb/ci"
            response = self.session.get(url, params=search_criteria)

            if response.status_code == 200:
                data = response.json()
                cis = data.get('cis', [])
                logger.info(f"Found {len(cis)} CIs matching criteria")
                return cis
            else:
                logger.error(f"Failed to search CIs: {response.status_code} - {response.text}")
                return []

        except Exception as e:
            logger.error(f"Error searching CIs: {str(e)}")
            return []

    def bulk_update_ci_fields(self, ci_updates: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Bulk update multiple CIs

        Args:
            ci_updates: List of dictionaries with 'ci_id' and 'updates' keys

        Returns:
            Dictionary with success/failure counts
        """
        results = {'successful': 0, 'failed': 0}

        for ci_update in ci_updates:
            ci_id = ci_update.get('ci_id')
            updates = ci_update.get('updates')

            if not ci_id or not updates:
                logger.warning(f"Skipping invalid CI update: {ci_update}")
                results['failed'] += 1
                continue

            if self.update_ci_fields(ci_id, updates):
                results['successful'] += 1
            else:
                results['failed'] += 1

        logger.info(f"Bulk update completed: {results['successful']} successful, {results['failed']} failed")
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
    """Main function to run the CI update script"""

    # Default configuration - modify these or use config file
    config = {
        "base_url": "https://your-sdp-server.com",
        "username": "your-api-user",
        "password": "your-api-password",  # or API key
        "technician_key": None,  # Optional
        "ci_updates": [
            {
                "ci_id": "CI001",
                "updates": {
                    "name": "Updated Server Name",
                    "description": "Updated description",
                    "status": "Active",
                    "custom_field": "custom_value"
                }
            }
        ]
    }

    # Load config from file if provided
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        file_config = load_config_from_file(config_file)
        config.update(file_config)

    # Initialize updater
    updater = SDPCMDBUpdater(
        base_url=config['base_url'],
        username=config['username'],
        password=config['password'],
        technician_key=config.get('technician_key')
    )

    # Perform updates
    ci_updates = config.get('ci_updates', [])
    if ci_updates:
        results = updater.bulk_update_ci_fields(ci_updates)
        print(f"Update Results: {results['successful']} successful, {results['failed']} failed")
    else:
        print("No CI updates specified in configuration")

    # Example usage for single CI update
    # updater.update_ci_fields("CI001", {"status": "Inactive"})

    # Example usage for CI search
    # search_results = updater.search_ci({"name": "Server*"})
    # print(f"Found {len(search_results)} servers")


if __name__ == "__main__":
    main()