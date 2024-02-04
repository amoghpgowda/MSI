from flask import Flask, jsonify, request
from database import DatabaseManager

app = Flask(__name__)

@app.route('/machines', methods=['GET'])
def get_machine_list():
    machines = DatabaseManager("multi_system_installer.db").read_all_machines()
    return jsonify(machines)

@app.route('/scheduled-jobs', methods=['GET'])
def get_scheduled_job_list():
    scheduled_jobs = DatabaseManager("multi_system_installer.db").read_all_scheduled_jobs()
    return jsonify(scheduled_jobs)

@app.route('/completed-jobs', methods=['GET'])
def get_completed_job_list():
    completed_jobs = DatabaseManager("multi_system_installer.db").read_all_completed_jobs()
    return jsonify(completed_jobs)

@app.route('/software', methods=['GET'])
def get_software_list():
    software = DatabaseManager("multi_system_installer.db").read_all_softwares()
    return jsonify(software)

@app.route('/machines', methods=['POST'])
def create_machine_entry():
    data = request.get_json()
    machine_id = data["machine_id"]
    ip_address = data["ip_address"]
    port_no = data["port_no"]
    username = data["username"]
    os_type = data["os_type"]
    path = data["path"]
    email = data["email"]
    machine_type = data["machine_type"]
    private_key = data["private_key"]
    password = data["password"]

    DatabaseManager("multi_system_installer.db").create_machine(machine_id, ip_address, port_no, username, os_type, path, email, machine_type, private_key, password)
    return jsonify({'message': 'Machine entry created successfully'})

@app.route('/scheduled-jobs', methods=['POST'])
def create_scheduled_job_entry():
    data = request.get_json()
    machine_id = data["machine_id"]
    software_id = data["software_id"]
    scheduled_time = data["scheduled_time"]

    DatabaseManager("multi_system_installer.db").create_scheduled_job(machine_id, software_id, scheduled_time)
    return jsonify({'message': 'Scheduled job entry created successfully'})

@app.route('/software', methods=['POST'])
def create_software_entry():
    data = request.get_json()
    software_id = data["software_id"]
    name = data["name"]
    version = data["version"]
    description = data["description"]
    os_type = data["os_type"]
    extension = data["extension"]

    DatabaseManager("multi_system_installer.db").create_software(software_id, name, version, description, os_type, extension)
    return jsonify({'message': 'Software entry created successfully'})

@app.route('/machines/<int:machine_id>', methods=['DELETE'])
def delete_machine_entry(machine_id):
    DatabaseManager("multi_system_installer.db").delete_machine(machine_id)
    return jsonify({'message': 'Machine entry deleted successfully'})

@app.route('/scheduled-jobs/<int:job_id>', methods=['DELETE'])
def delete_scheduled_job_entry(job_id):
    DatabaseManager("multi_system_installer.db").delete_scheduled_job(job_id)
    return jsonify({'message': 'Scheduled job entry deleted successfully'})

@app.route('/software/<int:software_id>', methods=['DELETE'])
def delete_software_entry(software_id):
    DatabaseManager("multi_system_installer.db").delete_software(software_id)
    return jsonify({'message': 'Software entry deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
