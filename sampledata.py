import json
import numpy as np
import random

# Load training data
with open('nasa-train.json', 'r') as file:
    original_data = json.load(file)

# Ambil semua job
original_jobs = original_data['jobs'][0]  # karena jobs disimpan dalam list
original_subtimes = [job['subtime'] for job in original_jobs]

# Hitung inter-arrival time & rata-ratanya
inter_arrival_times = [
    original_subtimes[i] - original_subtimes[i - 1]
    for i in range(1, len(original_subtimes))
]
average_inter_arrival_time = np.mean(inter_arrival_times)

# Tentukan berapa banyak job yang mau di-sample
sample_length = int(0.3 * len(original_jobs))  # misal ambil 30% dari job
sampled_jobs = random.sample(original_jobs, sample_length)

# Siapkan struktur dataset sampled
sampled_dataset = {
    'nb_res': original_data['nb_res'],
    'jobs': [],
    'profiles': original_data['profiles']
}

# Generate job baru dengan subtime yang diatur ulang
current_time = 0
job_id = 1

for i in range(len(sampled_jobs)):
    if i > 0:
        time_diff = np.random.exponential(average_inter_arrival_time)
        current_time += time_diff

    job = {
        'id': str(job_id),
        'res': sampled_jobs[i]['res'],
        'subtime': int(round(current_time)),
        'walltime': sampled_jobs[i]['walltime'],
        'profile': sampled_jobs[i]['profile'],
        'user_id': sampled_jobs[i]['user_id']
    }

    sampled_dataset['jobs'].append(job)
    job_id += 1

# Simpan hasilnya ke file JSON
with open('sampled_dataset.json', 'w') as outfile:
    json.dump(sampled_dataset, outfile, indent=4)

print(f"Sampled dataset berhasil disimpan. Jumlah job: {len(sampled_jobs)}")