#!/usr/bin/env python3
"""A tool for automating the setup of development and security tools on macOS"""

import os
import subprocess
import sys
import curses
import shutil

def run_command(command, sudo=False):
    try:
        if sudo and os.geteuid() != 0:
            command = f"sudo {command}"
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully ran: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {command}: {e}")
        sys.exit(1)

def is_tool_installed(tool_name):
    return shutil.which(tool_name) is not None

def install_homebrew():
    if is_tool_installed("brew"):
        print("Homebrew is already installed")
        return
    print("Installing Homebrew...")
    homebrew_install = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    run_command(homebrew_install)

def get_available_packages():
    return {
        "docker": "Docker container platform",
        "go": "Go programming language",
        "php": "PHP programming language", 
        "dotnet": ".NET development platform",
        "wireshark": "Network protocol analyzer",
        "burp-suite": "Web security testing tool",
        "nmap": "Network scanning tool",
        "metasploit": "Penetration testing framework",
        "git": "Version control system",
        "python3": "Python programming language",
        "node": "Node.js runtime",
        "visual-studio-code": "Code editor",
        "postman": "API testing tool",
        "iterm2": "Terminal emulator",
        "java": "Java development kit",
        "librewolf": "Privacy-focused Firefox fork",
        "brave-browser": "Privacy-focused web browser"
    }

def install_packages(selected_packages=None):
    print("Installing packages via Homebrew...")
    available_packages = get_available_packages()
    
    if selected_packages is None:
        packages_to_install = list(available_packages.keys())
    else:
        packages_to_install = selected_packages
    
    for package in packages_to_install:
        if is_tool_installed(package):
            print(f"{package} is already installed")
            continue
        print(f"Installing {package}...")
        run_command(f"brew install {package}", sudo=True)

def setup_docker():
    if not os.path.exists("/Applications/Docker.app"):
        print("Docker application not found")
        return
    print("Setting up Docker...")
    run_command("open /Applications/Docker.app")

def get_available_security_tools():
    return {
        "owasp-zap": "Web application security scanner",
        "sqlmap": "SQL injection testing tool",
        "nikto": "Web server scanner",
        "trivy": "Container vulnerability scanner"
    }

def install_security_tools(selected_tools=None):
    print("Installing additional security tools...")
    available_tools = get_available_security_tools()
    
    if selected_tools is None:
        if "owasp-zap" in (selected_tools or available_tools.keys()):
            if not os.path.exists("/Applications/OWASP ZAP.app"):
                run_command("brew install --cask owasp-zap", sudo=True)
            else:
                print("OWASP ZAP is already installed")
        if "sqlmap" in (selected_tools or available_tools.keys()):
            if not is_tool_installed("sqlmap"):
                run_command("pip3 install sqlmap", sudo=True)
            else:
                print("SQLMap is already installed")
        if "nikto" in (selected_tools or available_tools.keys()):
            if not is_tool_installed("nikto"):
                run_command("brew install nikto", sudo=True)
            else:
                print("Nikto is already installed")
        if "trivy" in (selected_tools or available_tools.keys()):
            if not is_tool_installed("trivy"):
                run_command("brew install aquasecurity/trivy/trivy", sudo=True)
            else:
                print("Trivy is already installed")

def draw_menu(stdscr, current_row, items):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    for idx, (item, desc) in enumerate(items):
        x = 2
        y = idx + 2
        
        if idx == current_row:
            stdscr.attron(curses.A_REVERSE)
        
        checkbox = "[x]" if item in selected_items else "[ ]"
        stdscr.addstr(y, x, f"{checkbox} {item}: {desc}")
        
        if idx == current_row:
            stdscr.attroff(curses.A_REVERSE)
    
    stdscr.refresh()

def select_tools():
    print("\nOptions:")
    print("1. Install all tools")
    print("2. Select specific tools")
    
    choice = input("\nEnter your choice (1 or 2): ")
    
    if choice == "1":
        return None, None
    elif choice == "2":
        def tool_selector(stdscr):
            global selected_items
            selected_items = set()
            
            # Set up colors
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
            
            # Get all tools
            available_packages = get_available_packages()
            available_security_tools = get_available_security_tools()
            
            all_tools = list(available_packages.items()) + list(available_security_tools.items())
            current_row = 0
            
            while True:
                draw_menu(stdscr, current_row, all_tools)
                
                key = stdscr.getch()
                
                if key == curses.KEY_UP and current_row > 0:
                    current_row -= 1
                elif key == curses.KEY_DOWN and current_row < len(all_tools) - 1:
                    current_row += 1
                elif key == ord(' '):  # Space to select/deselect
                    item = all_tools[current_row][0]
                    if item in selected_items:
                        selected_items.remove(item)
                    else:
                        selected_items.add(item)
                elif key == ord('\n'):  # Enter to finish selection
                    break
            
            return list(selected_items)
        
        selected_tools = curses.wrapper(tool_selector)
        
        dev_tools = [t for t in selected_tools if t in get_available_packages()]
        security_tools = [t for t in selected_tools if t in get_available_security_tools()]
        
        return dev_tools, security_tools
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

def main():
    print("Starting MacBook setup for Application Security Engineer...")
    
    # Check if running with sudo and warn if not
    if os.geteuid() != 0:
        print("Warning: Not running with sudo privileges. Will attempt to elevate privileges when needed.")
    
    # Install Homebrew first as it's required for other installations
    install_homebrew()
    
    # Let user select tools
    selected_dev_tools, selected_security_tools = select_tools()
    
    # Install and set up tools
    install_packages(selected_dev_tools)
    if "docker" in (selected_dev_tools or get_available_packages().keys()):
        setup_docker()
    install_security_tools(selected_security_tools)
    
    # Display installed tools
    if selected_dev_tools is None and selected_security_tools is None:
        print("""
    Setup complete! All tools have been installed:
    - Homebrew
    - Docker
    - Go
    - PHP
    - .NET
    - Wireshark
    - Burp Suite
    - Nmap
    - Metasploit
    - Git
    - Python3
    - Node.js
    - Visual Studio Code
    - Postman
    - iTerm2
    - Java
    - LibreWolf
    - Brave Browser
    - OWASP ZAP
    - SQLMap
    - Nikto
    - Trivy
    """)
    else:
        print("\nSetup complete! The following tools have been installed:")
        print("- Homebrew")
        if selected_dev_tools:
            for tool in selected_dev_tools:
                print(f"- {tool}")
        if selected_security_tools:
            for tool in selected_security_tools:
                print(f"- {tool}")
    
    print("\nPlease restart your computer to ensure all changes take effect.")

if __name__ == "__main__":
    main()
