import json
import argparse

class DataCombiner:
    def __init__(self, file1, file2, file3):
        self.data1 = self._load_json(file1)
        self.data2 = self._load_json(file2)
        self.data3 = self._load_json(file3)

    def _load_json(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return data

    def combineJob(self):
        jobs1 = self.data1['jobs']
        jobs2 = self.data2['jobs']
        jobs3 = self.data3['jobs']
        for job in jobs2:
            job["subtime"] = jobs1[-1]["subtime"] + job["subtime"]
        for job in jobs3:
            job["subtime"] = jobs2[-1]["subtime"] + job["subtime"]
        combined_jobs = jobs1 + jobs2 + jobs3
        for index, job in enumerate(combined_jobs, start=1):
            job['id'] = index
        return combined_jobs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file1", help="First JSON file")
    parser.add_argument("file2", help="Second JSON file")
    parser.add_argument("file3", help="Third JSON file")
    parser.add_argument("--output", help="Output JSON file", default="combined_dataset.json")
    args = parser.parse_args()

    combiner = DataCombiner(args.file1, args.file2, args.file3)
    combined_jobs = combiner.combineJob()

    with open(args.output, 'w') as outfile:
        json.dump(combined_jobs, outfile, indent=4)

if __name__ == "__main__":
    main()