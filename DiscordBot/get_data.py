import json
def get_data():
    with open("data.json",'r') as f:
        data = json.load(f)
    return data