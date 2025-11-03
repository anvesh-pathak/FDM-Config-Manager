# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

The security of this project is taken seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do Not Disclose Publicly

Please do **NOT** create a public GitHub issue for security vulnerabilities. This could put all users at risk.

### 2. Contact Us Directly

Report security vulnerabilities via email to:

**Security Contact:** [anvpatha@cisco.com](mailto:anvpatha@cisco.com)

**Subject Line:** `[SECURITY] FDM Import/Export - <Brief Description>`

### 3. Provide Details

Include the following information in your report:

- **Type of vulnerability** (e.g., authentication bypass, injection, etc.)
- **Full paths of source file(s)** related to the vulnerability
- **Location of the affected source code** (tag/branch/commit or direct URL)
- **Step-by-step instructions** to reproduce the issue
- **Proof-of-concept or exploit code** (if possible)
- **Impact of the vulnerability** (what an attacker could achieve)
- **Suggested fix** (if you have one)

### 4. Response Timeline

You can expect:

- **Acknowledgment:** Within 48 hours
- **Initial Assessment:** Within 5 business days
- **Status Updates:** Every 7 days until resolved
- **Resolution:** Depending on severity (critical: 7 days, high: 14 days, medium: 30 days)

### 5. Coordinated Disclosure

We follow a coordinated disclosure process:

1. You report the vulnerability privately
2. We confirm the vulnerability and develop a fix
3. We release a security patch
4. Public disclosure occurs after patch release (typically 7-14 days)
5. Credit is given to the reporter (if desired)

## Security Best Practices

When using this tool, follow these security practices:

### Credential Management

- **Never hardcode credentials** in scripts or configuration files
- **Use environment variables** for automation (with proper access controls)
- **Create dedicated API users** with minimal required permissions
- **Rotate credentials regularly** (every 90 days recommended)
- **Use strong passwords** (12+ characters, mixed case, numbers, symbols)

### Network Security

- **Use VPN or private networks** when connecting to FDM
- **Avoid public networks** for configuration operations
- **Enable firewall rules** restricting FDM API access
- **Monitor API access logs** for suspicious activity

### File Security

- **Encrypt backup files** at rest (configuration contains sensitive data)
- **Secure backup storage** with appropriate access controls
- **Delete old backups** following retention policies
- **Validate file integrity** before importing configurations

### Operational Security

- **Test in lab environments** before production use
- **Review configurations** before importing to production
- **Maintain audit logs** of all import/export operations
- **Use version control** for configuration backups
- **Implement change management** processes

## Known Security Considerations

### SSL Certificate Validation

The tool disables SSL certificate verification for self-signed certificates:

```python
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session.verify = False
```

**Why:** Most FDM deployments use self-signed certificates.

**Risk:** Potential man-in-the-middle attacks.

**Mitigation:**
- Use trusted networks
- Verify FDM fingerprint manually
- Consider implementing certificate pinning for production

### Password Handling

Passwords are entered via `getpass` and not logged:

**Good:**
- Not displayed on screen
- Not written to logs
- Not stored in memory longer than necessary

**Additional Recommendations:**
- Clear terminal history after use
- Use dedicated API accounts
- Implement password managers

### API Token Management

Access tokens are session-based and expire:

**Security Features:**
- Tokens stored only in memory
- Expire after session timeout
- Not persisted to disk

**Best Practices:**
- Close sessions when done
- Don't share tokens
- Monitor token usage

## Vulnerability Disclosure Examples

### Example 1: Authentication Bypass

```
**Vulnerability:** Authentication Bypass via Token Reuse

**Description:** 
Access tokens can be reused across sessions allowing unauthorized access.

**Reproduction:**
1. Authenticate and capture token
2. Terminate session
3. Reuse token in new session
4. Access granted without re-authentication

**Impact:** 
High - Unauthorized access to FDM configuration operations

**Suggested Fix:**
Implement token validation and expiration checks.
```

### Example 2: Path Traversal

```
**Vulnerability:** Path Traversal in File Download

**Description:**
User-controlled file paths allow reading arbitrary files.

**Reproduction:**
1. Run fdm_config_retriever.py
2. Specify download path: ../../../../etc/passwd
3. File written outside intended directory

**Impact:**
Medium - Local file system access

**Suggested Fix:**
Validate and sanitize file paths, use Path.resolve()
```

## Security Updates

Subscribe to security updates:

- **GitHub Watch:** Enable notifications for this repository
- **Email Alerts:** Contact [anvpatha@cisco.com](mailto:anvpatha@cisco.com)
- **Release Notes:** Check releases for security patches

## Security Checklist

Before deploying to production:

- [ ] Changed default credentials
- [ ] Created dedicated API user
- [ ] Restricted network access to FDM
- [ ] Implemented backup encryption
- [ ] Configured audit logging
- [ ] Tested in isolated environment
- [ ] Reviewed all configuration files
- [ ] Documented security procedures
- [ ] Trained users on security practices
- [ ] Established incident response plan

## Compliance

This tool helps with compliance requirements:

- **Audit Trails:** Console logs provide operation records
- **Configuration Versioning:** Backup timestamps for change tracking
- **Access Controls:** Integrates with FDM user permissions
- **Data Protection:** Supports encrypted backups (external encryption recommended)

## Security Resources

- [Cisco FDM Security Best Practices](https://www.cisco.com/c/en/us/support/security/firepower-ngfw/products-installation-and-configuration-guides-list.html)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

## Hall of Fame

Security researchers who responsibly disclosed vulnerabilities:

*No vulnerabilities reported yet*

## Contact

For security concerns:
- **Email:** [anvpatha@cisco.com](mailto:anvpatha@cisco.com)
- **PGP Key:** Available upon request

For general issues:
- **GitHub Issues:** [Report non-security bugs](https://github.com/anvesh-pathak/FDM-Import-Export/issues)

---

**Last Updated:** November 2025  
**Version:** 1.0
