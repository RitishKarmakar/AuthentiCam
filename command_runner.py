import csv
import subprocess
import os

# Function to execute daily activities
def execute_daily_activities(log_file="daily_activities.csv"):
    with open(log_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            process_name = row['Process']
            if os.path.isfile(process_name):
                start_command = row['PowerShellCommand_Start']
                print(f"Executing: {start_command}")
                subprocess.run(["powershell", "-Command", start_command], shell=True)

# Main function
def main():
    execute_daily_activities()

if __name__ == "__main__":
    main()
