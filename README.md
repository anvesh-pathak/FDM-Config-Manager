# FDM Configuration Import/Export Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Automate FDM configuration backups and restores via REST API. Export your entire FDM config to a zip file, and import it to another (or the same) FDM device.

**Stack:** Python 3.8+, Cisco FDM REST API v6+

## Why This Tool?

This is basically a disaster recovery tool. When FDM's built-in backup/restore isn't working or accessible, you can use this as an alternative method to export/import your configurations via the REST API.

## Quick Start

```bash
# Clone and setup
git clone https://github.com/anvesh-pathak/FDM-Import-Export.git
cd FDM-Import-Export
python3 -m venv myenv
source myenv/bin/activate  # or myenv\Scripts\activate on Windows
pip3 install -r requirements.txt

# Export config
python3 fdm_config_retriever.py

# Import config
python3 fdm_config_importer.py
```

## Requirements

- Python 3.8+
- FDM 7.2+ with API access
- Network access to FDM management interface

```bash
pip3 install requests urllib3
```

## Usage

### Export (Backup)

```bash
python3 fdm_config_retriever.py
```

You'll be prompted for:
- FDM IP/hostname
- Username/password
- Download path (default: current directory)
- Custom filename (optional)

Downloads a `.zip` file containing your full FDM configuration.

### Import (Restore)

```bash
python3 fdm_config_importer.py
```

Prompts for:
- Target FDM IP/hostname
- Username/password
- Full path to config `.zip` file

**Important:** Import doesn't auto-deploy. After import completes, log into FDM GUI and deploy the changes manually.

### Common Scenarios

**Daily backups:**
```bash
python3 fdm_config_retriever.py
# Save as: backup-$(date +%Y%m%d).zip
```

**Device migration:**
```bash
# Export from old FDM
python3 fdm_config_retriever.py  # IP: 10.1.1.10

# Import to new FDM
python3 fdm_config_importer.py   # IP: 10.1.1.20
```

**Disaster recovery:**
```bash
python3 fdm_config_importer.py
# Point to your latest backup zip
```

## How It Works

### Architecture

Three simple classes following SOLID principles:

```
FDMBaseClient - Shared auth and API calls
├── FDMConfigRetriever - Export functionality
└── FDMConfigImporter - Import functionality
```

### What Gets Exported?

Everything in your FDM config:
- Network/URL/Port objects
- Access control policies
- NAT policies
- Interfaces and zones
- Static routes
- All other configuration items

Exported as a JSON array in a zip file.

### API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `POST /fdm/token` | Authentication |
| `POST /action/configexport` | Start export job |
| `GET /jobs/configexportstatus/{id}` | Check export status |
| `GET /action/downloadconfigfile/{file}` | Download config |
| `POST /action/uploadconfigfile` | Upload config |
| `POST /action/configimport` | Start import job |
| `GET /jobs/configimportstatus/{id}` | Check import status |

## Troubleshooting

**`ModuleNotFoundError: No module named 'requests'`**
```bash
pip3 install -r requirements.txt
```

**`Connection refused`**
- Check FDM IP is correct
- Verify network connectivity
- Ensure FDM is running

**`Import failed: Cannot import configuration with X objects to be deployed`**
- You have pending changes on the target FDM
- Deploy or discard them first, then retry import

**`Authentication failed: 401`**
- Double-check username/password
- Verify account has admin privileges

## Known Limitations

- No auto-deployment (you must deploy manually via GUI)
- Import fails if target FDM has pending changes (deploy/discard first)
- SSL verification disabled (most FDMs use self-signed certs)
- May have issues importing across very different FDM versions

## Tested On

- **FDM:** 7.4.2, 7.6.2
- **Python:** 3.8, 3.9, 3.10, 3.11
- **OS:** macOS, Linux, Windows 10/11

## Security Notes

- Passwords entered via `getpass` (not echoed to terminal)
- No credentials stored anywhere
- All API communication over HTTPS
- Config files may contain sensitive data - encrypt your backups!

## Contributing

PRs welcome! This is a simple tool, so keep it simple:
- Follow PEP 8
- Add docstrings
- Test with real FDM before submitting
- Update README if adding features

## Author

Anvesh Pathak - [anvpatha@cisco.com](mailto:anvpatha@cisco.com)

## License

MIT - see LICENSE file

## Credits

- [Cisco FDM Import/Export API Guide](https://www.cisco.com/c/en/us/td/docs/security/firepower/ftd-api/guide/ftd-rest-api/ftd-api-import-export.html)
- [Python Requests](https://docs.python-requests.org/)

---

**Note:** Test in a lab before production use. Always validate backups work before you need them!
