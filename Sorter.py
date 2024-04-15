import psutil
import csv
import datetime
import time

def log_daily_activities(interval=60, duration=86400, log_file="daily_activities.csv"):
    start_time = time.time()
    end_time = start_time + duration

    while time.time() < end_time:
        current_time = datetime.datetime.now()

        with open(f"temp_daily_activities_{current_time.date()}.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Time', 'TimeSpent', 'Process', 'PowerShellCommand_Start', 'PowerShellCommand_Kill'])

            for process in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    process_info = process.info
                    process_name = process_info['name']
                    process_pid = process_info['pid']
                    username = process_info['username']

                    writer.writerow([
                        current_time.date(),
                        current_time.time(),
                        '',
                        process_name,
                        f"Start-Process -FilePath '{process_name}' -NoNewWindow -PassThru",
                        f"Stop-Process -Id {process_pid} -Force"
                    ])

                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    pass

        time.sleep(interval)

def update_time_spent(log_file, temp_log_files):
    rows_to_update = []

    for temp_file in temp_log_files:
        with open(temp_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                rows_to_update.append(row)

    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Time', 'TimeSpent', 'Process', 'PowerShellCommand_Start', 'PowerShellCommand_Kill'])
        writer.writerows(rows_to_update)

def main(interval=86400, duration=604800, log_file="weekly_activities.csv"):
    start_time = time.time()
    end_time = start_time + duration
    temp_log_files = []

    while time.time() < end_time:
        log_daily_activities(interval=interval)

        current_time = datetime.datetime.now()
        temp_file = f"temp_daily_activities_{current_time.date()}.csv"
        temp_log_files.append(temp_file)

        time.sleep(interval)

    update_time_spent(log_file, temp_log_files)

if __name__ == "__main__":
    main()
