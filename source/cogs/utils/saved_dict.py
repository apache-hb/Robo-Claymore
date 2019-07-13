import json
from .shortcuts import try_file

class SavedDict:
    def __init__(self, file: str, content: str = '{}'):
        self.file = file
        self.data = json.load(try_file(file, content = content))

    def save(self):
        json.dump(self.data, open(self.file, 'w'), indent = 4)

    def __contains__(self, key):
        return key in self.data

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, val):
        self.data[key] = val

    def items(self):
        return self.data.items()
