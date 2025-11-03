#!/usr/bin/env python3
"""
FDM API Base Client
Provides common functionality for FDM REST API interactions
"""
import requests
import requests.exceptions
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class FDMBaseClient:
    """Base class for FDM API clients following Single Responsibility Principle"""
    
    def __init__(self, host):
        self.base_url = f"https://{host}"
        self.token = None
        self.session = requests.Session()
        self.session.verify = False
    
    def authenticate(self, username, password):
        """Authenticate with FDM and get access token"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/fdm/latest/fdm/token",
                json={"grant_type": "password", "username": username, "password": password},
                timeout=30
            )
            response.raise_for_status()
            self.token = response.json()['access_token']
            print("✓ Authentication successful")
            return True
        except Exception as e:
            print(f"✗ Authentication failed: {e}")
            return False
    
    def _get_headers(self):
        """Get authorization headers (DRY principle)"""
        return {"Authorization": f"Bearer {self.token}"}
    
    def _make_request(self, method, endpoint, **kwargs):
        """Generic request handler (DRY principle)"""
        kwargs.setdefault('headers', self._get_headers())
        kwargs.setdefault('timeout', 30)
        
        url = f"{self.base_url}/api/fdm/latest/{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response
    
    def list_config_files(self):
        """List available configuration files on FDM"""
        try:
            response = self._make_request('GET', 'action/configfiles')
            files = response.json().get('items', [])
            
            if files:
                print(f"\n📁 Available configuration files ({len(files)}):")
                print("-" * 80)
                for file_info in files:
                    print(f"  • {file_info['diskFileName']} "
                          f"({file_info.get('sizeBytes', 0):,} bytes) - "
                          f"Modified: {file_info.get('dateModified', 'unknown')}")
                print("-" * 80)
            else:
                print("📁 No configuration files found")
            
            return files
        except Exception as e:
            print(f"✗ Failed to list configuration files: {e}")
            return []
    
    def delete_config_file(self, filename):
        """Delete a configuration file from FDM"""
        try:
            self._make_request('DELETE', f'action/configfiles/{filename}')
            print(f"✓ Deleted file: {filename}")
            return True
        except Exception as e:
            print(f"✗ Failed to delete {filename}: {e}")
            return False
