import os
import subprocess
import re
import logging
import sys

# Configure logging
LOG_FILE = '/home/sh/logs/security_hardening.log'
DRY_RUN = "--dry-run" in sys.argv  # Dry-run mode flag to simulate actions without applying changes

def ensure_log_directory(log_file):
    """Ensure the log directory exists before logging actions."""
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir, exist_ok=True)  # Create the directory if it doesn't exist
            print(f"Log directory created: {log_dir}")
        except Exception as e:
            print(f"Failed to create log directory: {e}")
            exit(1)  # Exit if the log directory cannot be created

ensure_log_directory(LOG_FILE)

# Set up logging to log messages into the specified log file
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_command(command):
    """Run a system command and log its output or errors."""
    try:
        if DRY_RUN:
            logging.info("Dry-run mode: Skipped running command: %s", command)
            return None  # Skip execution in dry-run mode
        result = subprocess.run(command, shell=True, capture_output=True, text=True)  # Execute the command
        if result.returncode == 0:  # Check if the command succeeded
            logging.info("Command succeeded: %s", command)
            return result.stdout  # Return the command's output
        else:
            logging.error("Command failed: %s\nError: %s", command, result.stderr)
            return None  # Log and return None if the command failed
    except Exception as e:
        logging.error("Error running command %s: %s", command, str(e))  # Handle unexpected errors
        return None

def backup_file(file_path):
    """Create a backup of a configuration file before modification."""
    try:
        if os.path.exists(file_path):
            backup_path = file_path + ".bak"
            if DRY_RUN:
                logging.info("Dry-run mode: Skipped creating backup for %s", file_path)
            else:
                run_command(f"cp {file_path} {backup_path}")  # Copy the file to create a backup
                logging.info("Backup of %s created at %s", file_path, backup_path)
        else:
            logging.warning("%s does not exist, skipping backup.", file_path)  # Warn if the file doesn't exist
    except Exception as e:
        logging.error("Error creating backup for %s: %s", file_path, str(e))  # Log errors during backup creation

def restore_backup(file_path):
    """Restore a backup file if it exists."""
    backup_path = file_path + ".bak"
    try:
        if os.path.exists(backup_path):  # Check if the backup file exists
            if DRY_RUN:
                logging.info("Dry-run mode: Skipped restoring backup for %s", file_path)
            else:
                run_command(f"mv {backup_path} {file_path}")  # Move backup file back to its original location
                logging.info("Restored backup for %s", file_path)
        else:
            logging.warning("No backup found for %s to restore.", file_path)  # Warn if no backup is found
    except Exception as e:
        logging.error("Error restoring backup for %s: %s", file_path, str(e))  # Log errors during restoration

def append_if_not_exists(file_path, search_text, new_line):
    """Append a line to a file if the line does not already exist."""
    try:
        with open(file_path, 'r') as f:
            if search_text in f.read():  # Check if the line already exists
                logging.info("%s already exists in %s", search_text.strip(), file_path)
                return
        if DRY_RUN:
            logging.info("Dry-run mode: Skipped appending to %s", file_path)
        else:
            with open(file_path, 'a') as f:
                f.write(new_line)  # Append the new line to the file
            logging.info("Added '%s' to %s", new_line.strip(), file_path)
    except Exception as e:
        logging.error("Error appending to %s: %s", file_path, str(e))  # Log errors during appending

def validate_change(file_path, search_text):
    """Validate that a specific change exists in the file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            if search_text in content:  # Check if the desired text is present
                logging.info("Validation passed: %s found in %s", search_text, file_path)
                return True
            else:
                logging.error("Validation failed: %s not found in %s", search_text, file_path)
                return False
    except Exception as e:
        logging.error("Error validating file %s: %s", file_path, str(e))  # Log errors during validation
        return False

def CID_5216():
    """CID 5216: Disable TCP forwarding in SSH."""
    sshd_config_path = '/etc/ssh/sshd_config'
    backup_file(sshd_config_path)  # Create a backup of the SSH config file
    updated = False
    try:
        with open(sshd_config_path, 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if re.match(r'^AllowTcpForwarding\s+no', line):  # Check if the setting is already enabled
                logging.info("AllowTcpForwarding is already set to 'no'. No changes needed.")
                return
            elif re.match(r'^#\s*AllowTcpForwarding\s+no', line):  # Uncomment the setting if it's commented out
                lines[i] = 'AllowTcpForwarding no\n'
                updated = True
                logging.info("Uncommented AllowTcpForwarding no in sshd_config.")
                break
        if not updated:
            lines.append('AllowTcpForwarding no\n')  # Add the setting if it's not found
            logging.info("Added AllowTcpForwarding no to sshd_config.")
        if DRY_RUN:
            logging.info("Dry-run mode: Skipped writing to %s", sshd_config_path)
        else:
            with open(sshd_config_path, 'w') as file:
                file.writelines(lines)  # Write the updated configuration back to the file
        validate_change(sshd_config_path, 'AllowTcpForwarding no')  # Confirm the change was applied
    except Exception as e:
        logging.error("Error applying CID_5216: %s", str(e))
        restore_backup(sshd_config_path)  # Restore the backup if an error occurs

def CID_5381():
    """CID 5381: Enable PAM in SSH."""
    sshd_config_path = '/etc/ssh/sshd_config'
    backup_file(sshd_config_path)  # Create a backup of the SSH config file
    append_if_not_exists(sshd_config_path, 'UsePAM yes', '\nUsePAM yes\n')  # Ensure PAM is enabled
    validate_change(sshd_config_path, 'UsePAM yes')  # Confirm the change was applied

def CID_1775():
    """CID 1775: Enable reverse path filtering."""
    sysctl_conf_path = '/etc/sysctl.conf'
    backup_file(sysctl_conf_path)  # Create a backup of the sysctl configuration file
    append_if_not_exists(sysctl_conf_path, 'net.ipv4.conf.default.rp_filter=1', '\nnet.ipv4.conf.default.rp_filter=1\n')
    append_if_not_exists(sysctl_conf_path, 'net.ipv4.conf.all.rp_filter=1', '\nnet.ipv4.conf.all.rp_filter=1\n')
    run_command("sysctl -p")  # Apply the changes immediately

def CID_1260():
    """CID 1260: Check the status of the CUPS service and disable it if necessary."""
    try:
        status_output = run_command('systemctl status cups')  # Check if the CUPS service is active
        if status_output and 'Active: active' in status_output:
            run_command('systemctl disable cups')  # Disable the service if it's active
            logging.info("CUPS service disabled.")
        else:
            logging.info("CUPS service is not active. No action taken.")
    except Exception as e:
        logging.error("Error applying CID_1260: %s", str(e))  # Log errors during the operation

def apply_security_hardening():
    # Ensure the script is run as root
    if os.geteuid() != 0:
        logging.error("This script must be run as root. Please use 'sudo'.")
        print("This script must be run as root. Please use 'sudo'.")
        exit(1)

    # Call each CID function to apply security hardening measures
    CID_5216()
    CID_5381()
    CID_1775()
    CID_1260()

    logging.info("Security hardening applied successfully.")
    print("Security hardening applied successfully.")

if __name__ == '__main__':
    apply_security_hardening()
