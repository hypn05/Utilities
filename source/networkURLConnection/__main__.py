#!/usr/bin/env python3
"""A utility script to monitor network connections and REST API calls for a specific application."""
import psutil
import sys
import readline
import time
import socket
from datetime import datetime
from urllib.parse import urlparse
import requests
from requests.exceptions import RequestException

def list_running_applications():
    """List all running applications"""
    running_apps = set()
    for proc in psutil.process_iter(['name']):
        try:
            running_apps.add(proc.info['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return sorted(list(running_apps))

def complete(text, state):
    """Tab completion function"""
    apps = list_running_applications()
    matches = [app for app in apps if app.lower().startswith(text.lower())]
    try:
        return matches[state]
    except IndexError:
        return None

def get_fqdn(ip):
    """Get FQDN from IP address"""
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        return ip

def get_connections(process_name):
    """Get network connections and API calls for a specific process"""
    connections = []
    seen_fqdns = set()
    
    # Iterate through all processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Check if process name matches
            if process_name.lower() in proc.info['name'].lower():
                # Get connections for this process using connections() method
                proc_connections = proc.connections()
                
                # Add connection details to list
                for conn in proc_connections:
                    if conn.raddr:  # Only process established connections
                        remote_ip = conn.raddr.ip
                        fqdn = get_fqdn(remote_ip)
                        seen_fqdns.add(fqdn)
                        
                        connection_info = {
                            'pid': proc.info['pid'],
                            'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}",
                            'remote_addr': f"{remote_ip}:{conn.raddr.port}",
                            'fqdn': fqdn,
                            'status': conn.status
                        }
                        
                        # Try to detect if this is an HTTP/HTTPS connection
                        if conn.raddr.port in (80, 443, 8080):
                            try:
                                protocol = 'https' if conn.raddr.port == 443 else 'http'
                                url = f"{protocol}://{fqdn}"
                                response = requests.head(url, timeout=1)
                                connection_info['api_info'] = {
                                    'url': url,
                                    'status_code': response.status_code,
                                    'headers': dict(response.headers)
                                }
                            except RequestException:
                                pass
                                
                        connections.append(connection_info)
                    
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    return connections, seen_fqdns

def main():
    if len(sys.argv) == 1:
        # Set up tab completion
        readline.set_completer(complete)
        readline.set_completer_delims(' \t\n')
        if sys.platform == 'darwin':  # macOS
            readline.parse_and_bind('bind ^I rl_complete')
        else:  # Linux and others
            readline.parse_and_bind('tab: complete')
        
        process_name = input("Enter application name (press Tab for suggestions): ")
        if not process_name:
            print("\nRunning applications:")
            for app in list_running_applications():
                print(app)
            process_name = input("\nEnter application name: ")
    else:
        process_name = sys.argv[1]

    print(f"\nMonitoring network connections and API calls for {process_name}...")
    print("Press Ctrl+C to stop monitoring")
    
    try:
        while True:
            connections, fqdns = get_connections(process_name)
            
            # Clear screen
            print("\033[H\033[J")
            
            print(f"Network activity for {process_name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:")
            print("\nConnected FQDNs:")
            print("-" * 80)
            for fqdn in sorted(fqdns):
                print(fqdn)
            
            print("\nDetailed Connections:")
            print("-" * 120)
            print(f"{'PID':<8} {'Local Address':<25} {'Remote Address':<25} {'FQDN':<35} {'Status':<12}")
            print("-" * 120)
            
            if not connections:
                print(f"No network connections found for process: {process_name}")
            else:
                for conn in connections:
                    print(f"{conn['pid']:<8} {conn['local_addr']:<25} {conn['remote_addr']:<25} {conn['fqdn']:<35} {conn['status']:<12}")
                    if 'api_info' in conn:
                        print(f"    API Call: {conn['api_info']['url']}")
                        print(f"    Status: {conn['api_info']['status_code']}")
                        print(f"    Headers: {conn['api_info']['headers']}\n")
            
            time.sleep(1)  # Update every second
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped")
        sys.exit(0)

if __name__ == "__main__":
    main()
