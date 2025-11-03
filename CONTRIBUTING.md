# Contributing to FDM Configuration Import/Export Tool

First off, thank you for considering contributing to this project! It's people like you that make this tool better for everyone.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

**Bug Report Template:**
```
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. Enter credentials '...'
3. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment:**
 - OS: [e.g. macOS 13.1, Ubuntu 22.04]
 - Python Version: [e.g. 3.10.5]
 - FDM Version: [e.g. 7.4.2-172]
 - Script Version: [e.g. v1.0]

**Screenshots/Logs**
If applicable, add screenshots or error logs to help explain your problem.

**Additional context**
Add any other context about the problem here.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Create an issue and provide the following information:

**Enhancement Request Template:**
```
**Is your feature request related to a problem?**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear description of any alternative solutions or features you've considered.

**Use case**
Explain the use case and how this enhancement would benefit users.

**Additional context**
Add any other context or screenshots about the feature request here.
```

### Pull Requests

1. **Fork the Repository**
   ```bash
   git clone https://github.com/anvesh-pathak/FDM-Import-Export.git
   cd FDM-Import-Export
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. **Make Your Changes**
   - Follow the coding standards below
   - Add tests if applicable
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   # Test with multiple FDM versions if possible
   python3 fdm_config_retriever.py
   python3 fdm_config_importer.py
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m 'Add some AmazingFeature'
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/AmazingFeature
   ```

7. **Open a Pull Request**
   - Use a clear and descriptive title
   - Reference any related issues
   - Provide a comprehensive description of changes

## Development Guidelines

### Code Style

This project follows PEP 8 style guidelines for Python code:

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Use type hints where applicable

**Example:**
```python
def upload_config_file(self, file_path: str) -> Optional[str]:
    """
    Upload configuration file to FDM
    
    Args:
        file_path: Path to the configuration file
        
    Returns:
        Filename on FDM if successful, None otherwise
    """
    # Implementation
    pass
```

### Coding Principles

Follow these design principles:

- **KISS:** Keep it simple, stupid - avoid unnecessary complexity
- **YAGNI:** You aren't gonna need it - don't add speculative features
- **DRY:** Don't repeat yourself - reuse code where possible
- **SOLID:** Follow SOLID principles for object-oriented design

### Commit Message Guidelines

Use clear and meaningful commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

**Good commit messages:**
```
Add support for partial configuration import

- Implement object type filtering
- Add CLI arguments for selective import
- Update documentation with examples

Fixes #123
```

### Testing

Before submitting a pull request:

1. **Test with multiple FDM versions** (if possible)
2. **Test error scenarios** (authentication failures, network issues, etc.)
3. **Verify backward compatibility**
4. **Check for memory leaks** with large configuration files
5. **Validate input handling** (edge cases, invalid data)

### Documentation

Update documentation for any changes:

- Update README.md if adding features
- Add docstrings to new functions/classes
- Update API endpoint documentation if relevant
- Include usage examples for new features

## Project Structure

```
FDM-Import-Export/
├── fdm_base_client.py       # Shared base class
├── fdm_config_retriever.py  # Export functionality
├── fdm_config_importer.py   # Import functionality
├── requirements.txt         # Python dependencies
├── README.md               # Main documentation
├── LICENSE                 # MIT License
├── CONTRIBUTING.md         # This file
└── SECURITY.md            # Security policy
```

## Review Process

Pull requests are reviewed based on:

1. **Code Quality**
   - Follows coding standards
   - Well-documented and commented
   - Handles errors appropriately

2. **Functionality**
   - Works as intended
   - Doesn't break existing features
   - Tested in realistic scenarios

3. **Performance**
   - No unnecessary performance degradation
   - Efficient use of resources

4. **Security**
   - No security vulnerabilities
   - Follows security best practices

## Getting Help

If you need help:

- Check existing issues and pull requests
- Read the README.md documentation
- Review Cisco FDM API documentation
- Contact the maintainer: [anvpatha@cisco.com](mailto:anvpatha@cisco.com)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

**Unacceptable behavior includes:**
- Harassment or discriminatory language
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could be considered inappropriate

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes for significant contributions
- README.md acknowledgments section (optional)

Thank you for contributing to making FDM configuration management better for everyone! 🎉
