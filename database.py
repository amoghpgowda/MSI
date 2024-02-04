import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_machine(self, machine_id, ip_address, port_no, username, os_type, path, email, machine_type, private_key, password):
        query = "INSERT INTO machines (machine_id, ip_address, port_no, username, os_type, path, email, machine_type, private_key, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, (machine_id, ip_address, port_no, username, os_type, path, email, machine_type, private_key, password))
        self.conn.commit()

    def create_software(self, software_id, name, version, description, os_type, extension):
        query = "INSERT INTO software_repository (software_id, name, version, description, os_type, extension) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, (software_id, name, version, description, os_type, extension))
        self.conn.commit()

    def create_scheduled_job(self, machine_id, software_id, scheduled_time):
        query = "INSERT INTO scheduled_jobs (machine_id, software_id, scheduled_time) VALUES (?, ?, ?)"
        self.cursor.execute(query, (machine_id, software_id, scheduled_time))
        self.conn.commit()

    def create_completed_job(self, job_id, machine_id, software_id, status, completion_time, error_message):
        query = "INSERT INTO completed_jobs (job_id, machine_id, software_id, status, completion_time, error_message) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, (job_id, machine_id, software_id, status, completion_time, error_message))
        self.conn.commit()

    def get_machine(self, machine_id):
        query = "SELECT ip_address, username, port_no, private_key, path, os_type FROM machines WHERE machine_id = ?"
        self.cursor.execute(query, (machine_id,))
        return self.cursor.fetchone()
    
    def read_all_machines(self):
        query = "SELECT * FROM machines"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_all_user_machines(self):
        query = "SELECT * FROM machines WHERE machine_type = 'user'"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_software_repo_machine(self):
        query = "SELECT username, ip_address, path FROM machines WHERE machine_type = 'software_repo'"
        self.cursor.execute(query)
        return self.cursor.fetchone()
       
    def get_software(self, software_id):
        query = "SELECT name, extension FROM software_repository WHERE software_id = ?"
        self.cursor.execute(query, (software_id,))
        return self.cursor.fetchone()

    def read_all_softwares(self):
        query = "SELECT * FROM software_repository"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def read_scheduled_job(self, job_id):
        query = "SELECT * FROM scheduled_jobs WHERE job_id = ?"
        self.cursor.execute(query, (job_id,))
        return self.cursor.fetchone()

    def read_all_scheduled_jobs(self):
        query = "SELECT * FROM scheduled_jobs"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def read_completed_job(self, job_id):
        query = "SELECT * FROM completed_jobs WHERE job_id = ?"
        self.cursor.execute(query, (job_id,))
        return self.cursor.fetchone()

    def read_all_completed_jobs(self):
        query = "SELECT * FROM completed_jobs"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_admin_email(self):
        query = "SELECT email_id, smtp_server, port, api_token FROM admin_mail"
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    def delete_machine(self, machine_id):
        query = "DELETE FROM machines WHERE machine_id = ?"
        self.cursor.execute(query, (machine_id,))
        self.conn.commit()

    def delete_software(self, software_id):
        query = "DELETE FROM software_repository WHERE software_id = ?"
        self.cursor.execute(query, (software_id,))
        self.conn.commit()

    def delete_scheduled_job(self, job_id):
        query = "DELETE FROM scheduled_jobs WHERE job_id = ?"
        self.cursor.execute(query, (job_id,))
        self.conn.commit()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()