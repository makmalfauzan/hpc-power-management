import json
from datetime import datetime
from collections import defaultdict

# ========== LOAD FILE ========== #
with open('nasa-train.json', 'r') as f:
    data = json.load(f)

# Cek dan perbaiki struktur jobs
jobs_raw = data['jobs']
jobs = jobs_raw[0] if isinstance(jobs_raw[0], list) else jobs_raw

# ========== HITUNG DAY AVERAGE ========== #
day_counter = defaultdict(int)
day_freq = defaultdict(set)

for job in jobs:
    dt = datetime.fromtimestamp(job['subtime'])
    day_name = dt.strftime('%A')  # e.g., 'Monday'
    date_str = dt.strftime('%Y-%m-%d')  # e.g., '2025-07-21'
    
    day_counter[day_name] += 1
    day_freq[day_name].add(date_str)

day_average = {}
for day in day_counter:
    total_days = len(day_freq[day])
    day_average[day] = round(day_counter[day] / total_days)

# ========== HITUNG JOB PERCENTAGE PER JAM ========== #
hour_counter = [0] * 24
total_jobs = len(jobs)

for job in jobs:
    hour = datetime.fromtimestamp(job['subtime']).hour
    hour_counter[hour] += 1

job_percentage = {
    str(hour): round(hour_counter[hour] / total_jobs, 4)
    for hour in range(24)
}

# ========== TAMPILKAN HASIL ========== #
print("\n Rata-rata job per hari (day_average):")
for day, count in day_average.items():
    print(f"{day}: {count}")

print("\n Persentase job per jam (job_percentage):")
for hour, pct in job_percentage.items():
    print(f"{hour}: {pct}")