#!/usr/bin/env python3
"""A utility script to monitor network connections for a specific application."""
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

def get_connections(process_name):
    """Get network connections for a specific process"""
    connections = []
    
    # Iterate through all processes
    for proc in psutil.process_iter(['pid', 'name']):  # Remove 'connections' from attrs
        try:
            # Check if process name matches
            if process_name.lower() in proc.info['name'].lower():
                # Get connections for this process using connections() method
                proc_connections = proc.connections()
                
                # Add connection details to list
                for conn in proc_connections:
                    connection_info = {
                        'pid': proc.info['pid'],
                        'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}",
                        'remote_addr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "None",
                        'status': conn.status
                    }
                    connections.append(connection_info)
                    
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

    print(f"\nMonitoring network connections for {process_name}...")
    print("Press Ctrl+C to stop monitoring")
    
    try:
        while True:
            connections = get_connections(process_name)
            
            # Clear screen
            print("\033[H\033[J")
            
            print(f"Network connections for {process_name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:")
            print("-" * 80)
            print(f"{'PID':<8} {'Local Address':<25} {'Remote Address':<25} {'Status':<12}")
            print("-" * 80)
            
            if not connections:
                print(f"No network connections found for process: {process_name}")
            else:
                for conn in connections:
                    print(f"{conn['pid']:<8} {conn['local_addr']:<25} {conn['remote_addr']:<25} {conn['status']:<12}")
            
            time.sleep(1)  # Update every second
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped")
        sys.exit(0)

if __name__ == "__main__":
    main()
