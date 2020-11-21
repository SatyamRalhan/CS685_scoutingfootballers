import json 
with open('neighbor-districts.json') as f:
	data = json.load(f)
print(data)