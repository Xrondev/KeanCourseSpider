import json

with open('info/searchInfo_1.json', 'r') as file:
    s = file.read()
    info = json.loads(s)

print(info['Sections'])