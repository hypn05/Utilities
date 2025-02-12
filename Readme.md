
# Python Utility Scripts

A collection of useful Python utility scripts for various system administration, networking, and security tasks.

## Scripts

- **networkRequest.py**: Monitor network connections and requests for specific applications in real-time
- **networkConnect.py**: Monitor network connections for specific applications with a clean table display
- **base64d.py**: Decode base64 strings and JWT tokens with formatted output
- **quickMac.py**: Automated setup tool for development and security tools on macOS
- **local-ftp.py**: Simple FTP server supporting anonymous or authenticated access
- **utilities.py**: Display a list of utility scripts with their descriptions in a pretty table

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/python-utility-scripts.git
cd python-utility-scripts
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### networkRequest.py

```bash
python networkRequest.py
```

### networkConnect.py

```bash
python networkConnect.py
```

### base64d.py

```bash
python base64d.py
```

### quickMac.py

# Follow interactive prompts to select and install tools

```bash
python quickMac.py
```

### local-ftp.py

# Follow interactive prompts to select and install tools
```bash
// Start anonymous FTP server on default port 21
python local-ftp.py

// Start server on custom port
python local-ftp.py -p 2121

// Start server with username and password
python local-ftp.py -u username -p password

// Start server with username and password and custom port
python local-ftp.py -u username -p password -p 2121

```

### utilities.py
Displays all utility scripts with their descriptions

```bash
python utilities.py
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes and commit them
4. Push to your fork
5. Create a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
