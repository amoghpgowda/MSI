import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from database import DatabaseManager

class MailSender:
    def __init__(self) -> None:
        self.db = DatabaseManager('multi_system_installer.db')
        self.email_id, self.smtp_server, self.port, self.api_token = self.db.get_admin_email()

        self.server = smtplib.SMTP(self.smtp_server, self.port)
        self.user_name = self.email_id
        self.password = self.api_token
        self.server.starttls()
        self.server.login(self.user_name, self.password)
        
    def send_mail(self, start_time: datetime.datetime, end_time: datetime.datetime, machine_id: int, package_name: str, status_report: str, receiver_mail: str) -> None:
        msg = MIMEMultipart()
        msg['From'] = self.user_name
        msg['To'] = receiver_mail
        msg['Subject'] = 'Status report for ' + package_name
        
        start_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

        body = 'Machine ID: ' + str(machine_id) + '\nPackage name: ' + package_name + '\nStart time: ' + start_str + '\nEnd time: ' + end_str + '\nStatus report: ' + status_report
        msg.attach(MIMEText(body, 'plain'))

        self.server.sendmail(self.user_name, receiver_mail, msg.as_string())

    def close_connection(self) -> None:
        self.db.close_connection()
        self.server.quit()
