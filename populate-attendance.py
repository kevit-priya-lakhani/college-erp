import random
from datetime import datetime, timedelta
import json

# List of student IDs
student_ids = [
    "66c73cbdbf6a67c64ee5ac7e",
    "66d53e7d67fa64dbc47f20f2",
    "66d53ea067fa64dbc47f20f3",
    "66d53eb467fa64dbc47f20f4",
    "66d53ed167fa64dbc47f20f5",
    "66d53ee867fa64dbc47f20f6",
    "66d53f0267fa64dbc47f20f7",
    "66d53f1267fa64dbc47f20f8",
    "66d53f2967fa64dbc47f20f9",
    "66d53f4167fa64dbc47f20fa",
    "66d53f5667fa64dbc47f20fb",
    "66d53ff567fa64dbc47f20fe",
    "66d5400367fa64dbc47f20ff"
]

# Function to generate random dates between two dates
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Date range for years 2019-2021
start_date = datetime(2019, 1, 1)
end_date = datetime(2021, 12, 31)

# Generate attendance records
attendance_records = []

for _ in range(50):
    record = {
        "student_id": random.choice(student_ids),
        "date": random_date(start_date, end_date).strftime('%d-%m-%Y'),
        "present": random.choice([1, 1])
    }
    attendance_records.append(record)

# Store the records in a JSON file
with open('attendance_records.json', 'w') as json_file:
    json.dump(attendance_records, json_file, indent=4)

print("Attendance records have been saved to 'attendance_records.json'")
