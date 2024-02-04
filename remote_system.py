import paramiko
import logging

class RemoteSystem:
    def __init__(self, software_repository: tuple, host_name: str, user_name: str, port_number: int, privatekey: str, path: str) -> None:
        self.host_name = host_name
        self.user_name = user_name
        self.port_number = port_number
        self.private_key = privatekey
        self.private_key_file = paramiko.RSAKey(filename="C:\\Users\\Dell\\OneDrive\\Desktop\\Hewlett-Packard-Enterprises\\Info\\privateKey.pem")
        self.remote_path = path
        self.software_repo = software_repository
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname=self.host_name, port=self.port_number, username=self.user_name, pkey=self.private_key_file)
        self.setup_logging()

    def setup_logging(self):
        self.logger = logging.getLogger('RemoteSystem')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('remote_system.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def file_transfer(self, file_name: str) -> None:
        username, host_name, host_path = self.software_repo
        cmd = f"scp -i {self.private_key} {username}@{host_name}:{host_path}{file_name} {self.remote_path}"
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
            wait = stdout.read().decode("utf-8")
            self.logger.info(f"File transfer successful: {file_name} @ Username: {self.user_name} IP: {self.host_name}")
        except Exception as e:
            self.logger.error(f"Exception occurred during file transfer: {str(e)} @ Username: {self.user_name} IP: {self.host_name}")

    def install_software(self, file_name: str, os_type: str) -> str:
        self.file_transfer(file_name)
        cmd = f'echo pass7602 | sudo -S apt install ./{file_name} -y'
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
            wait = stdout.read().decode("utf-8")
            self.logger.info(f"Software installation successful: {file_name} @ Username: {self.user_name} IP: {self.host_name}")
        except Exception as e:
            self.logger.error(f"Exception occurred during software installation: {str(e)} @ Username: {self.user_name} IP: {self.host_name}")
        return stdout.read().decode("utf-8")

    def close_connection(self) -> None:
        self.ssh_client.close()
        self.logger.info("SSH connection closed")
