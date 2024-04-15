import csv
import subprocess

def execute_unique_start_process_commands(input_file="unique_activities.csv"):
    executed_processes = set()

    with open(input_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            process_name = row['Process']
            if process_name not in executed_processes:
                executed_processes.add(process_name)
                start_command = row['PowerShellCommand_Start']
                print(f"Executing: {start_command}")
                subprocess.run(["powershell", "-Command", start_command], shell=True)
def main():
    execute_unique_start_process_commands()

if __name__ == "__main__":
    main()
