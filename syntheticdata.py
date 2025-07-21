import random
import math
import json
from datetime import datetime, timedelta
import numpy as np

# ========== PARAMETER & VARIABEL DASAR ==========
year = 2025
month = 7
date = 1
days = 30  # total hari synthetic yang ingin dibuat

PROFILE = "100"
USER_ID = 0
job_subtime = []

# ========== DARI HASIL generate_day_job.py ==========

day_average = {
    'Thursday': 223,
    'Friday': 126,
    'Saturday': 60,
    'Sunday': 212,
    'Monday': 273,
    'Tuesday': 282,
    'Wednesday': 261
}

job_percentage = {
    "0": 0.0724, "1": 0.0546, "2": 0.0438, "3": 0.0341, "4": 0.0225, "5": 0.009,
    "6": 0.0073, "7": 0.004, "8": 0.0058, "9": 0.0051, "10": 0.0036, "11": 0.0031,
    "12": 0.0082, "13": 0.0134, "14": 0.0206, "15": 0.041, "16": 0.0602, "17": 0.0824,
    "18": 0.0962, "19": 0.0866, "20": 0.0845, "21": 0.0814, "22": 0.0835, "23": 0.0768
}

# ========== GENERATE SUBMISSION TIME ==========
for i in range(days):
    job_per_hour = {}
    start_time = datetime(year, month, date, 0, 0, 0)
    day_count = start_time.strftime("%A")
    job_count_day = day_average.get(day_count, 0)

    for hour, percentage in job_percentage.items():
        job_per_hour[hour] = job_count_day * percentage

    for hour, count in job_per_hour.items():
        random_num = random.random()
        if random_num > 0.5:
            rounded_value = math.ceil(count)
        else:
            rounded_value = math.floor(count)
        job_per_hour[hour] = int(rounded_value)

    job_hour = {}
    for hour in job_per_hour:
        job_hour[hour] = []

    for hour, count in job_per_hour.items():
        for i in range(count):
            random_minute = random.randint(0, 59)
            random_second = random.randint(0, 59)
            job_hour[hour].append(
                datetime(year, month, date, int(hour), random_minute, random_second)
            )

    job_hour = {int(k): v for k, v in sorted(job_hour.items())}
    for item in job_hour:
        job_hour[item] = sorted(job_hour[item])

    # masukin semua waktu ke job_subtime
    for hour in job_hour:
        for dt in job_hour[hour]:
            job_subtime.append(dt)

    # pindah ke hari berikutnya
    date += 1
    if month in (1, 3, 5, 7, 8, 10) and date > 31:
        date = 1
        month += 1
    elif month in (4, 6, 9, 11) and date > 30:
        date = 1
        month += 1
    elif month == 2 and date > 28:
        date = 1
        month += 1
    elif month == 12 and date > 31:
        date = 1
        month = 1
        year += 1

# ========== WALLTIME DAN REQUESTED NODE ==========
# Contoh distribusi dummy
walltime_distributions = {
    "100-500": 100,
    "501-2000": 250,
    "2001-6000": 120,
    "6001-12000": 80
}

res_distribution = {
    "2": 150,
    "4": 100,
    "8": 50,
    "16": 40,
    "32": 30,
    "64": 15,
    "128": 10
}

def calculate_probabilities(distribution):
    total = sum(distribution.values())
    return [count / total for count in distribution.values()]

walltime_probs = calculate_probabilities(walltime_distributions)
res_probs = calculate_probabilities(res_distribution)

def generate_job(jobId, walltime_probs, res_probs):
    walltime_group = np.random.choice(
        list(walltime_distributions.keys()), p=walltime_probs)
    walltime_range = walltime_group.split('-')
    walltime = random.randint(int(walltime_range[0]), int(walltime_range[1]))

    res = np.random.choice(list(res_distribution.keys()), p=res_probs)
    res = int(res)

    return {
        "id": jobId,
        "res": res,
        "subtime": 0,
        "walltime": walltime,
        "profile": PROFILE,
        "user_id": USER_ID,
    }

jobId = 1
synthetic_data = []
total_jobs = len(job_subtime)

for _ in range(total_jobs):
    job = generate_job(jobId, walltime_probs, res_probs)
    synthetic_data.append(job)
    jobId += 1

# ========== GABUNGKAN SUBTIME KE JOB ==========
for i in range(total_jobs):
    subtime = (job_subtime[i] - job_subtime[0]).total_seconds()
    synthetic_data[i]['subtime'] = int(subtime)

# ========== SIMPAN DATASET ==========
synthetic_dataset = {
    "nb_res": 128,
    "profiles": {
        "100": {
            "cpu": 100000000,
            "com": 0,
            "type": "parallel_homogeneous"
        }
    },
    "jobs": synthetic_data
}

with open("synthetic_dataset.json", "w") as f:
    json.dump(synthetic_dataset, f, indent=4)

print(f"Synthetic dataset berhasil disimpan. Jumlah job: {total_jobs}")