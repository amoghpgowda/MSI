from datetime import datetime
from remote_system import RemoteSystem
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from database import DatabaseManager
from mail_sender import MailSender
import logging

class JobScheduler:
    def __init__(self):
        self.db = DatabaseManager('multi_system_installer.db')
        self.software_repository = self.db.get_software_repo_machine()
        self.pool = ThreadPoolExecutor(10)
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(filename='job_scheduler.log', level=logging.INFO,
                            format='%(asctime)s %(levelname)s: %(message)s')

    def executor(self, job_id: int, machine_id: int, software_id: int):
        try:
            db = DatabaseManager('multi_system_installer.db')
            email = MailSender()
            host_name, user_name, port_number, private_key, path, os_type = db.get_machine(machine_id=machine_id)
            remote_system = RemoteSystem(self.software_repository, host_name, user_name, port_number, private_key, path)
            name, extension = db.get_software(software_id=software_id)
            filename = name + extension
            start_time = datetime.now()
            report = remote_system.install_software(file_name=filename, os_type=os_type)
            end_time = datetime.now()
            logging.info(f"Machine ID: {machine_id} Software ID: {software_id} Status: Completed")
            print(f"Machine ID: {machine_id}\nSoftware ID: {software_id}\nStatus: Completed")
            email.send_mail(start_time=start_time, end_time=end_time, machine_id=machine_id, package_name=filename, status_report="success", receiver_mail="amoghpgowda@gmail.com")
            db.create_completed_job(job_id=job_id, machine_id=machine_id, software_id=software_id, status="SUCCESS", completion_time=end_time, error_message="N/A")
            db.delete_scheduled_job(job_id=job_id)
            remote_system.close_connection()
        except Exception as e:
            logging.error(f"An error occurred during execution: {str(e)}")

    def run(self):
        terminate_flag = True
        while terminate_flag:
            scheduled_jobs = self.db.read_all_scheduled_jobs()
            futures = []
            for job in scheduled_jobs:
                job_id, machine_id, software_id, scheduled_time = job
                format_string = '%Y-%m-%d %H:%M:%S'
                datetime_object = datetime.strptime(scheduled_time, format_string)
                if datetime_object <= datetime.now():
                    future = self.pool.submit(self.executor, job_id, machine_id, software_id)
                    futures.append(future)
            for future in as_completed(futures):
                result = future.result()
            time.sleep(30 * 60)

JobScheduler().run()
