import argparse
from tabulate import tabulate
from database import DatabaseManager


def main():
    parser = argparse.ArgumentParser()

    view_group = parser.add_mutually_exclusive_group()

    view_group.add_argument("-m", "--list-machines", action="store_true", help="list all machines")
    view_group.add_argument("-s", "--list-softwares", action="store_true", help="list all softwares")
    view_group.add_argument("-j", "--list-scheduled-jobs", action="store_true", help="list all scheduled jobs")
    view_group.add_argument("-c", "--list-completed-jobs", action="store_true", help="list all completed jobs")
    

    schedule_group = parser.add_argument_group("To schedule job")

    schedule_group.add_argument("-sj", "--schedule-a-job", action="store_true",
                                help = "shedule a job (include -mi MACHINE_ID -si SOFTWARE_ID -dt DATETIME)")

    schedule_group.add_argument("-am", "--shedule-all-mach", action="store_true",
                                help = "shedule a job for all machines (include -si SOFTWARE_ID -dt DATETIME)")


    input_group = parser.add_argument_group("Input options")

    input_group.add_argument("-mi", "--machine-id", nargs=1, metavar="MACHINE_ID", help="to pecify the machine ID")
    input_group.add_argument("-si", "--software-id", nargs=1, metavar="SOFTWARE_ID", help="to specify the software ID")
    input_group.add_argument("-dt", "--date-time", nargs=1, metavar="DATETIME", help="to specify the date and time")

    db_manager = DatabaseManager("multi_system_installer.db")

    args = parser.parse_args()

    message1 = "Invalid Option (-sj cannot be given with -m | -s | -j | -c)"

    message2 = "Invalid Option (-sj cannot be given with -am)"

    message3 = "Invalid Option (-sj requires -mi MACHINE_ID -si SOFTWARE_ID -dt DATETIME)"

    message4 = "Invalid Option (-am cannot have -mi MACHINE_ID only -si SOFTWARE_ID -dt DATETIME is required)"

    message5 = "Invalid Option (-am requires -si SOFTWARE_ID -dt DATETIME)"

    message6 = "Invalid Option (-am cannot be given with -m | -s | -j | -c)"


    if ((args.list_machines or args.list_softwares or args.list_scheduled_jobs or args.list_completed_jobs) and args.schedule_a_job):
         parser.error(message1) 

    if args.schedule_a_job and args.shedule_all_mach:
         parser.error(message2) 

    if args.schedule_a_job:
        if not (args.machine_id and args.software_id and args.date_time):
            parser.error(message3) 

    if (args.shedule_all_mach and args.machine_id):
         parser.error(message4)  

    if args.shedule_all_mach:
        if not (args.software_id and args.date_time):
            parser.error(message5) 

    if ((args.list_machines or args.list_softwares or args.list_scheduled_jobs or args.list_completed_jobs) and args.shedule_all_mach):
         parser.error(message6)

    if args.list_machines:
        user_machines = db_manager.get_all_user_machines()
        print(tabulate(user_machines, headers=["machine_id", "ip_address", "port_no", "username", "os_type", "path", "email", "machine_type", "private_key", "password"], tablefmt="pretty"))

    if args.list_softwares:
        all_softwares = db_manager.read_all_softwares()
        print(tabulate(all_softwares, headers=["software_id", "name", "version", "description", "os_type", "extension"], tablefmt="pretty"))

    if args.list_scheduled_jobs:
        all_scheduled_jobs = db_manager.read_all_scheduled_jobs()
        print(tabulate(all_scheduled_jobs, headers=["job_id", "machine_id", "software_id", "scheduled_time"], tablefmt="pretty"))

    if args.list_completed_jobs:
        all_completed_jobs = db_manager.read_all_completed_jobs()
        print(tabulate(all_completed_jobs, headers=["job_id", "machine_id", "software_id", "status", "completion_time", "error_message"], tablefmt="grid"))


    if args.schedule_a_job and args.machine_id and args.software_id and args.date_time:
        m_id = args.machine_id[0]
        s_id = args.software_id[0]
        dt = args.date_time[0]
        db_manager.create_scheduled_job(m_id, s_id, dt)        

    if args.shedule_all_mach and args.software_id and args.date_time:
        s_id = args.software_id[0]
        dt = args.date_time[0]
        all_machines = db_manager.get_all_user_machines()
        for item in all_machines:
            m_id = item[0]
            db_manager.create_scheduled_job(m_id, s_id, dt)      
    

if __name__ == "__main__":
    main()