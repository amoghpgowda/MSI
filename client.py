import argparse
import json 
import paramiko
from scp import SCPClient
from datetime import datetime
import os

class clientSystemInstaller:
    def __init__(self):
        self.currentDirectory = os.getcwd()
        self.configFilePath = self.currentDirectory + "\configuration.json"

        with open(self.configFilePath, "r") as jfile:
            self.configurationFile = json.load(jfile)
        
        self.machineID = self.configurationFile["machine-id"]
        self.adminIP = self.configurationFile["admin-hostname"]
        self.adminUsername = self.configurationFile["admin-username"]
        self.privateKeyPath = self.configurationFile["private-key-path"]
        self.userConfigPath = self.configurationFile["config-file-path(local)"]
        self.adminConfigPath = self.configurationFile["config-file-path(admin)"]
        self.sotwareRequirementsPath = self.configurationFile["software-requirements-file-path"]

    def connection_builder(self) -> paramiko.SSHClient:
        private_key = paramiko.RSAKey(filename=self.privateKeyPath)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh_client.connect(hostname=self.adminIP, port=22, username=self.adminUsername, pkey=private_key)
        return ssh_client

    def send_config_file(self, filename : str):
        ssh_client = self.connection_builder()
        
        scp = SCPClient(ssh_client.get_transport())
        local_path = self.userConfigPath + filename
        remote_path = self.adminConfigPath
        scp.put(local_path, remote_path)
        ssh_client.close()

    def command_parser(self) -> argparse.ArgumentParser.parse_args:
        parser = argparse.ArgumentParser(description="Command Line Interface/Multi-System-Installer")
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-i', '--install', action='store_true', help='Install')
        group.add_argument('-u', '--update', action='store_true', help='Update')
        parser.add_argument('-f', '--filename', type=str, required=True, metavar=" ", help='Filename containing software list(.txt)')
        parser.add_argument('-t', '--datetime', type=str, required=True, metavar=" ", help='Schedule datetime in ISO format')
        
        args = parser.parse_args()

        return args 

    def configuration_file(self, args : argparse.ArgumentParser.parse_args) -> tuple:
        configuration = {}
        configuration["machine-id"] = self.machineID
        configuration["action"] = "install" if args.install else "update"
        configuration["datetime"] = args.datetime

        file_path = self.sotwareRequirementsPath + args.filename  
        with open(file_path, 'r') as file:
            packages = [f.strip() for f in file.readlines()]
            
        configuration["software_list"] = packages
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        extension = dt.replace(" ", ".").replace(":", "-")

        return configuration, extension

    def driver(self):           
        args = self.command_parser()
        config, extend = self.configuration_file(args)
        filename = "config_file" + extend + ".json"
        filepath = self.userConfigPath + filename
        with open(filepath, "w") as outfile:
            json.dump(config, outfile, indent=4)
        
        self.send_config_file(filename)

if __name__ == '__main__':
    clientSystemInstaller().driver()