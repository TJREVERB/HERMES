import json


def read_file(filename):
    data = json.load(open(filename))
    data = {int(key): data[key] for key in data}
    return data


def write_file(filename, data):
    json.dump(data, open(filename, "w+"))
