import psutil
import csv
import datetime
import time

# Function to log daily activities
def log_daily_activities(interval=60, duration=3600, log_file="daily_activities.csv"):
    start_time = time.time()
    end_time = start_time + duration

    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Time', 'TimeSpent', 'Process', 'PowerShellCommand_Start', 'PowerShellCommand_Kill'])

        while time.time() < end_time:
            current_time = datetime.datetime.now()
            start_time = time.time()

            # Retrieve active processes
            for process in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    process_info = process.info
                    process_name = process_info['name']
                    process_pid = process_info['pid']
                    username = process_info['username']
                    
                    # Log the process details
                    writer.writerow([
                        current_time.date(), 
                        current_time.time(), 
                        '',  # Placeholder for TimeSpent, will be updated later
                        process_name, 
                        f"Start-Process -FilePath '{process_name}' -NoNewWindow -PassThru", 
                        f"Stop-Process -Id {process_pid} -Force"
                    ])

                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    pass

            
            elapsed_time = time.time() - start_time
            update_time_spent(log_file, current_time, elapsed_time)

           
            time.sleep(interval)


def update_time_spent(log_file, current_time, elapsed_time):
    rows_to_update = []

    with open(log_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            date, time_stamp, _, _, _, _ = row
            row_time = datetime.datetime.strptime(f"{date} {time_stamp}", "%Y-%m-%d %H:%M:%S.%f")

            if current_time.date() == row_time.date():
                time_spent = datetime.timedelta(seconds=elapsed_time)
                rows_to_update.append([date, time_stamp, str(time_spent), *row[3:]])

    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Time', 'TimeSpent', 'Process', 'PowerShellCommand_Start', 'PowerShellCommand_Kill'])
        writer.writerows(rows_to_update)

# Main function
def main():
    log_daily_activities()

if __name__ == "__main__":
    main()
