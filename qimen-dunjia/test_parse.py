import json

with open('pdf_content.json', 'r') as f:
    d = json.load(f)

for k, v in d.items():
    print(k, len(v))

