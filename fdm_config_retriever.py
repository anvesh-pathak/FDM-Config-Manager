#!/usr/bin/env python3
import getpass
import sys
import time
from pathlib import Path
from fdm_base_client import FDMBaseClient


class FDMConfigRetriever(FDMBaseClient):
    """Handles FDM configuration export operations"""
    
    def export_configuration(self, disk_filename=None):
        """Export FDM full configuration"""
        payload = {
            "configExportType": "FULL_EXPORT",
            "type": "scheduleconfigexport",
            "doNotEncrypt": True,
            "deployedObjectsOnly": False
        }
        
        if disk_filename:
            payload["diskFileName"] = disk_filename
        
        try:
            print("📤 Starting full configuration export...")
            response = self._make_request('POST', 'action/configexport', json=payload)
            job_id = response.json().get('id')
            print(f"✓ Export job created: {job_id}")
            return job_id
        except Exception as e:
            print(f"✗ Export job creation failed: {e}")
            return None
    
    def check_export_status(self, job_id):
        """Check export job status"""
        try:
            response = self._make_request('GET', f'jobs/configexportstatus/{job_id}')
            return response.json()
        except Exception as e:
            # Job status endpoint may return 404 if job is complete or not found
            if hasattr(e, 'response') and hasattr(e.response, 'status_code') and e.response.status_code == 404:
                return None
            print(f"✗ Failed to check export status: {e}")
            return None
    
    def wait_for_export_completion(self, job_id, timeout=300):
        """Wait for export job to complete"""
        start_time = time.time()
        initial_files = [f['diskFileName'] for f in self.list_config_files()]
        
        while time.time() - start_time < timeout:
            status_data = self.check_export_status(job_id)
            
            if status_data:
                status = status_data.get('status', 'UNKNOWN')
                if status == 'SUCCESS':
                    print(f"✓ Export completed: {status_data.get('diskFileName')}")
                    return status_data
                elif status in ['FAILED', 'ERROR']:
                    print(f"✗ Export failed: {status_data.get('statusMessage')}")
                    return None
                elif status in ['RUNNING', 'QUEUED', 'PENDING']:
                    print(f"⏳ Export in progress... ({status})")
            else:
                # Check for new files if status unavailable
                current_files = [f['diskFileName'] for f in self.list_config_files()]
                new_files = [f for f in current_files if f not in initial_files]
                
                if new_files:
                    print(f"✓ Found new export file: {new_files[-1]}")
                    return {'status': 'SUCCESS', 'diskFileName': new_files[-1]}
            
            time.sleep(5)
        
        print(f"✗ Export timeout after {timeout} seconds")
        return None
    
    def download_config_file(self, filename, output_dir="."):
        """Download configuration file from FDM (keeps original .zip format)"""
        try:
            print(f"📥 Downloading {filename}...")
            response = self._make_request('GET', f'action/downloadconfigfile/{filename}', 
                                         stream=True, timeout=60)
            
            # Keep original filename (including .zip extension)
            output_path = Path(output_dir) / filename
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✓ Downloaded: {output_path}")
            print(f"📊 File size: {output_path.stat().st_size:,} bytes")
            return str(output_path)
        except Exception as e:
            print(f"✗ Download failed: {e}")
            return None



def get_user_inputs():
    """Get user inputs for FDM connection"""
    print("=" * 60)
    print("║" + " " * 18 + "FDM Configuration Exporter" + " " * 14 + "║")
    print("=" * 60)
    print()
    
    return (
        input("FDM IP address: ").strip(),
        input("Username: ").strip(),
        getpass.getpass("Password: "),
        input("\nDownload path [current directory]: ").strip() or ".",
        input("Custom filename (optional): ").strip()
    )


def main():
    try:
        host, username, password, download_path, filename = get_user_inputs()
        
        client = FDMConfigRetriever(host)
        if not client.authenticate(username, password):
            sys.exit(1)
        
        job_id = client.export_configuration(disk_filename=filename)
        if not job_id:
            sys.exit(1)
        
        result = client.wait_for_export_completion(job_id)
        if not result:
            sys.exit(1)
        
        exported_filename = result.get('diskFileName')
        if not exported_filename:
            print("✗ No filename returned from export job")
            sys.exit(1)
        
        downloaded_file = client.download_config_file(exported_filename, download_path)
        if not downloaded_file:
            sys.exit(1)
        
        print(f"✓ Configuration exported successfully to: {downloaded_file}")
        
        if input("Delete file from FDM? (y/N): ").strip().lower() == 'y':
            client.delete_config_file(exported_filename)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()