import json
import copy

# Step 1: Baca data dari file
with open('data/nasa_workload.txt', 'r') as file:
    data_txt = file.read()

# Step 2: Parsing ke data_list
data_list = []

# Split the lines and create a list of dictionaries
for line in data_txt.split('\n'):
    if line.startswith(';') or line.strip() == '':
        continue
    
    data_dict = {}
    values = line.split()
    values = [int(value) for value in values]  # Convert values to int

    # Create a dictionary using values and keys
    data_dict = {
        "id": values[0],
        "res": values[4],
        "subtime": values[1],
        "walltime": values[3],
        "profile": "100",
        "user_id": 0
    }

    data_list.append(data_dict)

# Step 3: Split dataset (80:20)
train_size = int(0.8 * len(data_list))  # split dataset
train_data = data_list[:train_size]
test_data = data_list[train_size:]

# Step 4: Bikin dataset dasar
profile = {
    "100": {
        "cpu": 100000000,
        "com": 0,
        "type": "parallel_homogeneous"
    }
}

dataset = {
    "nb_res": 128,
    "profiles": profile,
    "jobs": []
}

# Step 5: Salin dataset & masukkan data train dan test
train_dataset = copy.deepcopy(dataset)
test_dataset = copy.deepcopy(dataset)

train_dataset["jobs"].append(train_data)
test_dataset["jobs"].append(test_data)

# Step 6: Reset subtime pada test data
test_base_subtime = test_dataset["jobs"][0][0]["subtime"]
for i in range(len(test_dataset["jobs"][0])):
    test_dataset["jobs"][0][i]["subtime"] -= test_base_subtime

# Step 7: Simpan ke file JSON
train_json_data = json.dumps(train_dataset, indent=2)
test_json_data = json.dumps(test_dataset, indent=2)

with open("nasa-train.json", "w") as outfile:
    outfile.write(train_json_data)

with open("nasa-test.json", "w") as outfile:
    outfile.write(test_json_data)