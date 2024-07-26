#!/usr/bin/env python3

import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define thresholds as variables
DISK_USAGE_THRESHOLD = 90
CPU_USAGE_THRESHOLD = 90

def get_disk_usage():
    logging.info("Starting disk usage check...")
    try:
        result = subprocess.run(['df', '-h'], stdout=subprocess.PIPE, text=True, check=True)
        lines = result.stdout.splitlines()
        for line in lines[1:]:
            usage = line.split()[4].rstrip('%')
            if int(usage) > DISK_USAGE_THRESHOLD:
                logging.warning(f"Disk Utilization > {DISK_USAGE_THRESHOLD}%: {line}")
            else:
                logging.info(f"Disk Utilization < {DISK_USAGE_THRESHOLD}%: {line}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to check disk usage: {e}")

def get_cpu_usage():
    logging.info("Starting CPU usage check...")
    try:
        result = subprocess.run(['top', '-b', '-n1'], stdout=subprocess.PIPE, text=True, check=True)
        lines = result.stdout.splitlines()
        for line in lines:
            if "Cpu(s)" in line:
                cpu_parts = line.split()
                user_usage = float(cpu_parts[1].strip('%'))
                system_usage = float(cpu_parts[3].strip('%'))
                cpu_usage = user_usage + system_usage
                if cpu_usage > CPU_USAGE_THRESHOLD:
                    logging.warning(f"CPU Utilization > {CPU_USAGE_THRESHOLD}%: {cpu_usage}%")
                else:
                    logging.info(f"CPU Utilization < {CPU_USAGE_THRESHOLD}%: {cpu_usage}%")
                break
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to check CPU usage: {e}")

if __name__ == "__main__":
    get_disk_usage()
    get_cpu_usage()
