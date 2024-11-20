import os
import logging

# Configure logging
LOG_FILE = '/home/sh/logs/security_hardening_restore.log'

def ensure_log_directory(log_file):
    """Ensure the log directory exists."""
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir, exist_ok=True)
            print(f"Log directory created: {log_dir}")
        except Exception as e:
            print(f"Failed to create log directory: {e}")
            exit(1)

ensure_log_directory(LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def restore_backup(file_path):
    """Restore the backup file if it exists."""
    backup_path = file_path + ".bak"
    try:
        if os.path.exists(backup_path):
            os.rename(backup_path, file_path)  # Rename the backup to replace the original file
            logging.info("Restored %s from backup %s", file_path, backup_path)
            print(f"Restored {file_path} from backup.")
        else:
            logging.warning("No backup found for %s. Skipping.", file_path)
            print(f"No backup found for {file_path}. Skipping.")
    except Exception as e:
        logging.error("Error restoring backup for %s: %s", file_path, str(e))
        print(f"Error restoring backup for {file_path}: {e}")

def restore_files(file_paths):
    """Restore a list of files from their backups."""
    for file_path in file_paths:
        restore_backup(file_path)

if __name__ == "__main__":
    # List of files to restore
    files_to_restore = [
        '/etc/ssh/sshd_config',
        '/etc/sysctl.conf'
    ]

    # Ensure the script is run as root
    if os.geteuid() != 0:
        logging.error("This script must be run as root. Please use 'sudo'.")
        print("This script must be run as root. Please use 'sudo'.")
        exit(1)

    print("Starting restoration of original files...")
    logging.info("Starting restoration process.")
    
    restore_files(files_to_restore)
    
    logging.info("Restoration process completed.")
    print("Restoration process completed. Check the log for details.")
