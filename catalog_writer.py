import json
import struct
import os
from pathlib import Path

CATALOG = "catalog.json"

def read_pascal_string(file):
    #godot stores 4 bytes of pascal string length
    length_bytes = file.read(4)
    if not length_bytes: return ""

    string_length = struct.unpack('<I', length_bytes)[0]
    string_bytes = file.read(string_length)

    return string_bytes.decode("utf-8")



def read_exercises():
    exercise_dir = Path('./exercises')
    MAGIC = "EXERCISE"

    result = {}

    for item in exercise_dir.rglob('*'):
        if not item.is_file(): continue
        with open(item, "rb") as file:
            if read_pascal_string(file) != MAGIC: continue
            file.seek(9, os.SEEK_CUR) #skipping version and offsets
            id = read_pascal_string(file)
            result[id] = {
                "exercise_name" : read_pascal_string(file),
                "song_name" : read_pascal_string(file),
                "path" : item.as_posix()
            }
    return result

catalog = {}
with open(CATALOG, 'r', encoding="utf-8") as file:
    catalog = json.load(file)

exercises = read_exercises()
new_count = 0
for id in exercises:
    if not id in catalog["exercises"]:
        catalog["exercises"][id] = exercises[id]
        new_count += 1

with open(CATALOG, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, ensure_ascii=False, indent=4, sort_keys=True)

print(f"✅ Found {len(exercises)} exercises, {new_count} new ones added")





