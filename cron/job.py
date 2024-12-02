import schedule
import time
import subprocess
import logging
import os

# Set up logging
logging.basicConfig(filename='./logfile.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

"""
This script is used to schedule a backup task every minute. It's used instead of cron jobs for cross-OS compatibility.
"""


def backup_task():
    try:
        # Determine the script to run based on the operating system
        if os.name == 'nt':  # Windows
            script = "backup_script.bat"
        else:  # Unix-like (Linux, macOS, etc.)
            script = "./backup_script.sh"

        # Run the appropriate script
        subprocess.run([script], shell=True, check=True)
        logging.info(f"Backup task completed successfully using {script}.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while running backup script: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


schedule.every(1).minute.do(backup_task)

while True:
    schedule.run_pending()
    time.sleep(1)
