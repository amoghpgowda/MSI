import os
import time
import json
import sqlite3

class ConfigProcessor:
    def __init__(self, config_folder, done_folder, database_file, check_interval):
        self.config_folder = config_folder
        self.done_folder = done_folder
        self.database_file = database_file
        self.check_interval = check_interval

    def process_config_file(self, config_file):
        with open(config_file) as f:
            config_data = json.load(f)

        machine_id = config_data["machine-id"]
        scheduled_time = config_data["datetime"]

        software_list = config_data["software_list"]

        conn = sqlite3.connect(self.database_file)
        c = conn.cursor()

        for software in software_list:
            software_id = software.split()[0]
            c.execute("INSERT INTO scheduled_jobs (machine_id, software_id, scheduled_time) VALUES (?, ?, ?)",
                      (machine_id, software_id, scheduled_time))

        conn.commit()
        conn.close()
        
        os.rename(config_file, os.path.join(self.done_folder, os.path.basename(config_file)))

    def process_config_files(self):
        while True:
            config_files = os.listdir(self.config_folder)
            for config_file in config_files:
                if config_file.endswith('.json'):
                    config_file = os.path.join(self.config_folder, config_file)
                    self.process_config_file(config_file)
            time.sleep(self.check_interval)

if __name__ == "__main__":
    CONFIG_FOLDER = "config_files"
    DONE_FOLDER = "done_folder"
    DATABASE_FILE = "multi_system_installer.db"
    CHECK_INTERVAL = 30 * 60 

    os.makedirs(CONFIG_FOLDER, exist_ok=True)
    os.makedirs(DONE_FOLDER, exist_ok=True)

    config_processor = ConfigProcessor(CONFIG_FOLDER, DONE_FOLDER, DATABASE_FILE, CHECK_INTERVAL)

    config_processor.process_config_files()
