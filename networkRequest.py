#!/usr/bin/env python3
"""A utility script to monitor network connections and requests for a specific application."""
import psutil
import sys
import readline
import time
from datetime import datetime

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

def get_connection_type(conn):
    """Determine if connection is inbound, outbound, or listening"""
    if conn.status == "LISTEN":
        return "LISTENING"
    elif not conn.raddr:
        return "PENDING"
    elif conn.laddr.port < conn.raddr.port:
        return "OUTBOUND"
    else:
        return "INBOUND"

def get_connections(process_name):
    """Get network connections for a specific process"""
    connections = []
    seen_connections = set()
    
    # Iterate through all processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Check if process name matches
            if process_name.lower() in proc.info['name'].lower():
                # Get connections for this process using connections() method
                proc_connections = proc.connections()
                
                # Add connection details to list
                for conn in proc_connections:
                    # Create unique connection identifier
                    conn_id = f"{conn.laddr.ip}:{conn.laddr.port}-{conn.raddr.ip if conn.raddr else 'None'}:{conn.raddr.port if conn.raddr else 'None'}"
                    
                    connection_type = get_connection_type(conn)
                    connection_info = {
                        'pid': proc.info['pid'],
                        'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}",
                        'remote_addr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "None",
                        'status': conn.status,
                        'type': connection_type,
                        'conn_id': conn_id
                    }
                    
                    # Only add if this is a new connection
                    if conn_id not in seen_connections:
                        connections.append(connection_info)
                        seen_connections.add(conn_id)
                        # Print new connection request
                        print(f"\nNew connection detected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:")
                        print(f"PID: {connection_info['pid']}")
                        print(f"Type: {connection_info['type']}")
                        print(f"Local Address: {connection_info['local_addr']}")
                        print(f"Remote Address: {connection_info['remote_addr']}")
                        print(f"Status: {connection_info['status']}")
                        print("-" * 80)
                    
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    return connections

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

    print(f"\nMonitoring network requests for {process_name}...")
    print("Press Ctrl+C to stop monitoring")
    
    try:
        previous_connections = set()
        while True:
            connections = get_connections(process_name)
            time.sleep(0.1)  # Check more frequently for new requests
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped")
        sys.exit(0)

if __name__ == "__main__":
    main()
