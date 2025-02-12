#!/usr/bin/env python3
"""A simple FTP server script that supports anonymous or authenticated access with customizable port and directory."""

import argparse
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

def get_eth0_ip():
    try:
        import netifaces
        return netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
    except (ImportError, ValueError, KeyError):
        return "IP not found (eth0)"

def start_ftp_server(port=2121, username=None, password=None, directory=None):
    # Create authorizer
    authorizer = DummyAuthorizer()
    
    # Use current directory if none specified
    if directory is None:
        directory = os.getcwd()

    # Add user if credentials are provided, otherwise allow anonymous access
    if username and password:
        authorizer.add_user(username, password, directory, perm="elradfmw")
    else:
        authorizer.add_anonymous(directory, perm="elradfmw")

    # Create handler
    handler = FTPHandler
    handler.authorizer = authorizer
    
    # Set up server
    server = FTPServer(("0.0.0.0", port), handler)
    
    # Print server info
    ip_address = get_eth0_ip()
    print(f"\nFTP Server started on {ip_address}:{port}")
    print(f"Serving directory: {directory}")
    if username and password:
        print(f"Username: {username}")
        print(f"Password: {password}")
    else:
        print("Anonymous access enabled")
    print("\nPress Ctrl+C to stop the server")

    # Start server
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down FTP server")
        server.close_all()

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Start a simple FTP server with optional authentication",
        epilog="""
Examples:
  # Start anonymous FTP server on default port 21
  python3 local-ftp.py

  # Start server on custom port 2121
  python3 local-ftp.py -p 2121

  # Start server with authentication
  python3 local-ftp.py -u myuser -P mypassword

  # Serve specific directory
  python3 local-ftp.py -d /path/to/directory

  # Combine options
  python3 local-ftp.py -p 2121 -u myuser -P mypassword -d /path/to/share
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=21,
        help="Port number (default: 2121)"
    )
    
    parser.add_argument(
        "-u", "--username",
        help="FTP username (optional)"
    )
    
    parser.add_argument(
        "-P", "--password",
        help="FTP password (optional)"
    )
    
    parser.add_argument(
        "-d", "--directory",
        help="Directory to serve (default: current directory)"
    )

    args = parser.parse_args()

    # Validate that if username is provided, password is also provided and vice versa
    if bool(args.username) != bool(args.password):
        parser.error("Both username and password must be provided together")

    # Start the server
    start_ftp_server(
        port=args.port,
        username=args.username,
        password=args.password,
        directory=args.directory
    )

if __name__ == "__main__":
    main()