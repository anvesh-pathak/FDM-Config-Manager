#!/usr/bin/env python3
import getpass
import sys
import time
import json
import zipfile
from pathlib import Path
from fdm_base_client import FDMBaseClient


class FDMConfigImporter(FDMBaseClient):
    """Handles FDM configuration import operations"""
    
    def extract_zip_config(self, zip_path):
        """Extract configuration from .zip file"""
        try:
            zip_path = Path(zip_path)
            if not zip_path.exists():
                print(f"✗ File not found: {zip_path}")
                return None
            
            print(f"📦 Extracting configuration from: {zip_path.name}")
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # List contents
                file_list = zip_ref.namelist()
                print(f"   Files in archive: {', '.join(file_list)}")
                
                # Find the JSON config file (usually the only file or named config.json)
                json_file = None
                for fname in file_list:
                    if fname.endswith('.json') or fname == 'config' or not '.' in fname:
                        json_file = fname
                        break
                
                if not json_file:
                    json_file = file_list[0]  # Use first file if no obvious config found
                
                # Extract to temporary file
                extracted_content = zip_ref.read(json_file)
                temp_path = zip_path.parent / f"{zip_path.stem}_extracted.json"
                
                with open(temp_path, 'wb') as f:
                    f.write(extracted_content)
                
                print(f"✓ Extracted to: {temp_path}")
                return str(temp_path)
                
        except zipfile.BadZipFile:
            print(f"✗ Invalid ZIP file: {zip_path}")
            return None
        except Exception as e:
            print(f"✗ Extraction failed: {e}")
            return None
    
    def upload_config_file(self, file_path):
        """Upload configuration file to FDM (uploads .zip directly, extracts .txt/.json to zip first)"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                print(f"✗ File not found: {file_path}")
                return None
            
            # Determine upload path and MIME type
            if file_path.suffix.lower() == '.zip':
                # Upload .zip files directly
                upload_path = file_path
                mime_type = 'application/zip'
            else:
                # For .txt or .json files, we need to create a temporary .zip
                print(f"📦 Creating ZIP archive from: {file_path.name}")
                upload_path = file_path.parent / f"{file_path.stem}.zip"
                
                with zipfile.ZipFile(upload_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                    # Add the config file to zip with a standard name
                    zip_ref.write(file_path, 'full_config.txt')
                
                mime_type = 'application/zip'
                print(f"✓ Created: {upload_path.name}")
            
            print(f"📤 Uploading configuration file: {upload_path.name}")
            
            with open(upload_path, 'rb') as f:
                files = {'fileToUpload': (upload_path.name, f, mime_type)}
                response = self._make_request('POST', 'action/uploadconfigfile', 
                                             files=files, timeout=60)
            
            result = response.json()
            print(f"✓ Upload successful: {result['diskFileName']} ({result.get('sizeBytes', 0):,} bytes)")
            
            # Clean up temporary zip file if we created one
            if file_path.suffix.lower() != '.zip' and upload_path.exists():
                upload_path.unlink()
                print(f"🗑️  Cleaned up temporary file: {upload_path.name}")
            
            return result['diskFileName']
        except Exception as e:
            print(f"✗ Upload failed: {e}")
            return None
            return None
    
    def import_configuration(self, disk_filename, auto_deploy=False, 
                           allow_pending_changes=False, preserve_file=True):
        """Import configuration from uploaded file"""
        payload = {
            "diskFileName": disk_filename,
            "preserveConfigFile": preserve_file,
            "autoDeploy": auto_deploy,
            "allowPendingChange": allow_pending_changes,
            "type": "scheduleconfigimport"
        }
        
        try:
            print(f"📥 Starting configuration import...")
            print(f"   • Auto-deploy: {auto_deploy}")
            print(f"   • Allow pending changes: {allow_pending_changes}")
            
            response = self._make_request('POST', 'action/configimport', json=payload)
            job_id = response.json().get('jobHistoryUuid')
            print(f"✓ Import job created: {job_id}")
            return job_id
        except Exception as e:
            print(f"✗ Import job creation failed: {e}")
            return None
    
    def check_import_status(self, job_id):
        """Check import job status"""
        try:
            response = self._make_request('GET', f'jobs/configimportstatus/{job_id}')
            return response.json()
        except Exception as e:
            # Job status endpoint may return 404 if job is complete or not found
            if hasattr(e, 'response') and hasattr(e.response, 'status_code') and e.response.status_code == 404:
                return None
            print(f"✗ Failed to check import status: {e}")
            return None
    
    def wait_for_import_completion(self, job_id, timeout=600):
        """Wait for import job to complete"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status_data = self.check_import_status(job_id)
            
            if not status_data:
                print(f"⚠ Job status not available")
                time.sleep(10)
                continue
            
            status = status_data.get('status', 'UNKNOWN')
            message = status_data.get('statusMessage', '')
            
            if status == 'SUCCESS':
                print(f"✓ Import completed successfully!")
                if status_data.get('autoDeploy'):
                    print("✓ Configuration deployed automatically")
                return status_data
            elif status in ['FAILED', 'ERROR']:
                # Check for pending deployment error
                if 'objects to be deployed' in message or 'pending' in message.lower():
                    print(f"✗ Import failed: {message}")
                    print("\n⚠️  RESOLUTION: There are pending deployments on the FDM device.")
                    print("   Please deploy or discard pending changes before importing:")
                    print("   1. Log into FDM web interface")
                    print("   2. Go to Deploy > Deployment")
                    print("   3. Either 'Deploy' or 'Discard' pending changes")
                    print("   4. Try running the import again")
                else:
                    print(f"✗ Import failed: {message}")
                
                messages = status_data.get('messages', [])
                if messages:
                    print("\nError details:")
                    for msg in messages:
                        print(f"  • {msg}")
                return None
            elif status in ['RUNNING', 'QUEUED', 'PENDING']:
                print(f"⏳ Import in progress... ({status})")
            else:
                print(f"ℹ Import status: {status} - {message}")
            
            time.sleep(10)
        
        print(f"✗ Import timeout after {timeout} seconds")
        return None
    
    def validate_config_file(self, file_path):
        """Validate configuration file format (handles both .zip and JSON files)"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                print(f"✗ File not found: {file_path}")
                return False
            
            print(f"🔍 Validating configuration file: {file_path.name}")
            
            # If it's a .zip file, extract and validate the contents
            if file_path.suffix.lower() == '.zip':
                extracted_path = self.extract_zip_config(file_path)
                if not extracted_path:
                    return False
                validate_path = Path(extracted_path)
            else:
                validate_path = file_path
            
            with open(validate_path, 'r') as f:
                config_data = json.load(f)
            
            if not isinstance(config_data, list) or not config_data:
                print("✗ Configuration must be a non-empty JSON array")
                # Clean up if we extracted
                if file_path.suffix.lower() == '.zip' and validate_path.exists():
                    validate_path.unlink()
                return False
            
            if config_data[0].get('type') != 'metadata':
                print("✗ First object must be metadata")
                # Clean up if we extracted
                if file_path.suffix.lower() == '.zip' and validate_path.exists():
                    validate_path.unlink()
                return False
            
            metadata = config_data[0]
            print(f"✓ Valid configuration file:")
            print(f"   • Hardware Model: {metadata.get('hardwareModel', 'Unknown')}")
            print(f"   • Software Version: {metadata.get('softwareVersion', 'Unknown')}")
            print(f"   • Objects: {len(config_data)} total")
            
            # Clean up temporary extracted file if we created one
            if file_path.suffix.lower() == '.zip' and validate_path.exists():
                validate_path.unlink()
            
            return True
        except json.JSONDecodeError as e:
            print(f"✗ Invalid JSON format: {e}")
            return False
        except Exception as e:
            print(f"✗ Validation failed: {e}")
            return False



def find_config_file(file_input):
    """Find configuration file from user input or directory listing"""
    config_path = Path(file_input)
    
    if config_path.exists():
        return str(config_path)
    
    print(f"✗ File not found: {file_input}")
    config_files = list(Path('.').glob('*.txt')) + list(Path('.').glob('*.json')) + list(Path('.').glob('*.zip'))
    
    if not config_files:
        print("No configuration files found")
        return None
    
    print("\n📁 Configuration files found in current directory:")
    for i, file in enumerate(config_files, 1):
        print(f"  {i}. {file.name}")
    
    choice = input(f"\nSelect file (1-{len(config_files)}) or press Enter to exit: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(config_files):
        return str(config_files[int(choice) - 1])
    
    return None


def get_user_inputs():
    """Get user inputs for FDM connection"""
    print("=" * 60)
    print("║" + " " * 18 + "FDM Configuration Importer" + " " * 14 + "║")
    print("=" * 60)
    print()
    
    host = input("Target FDM IP address: ").strip()
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    config_file = find_config_file(input("\nConfiguration file path: ").strip())
    
    if not config_file:
        sys.exit(1)
    
    # Default settings
    print(f"\nUsing default import settings:")
    print(f"  • Auto-deploy: False")
    print(f"  • Allow pending changes: False")
    print(f"  • Keep uploaded file: True")
    
    return host, username, password, config_file


def main():
    try:
        host, username, password, config_file = get_user_inputs()
        
        client = FDMConfigImporter(host)
        if not client.authenticate(username, password):
            sys.exit(1)
        
        if not client.validate_config_file(config_file):
            sys.exit(1)
        
        disk_filename = client.upload_config_file(config_file)
        if not disk_filename:
            sys.exit(1)
        
        job_id = client.import_configuration(disk_filename, auto_deploy=False, 
                                            allow_pending_changes=False, preserve_file=True)
        if not job_id:
            sys.exit(1)
        
        result = client.wait_for_import_completion(job_id)
        
        if result:
            print("\n" + "=" * 70)
            print("║" + " " * 68 + "║")
            print("║" + " " * 10 + "🎉 CONFIGURATION IMPORT COMPLETED SUCCESSFULLY! 🎉" + " " * 7 + "║")
            print("║" + " " * 68 + "║")
            print("=" * 70)
            print("\n⚠️  IMPORTANT: Configuration imported but NOT deployed yet")
            print("   Manual deployment required to activate changes:")
            print("   1. Log into FDM web interface")
            print("   2. Navigate to Deploy > Deployment")
            print("   3. Review pending changes")
            print("   4. Click 'Deploy' to apply configuration\n")
        else:
            print("\n✗ Configuration import failed")
            client.delete_config_file(disk_filename)
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()