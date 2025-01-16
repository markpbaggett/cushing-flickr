import json
import os


total_comments = 0
for path, directories, files in os.walk("output"):
    for filename in files:
        filepath = os.path.join(path, filename)
        x = json.load(open(filepath))
        try:
            if x['metadata']['photo']['comments']['_content'] != "0":
                try:
                    for comment in x['comments']['comments']['comment']:
                        print(comment)
                        total_comments += 1
                except KeyError:
                    print(f"\n\nKeyerror: {filepath}\n\n")
        except json.decoder.JSONDecodeError:
            print(f"Error: {filepath}")

print(total_comments)