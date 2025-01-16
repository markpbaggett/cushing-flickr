import os
from csv import DictReader
import json

all_data = []
oak_trust_items_in_flickr=[]
all_items_in_flickr=[]
missing_items_in_flickr=[]
with open("oaktrust_metadata.csv", "r") as f:
    reader = DictReader(f)
    for row in reader:
        all_data.append(row)

for item in all_data:
    if 'dc.identifier.other' in item:
        flickr_url = [item.split("r:")[-1].strip() for item in item['dc.identifier.other'].split("||") if "Flickr" in item][0]
        oak_trust_items_in_flickr.append(flickr_url.replace('http:', "https:"))

for path, dirs, files in os.walk("output"):
    for file in files:
        data = json.load(open(os.path.join(path, file), "r"))
        try:
            flickr_url = [url['_content'] for url in data['metadata']['photo']['urls']['url'] if url['type'] == "photopage"][0]
            all_items_in_flickr.append(flickr_url)
        except:
            print(file)

for item in all_items_in_flickr:
    if item not in oak_trust_items_in_flickr:
        missing_items_in_flickr.append(item)

for item in missing_items_in_flickr:
    print(item)

# print(missing_items_in_flickr[0])
# print(oak_trust_items_in_flickr[0])