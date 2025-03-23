import os
import subprocess
from termcolor import colored
import time
from datetime import datetime

def print_banner():
    banner = """
    █████╗ ██╗     ██╗
    ██╔══██╗██║     ██║
    ███████║██║     ██║
    ██╔══██║██║     ██║
    ██║  ██║███████╗███████╗
    ╚═╝  ╚═╝╚══════╝╚══════╝
    """
    for line in banner.split('\n'):
        print(colored(line, 'cyan'))
        time.sleep(0.2)  # إضافة تأخير لإظهار البانر تدريجياً
    print(colored("\tLinux Admin Toolkit by Eng-> ALI MAHMOUD", 'yellow', attrs=['bold']))
    print(colored(f"\t{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 'green'))  # عرض التاريخ والوقت
    print("\n" + "="*50 + "\n")


# Function to execute shell commands and return output with improved readability
def execute_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
    return colored(output, 'green' if result.returncode == 0 else 'red')

# Function to list and manage system services
def manage_service():
    services = execute_command("systemctl list-units --type=service --no-pager --no-legend | awk '{print NR, $1}'")
    print(colored("Available Services:", 'cyan'))
    print(services)
    try:
        choice = int(input(colored("Enter the number of the service: ", 'blue')))
        selected_service = execute_command(f"systemctl list-units --type=service --no-pager --no-legend | awk 'NR=={choice}{{print $1}}'").strip()
        if selected_service:
            action = input(colored("Enter action (start/stop/restart/status): ", 'blue'))
            print(execute_command(f'sudo systemctl {action} {selected_service}'))
        else:
            print(colored("Invalid choice!", 'red'))
    except ValueError:
        print(colored("Invalid input! Please enter a number.", 'red'))

# Function to list and manage packages
def manage_packages():
    packages = execute_command("dpkg --list | awk 'NR>5 {print NR-5, $2}'")
    print(colored("Installed Packages:", 'cyan'))
    print(packages)
    try:
        choice = int(input(colored("Enter the number of the package: ", 'blue')))
        selected_package = execute_command(f"dpkg --list | awk 'NR-5=={choice}{{print $2}}'").strip()
        if selected_package:
            action = input(colored("Enter action (install/remove/update): ", 'blue'))
            print(execute_command(f'sudo apt {action} {selected_package} -y'))
        else:
            print(colored("Invalid choice!", 'red'))
    except ValueError:
        print(colored("Invalid input! Please enter a number.", 'red'))
'''
# Function to manage users
def manage_users():
    options = {"1": "Add User", "2": "Delete User", "3": "List Users", "4": "Change Password"}
    print(colored("User Management:", 'cyan'))
    for key, value in options.items():
        print(colored(f"{key}. {value}", 'yellow'))
    choice = input(colored("Enter your choice: ", 'blue'))
    
    if choice == "1":  # Add User
        username = input(colored("Enter the username to add: ", 'blue')).strip()
        if username:
            print(execute_command(f'sudo adduser {username}'))
        else:
            print(colored("Username cannot be empty!", 'red'))
    
    elif choice == "2":  # Delete User
        username = input(colored("Enter the username to delete: ", 'blue')).strip()
        if username:
            print(execute_command(f'sudo deluser {username}'))
        else:
            print(colored("Username cannot be empty!", 'red'))
    
    elif choice == "3":  # List Users
        print(colored("System Users:", 'cyan'))
        print(execute_command("cut -d: -f1 /etc/passwd"))
    
    elif choice == "4":  # Change Password
        username = input(colored("Enter the username to change password: ", 'blue')).strip()
        if username:
            print(execute_command(f'sudo passwd {username}'))
        else:
            print(colored("Username cannot be empty!", 'red'))
    
    else:
        print(colored("Invalid choice!", 'red'))
'''
# Function to monitor system resources
def monitor_system():
    resources = {"CPU Usage": "top -b -n1 | grep 'Cpu(s)'", "Memory Usage": "free -h", "Disk Usage": "df -h"}
    print(colored("System Resource Usage:", 'cyan'))
    for title, cmd in resources.items():
        print(colored(title, 'cyan'))
        print(execute_command(cmd))

# Function to check open ports
def check_open_ports():
    print(colored("Open Ports:", 'cyan'))
    print(execute_command("sudo netstat -tulnp | awk '{print $1, $4, $7}'"))

# Function to manage processes
def manage_processes():
    print(colored("Top 10 Memory-Consuming Processes:", 'cyan'))
    print(execute_command("ps aux --sort=-%mem | head -10 | awk '{printf \"%-10s %-10s %-10s %-50s\\n\", $2, $3, $4, $11}'"))
    try:
        pid = int(input(colored("Enter the PID to kill: ", 'blue')))
        print(execute_command(f"sudo kill -9 {pid}"))
    except ValueError:
        print(colored("Invalid input! Please enter a valid PID.", 'red'))

# Main function to provide menu options and execute user-selected actions
def main():
    print_banner()
    menu_options = {
        "1": ("Manage Services", manage_service),
        "2": ("Manage Packages", manage_packages),
        #"3": ("Manage Users", manage_users),
        "4": ("Monitor System", monitor_system),
        "5": ("Check Open Ports", check_open_ports),
        "6": ("Manage Processes", manage_processes)
    }
    
    while True:
        print(colored("\nLinux Administration Menu:", 'cyan'))
        for key, (desc, _) in menu_options.items():
            print(colored(f"{key}. {desc}", 'yellow'))
        print(colored("0. Exit", 'red'))
        
        choice = input(colored("Enter your choice: ", 'blue'))
        if choice == "0":
            print(colored("Exiting...", 'red'))
            break
        elif choice in menu_options:
            print(colored(f"Executing: {menu_options[choice][0]}", 'magenta'))
            menu_options[choice][1]()
        else:
            print(colored("Invalid choice! Please try again.", 'red'))

# Execute the script only if it is run directly
if __name__ == "__main__":
    main()
