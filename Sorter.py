import csv

# Function to remove duplicates from daily activities
def remove_duplicates(input_file="daily_activities.csv", output_file="unique_activities.csv"):
    unique_activities = set()

    with open(input_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            unique_activities.add((row['Date'], row['Time'], row['Process'], row['PowerShellCommand_Start'], row['PowerShellCommand_Kill']))

    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Date', 'Time', 'Process', 'PowerShellCommand_Start', 'PowerShellCommand_Kill'])
        writer.writerows(unique_activities)

# Main function
def main():
    remove_duplicates()

if __name__ == "__main__":
    main()
