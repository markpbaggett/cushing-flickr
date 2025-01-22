import os
import json
from csv import DictWriter, DictReader


all_fields = []
all_files={}
all_records = []
fields_to_check = []
for path, dirs, files in os.walk("output"):
    for filename in files:
        current_file = json.load(open(os.path.join(path, filename)))
        flickr_url = [url['_content'] for url in current_file['metadata']['photo']['urls']['url'] if url['type'] == "photopage"][0]
        all_files[flickr_url] = current_file

with open('unique_fields.txt', 'r') as uniques:
    for line in uniques:
        fields_to_check.append(line.strip())


with open('missing.txt', 'r') as f:
    for line in f:
        key = line.strip()
        metadata = all_files[key]['metadata']['photo']['descriptive_metadata']
        try:
            record = {
                'Item title': all_files[key]['metadata']['photo']['title']['_content'],
                'Item link': [file['source'] for file in all_files[key]['sizes']['sizes']['size'] if file['label'] == "Original"][0],
                'Medium Image': [file['source'] for file in all_files[key]['sizes']['sizes']['size'] if file['label'] == "Medium"][0],
            }
        except IndexError as e:
            record = {
                'Item title': all_files[key]['metadata']['photo']['title']['_content'],
                'Item link': [file['source'] for file in all_files[key]['sizes']['sizes']['size'] if
                              file['label'] == "Original"][0],
                'Medium Image':
                    [file['source'] for file in all_files[key]['sizes']['sizes']['size'] if file['label'] == "Small 320"][
                        0],
            }
        for field in fields_to_check:
            record[field] = ""
        for k, v in metadata.items():
            # if k.strip() not in all_fields and v.strip() != "":
            #     all_fields.append(k.strip())
            if k.strip() in fields_to_check and v.strip() != "":
                record[k.strip()] = v.strip()
        all_records.append(record)

with open('migration.csv', 'w') as csvfile:
    writer = DictWriter(csvfile, fieldnames=all_records[0].keys())
    writer.writeheader()
    writer.writerows(all_records)
