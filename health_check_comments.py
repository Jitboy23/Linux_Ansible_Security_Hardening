#!/usr/bin/env python3

import subprocess  # Importing subprocess module to run shell commands from within Python

def get_disk_usage():
    print("Starting disk usage check...")  # Print a message indicating the start of the disk usage check
    result = subprocess.run(['df', '-h'], stdout=subprocess.PIPE, text=True)  # Run the 'df -h' command to check disk usage and capture the output
    lines = result.stdout.splitlines()  # Split the output into lines
    for line in lines[1:]:  # Iterate over each line, skipping the header
        usage = line.split()[4].rstrip('%')  # Extract the usage percentage from the line and remove the '%' character
        if int(usage) > 90:  # Check if the usage is greater than 90%
            print(f"Disk Utilization > 90%: {line}")  # Print a message if usage is greater than 90%
        else:
            print(f"Disk Utilization < 90%: {line}")  # Print a message if usage is less than 90%

def get_cpu_usage():
    print("Starting CPU usage check...")  # Print a message indicating the start of the CPU usage check
    result = subprocess.run(['top', '-b', '-n1'], stdout=subprocess.PIPE, text=True)  # Run the 'top' command in batch mode to get CPU usage and capture the output
    lines = result.stdout.splitlines()  # Split the output into lines
    for line in lines:  # Iterate over each line
        if "Cpu(s)" in line:  # Check if the line contains CPU usage information
            cpu_parts = line.split()  # Split the line into parts
            user_usage = float(cpu_parts[1].strip('%'))  # Extract the user CPU usage percentage and convert it to a float
            system_usage = float(cpu_parts[3].strip('%'))  # Extract the system CPU usage percentage and convert it to a float
            cpu_usage = user_usage + system_usage  # Calculate the total CPU usage
            if cpu_usage > 90:  # Check if the total CPU usage is greater than 90%
                print(f"CPU Utilization > 90%: {cpu_usage}%")  # Print a message if usage is greater than 90%
            else:
                print(f"CPU Utilization < 90%: {cpu_usage}%")  # Print a message if usage is less than 90%

def main():
    get_disk_usage()  # Call the function to check disk usage
    get_cpu_usage()  # Call the function to check CPU usage

if __name__ == "__main__":
    main()  # Run the main function if the script is executed directly
