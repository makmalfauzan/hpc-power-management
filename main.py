import json
import copy

with open('nasa_workload.txt', 'r') as file:
    data_txt = file.read()
    
profile = {
    "100": {
        "cpu": 100000000,
        "com": 0,
        "type": "parallel_homogeneous"
    }
}

dataset = {
    "nb_res": 128,
    "job": [],
    "profiles": profile
}