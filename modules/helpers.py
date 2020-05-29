import json

def read_file(filename):
    return json.load(open(filename))


def write_file(filename, data):
    json.dump(data, open(filename, "w+"))
