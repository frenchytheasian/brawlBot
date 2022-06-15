import json

def read_json():
    with open("data.json", "r") as infile:
        data = json.load(infile)
    return data

if __name__ == "__main__":
    data = read_json()
    print(type(data))