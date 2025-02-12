#!/usr/bin/env python3
"""A utility to base64 decode space-separated arguments and JWT tokens"""

import base64
import sys
import json
import argparse
from colorama import init, Fore, Style

init()

def decode_base64(encoded_str):
    try:
        decoded = base64.b64decode(encoded_str).decode('utf-8')
        return decoded
    except Exception as e:
        return f"Error decoding {encoded_str}: {str(e)}"

def decode_jwt(token):
    try:
        # Split token into parts
        header, payload, signature = token.split('.')
        
        # Add padding if needed
        def add_padding(s):
            pad_length = len(s) % 4
            if pad_length:
                s += '=' * (4 - pad_length)
            return s

        # Decode header and payload
        header_json = json.loads(decode_base64(add_padding(header)))
        payload_json = json.loads(decode_base64(add_padding(payload)))
        
        # Format and color output
        print(f"\n{Fore.CYAN}=== JWT Token ==={Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}Header:{Style.RESET_ALL}")
        print(json.dumps(header_json, indent=2))
        print(f"\n{Fore.GREEN}Payload:{Style.RESET_ALL}")
        print(json.dumps(payload_json, indent=2))
        print(f"\n{Fore.YELLOW}Signature:{Style.RESET_ALL}")
        print(signature)
        
    except Exception as e:
        print(f"{Fore.RED}Error decoding JWT token: {str(e)}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(
        description='Base64 decode strings and JWT tokens',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  Decode base64 string:
    base64d.py SGVsbG8gV29ybGQ=
        
  Decode multiple base64 strings:
    base64d.py SGVsbG8= V29ybGQ=
        
  Decode JWT token:
    base64d.py eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U
        ''')
    parser.add_argument('strings', nargs='+', help='Base64 encoded string(s) or JWT token')
    args = parser.parse_args()
        
    for encoded in args.strings:
        # Check if input looks like a JWT token
        if encoded.count('.') == 2:
            decode_jwt(encoded)
        else:
            decoded = decode_base64(encoded)
            print(f"{encoded} -> {decoded}")

if __name__ == "__main__":
    main()
