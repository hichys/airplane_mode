#!/usr/bin/env python3
import json
import argparse
import subprocess
import sys
import os

def main():
    # 1. Setup argument parser to accept anything
    parser = argparse.ArgumentParser(description="Universal bench wrapper for default site.")
    # REMAINDER captures all arguments passed after the script name
    parser.add_argument("bench_args", nargs=argparse.REMAINDER, 
                        help="Any bench command and its arguments")
    args = parser.parse_args()

    if not args.bench_args:
        print("Error: No bench command provided. Example: mybench console")
        sys.exit(1)

    # 2. Read the default_site from common_site_config.json
    # Note: Use absolute path if the script is run globally
    # Change '/home/user/frappe-bench/sites/...' to your actual bench path
    config_path = os.path.expanduser('~/frappe-15/sites/common_site_config.json')
    
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found. Please update the path in the script.")
        sys.exit(1)

    with open(config_path, 'r') as f:
        config = json.load(f)
        default_site = config.get("default_site")

    if not default_site:
        print("Error: 'default_site' not found in config.")
        sys.exit(1)

    # 3. Construct and run the command
    # This combines: bench + --site + [site] + [all your arguments]
    full_command = ["bench", "--site", default_site] + args.bench_args
    
    print(f"Running: {' '.join(full_command)}")
    
    try:
        subprocess.run(full_command, check=True)
    except subprocess.CalledProcessError:
        pass # Bench will handle its own error output
    except KeyboardInterrupt:
        print("\nCommand interrupted.")

if __name__ == "__main__":
    main()
