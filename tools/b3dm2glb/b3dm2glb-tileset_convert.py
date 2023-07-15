import os
import json
import argparse
import time

b3dm_counter = 0
json_counter = 0

def convert_b3dm_to_glb(file_abs_path):
    global b3dm_counter
    glb_abs_path = file_abs_path.replace(".b3dm", ".glb")
    try:
        if os.path.exists(glb_abs_path):
            print(f"GLB file already exists: {glb_abs_path}")
        else:
            with open(file_abs_path, "rb") as f:
                b3dm_data = f.read()
            marker = b'glTF'
            marker_pos = b3dm_data.find(marker)
            with open(glb_abs_path, "wb") as f:
                f.write(b3dm_data[marker_pos:])
            os.remove(file_abs_path)
            b3dm_counter += 1
    except PermissionError:
        print(f"Permission denied when processing file: {file_abs_path}")
    except OSError:
        print(f"Not enough disk space to write file: {glb_abs_path}")

def replace_b3dm_with_glb(node, base_path):
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ["url", "uri"] and value.endswith(".b3dm"):
                node[key] = value.replace(".b3dm", ".glb")
                file_abs_path = os.path.join(base_path, value)
                convert_b3dm_to_glb(file_abs_path)
            elif isinstance(value, (dict, list)):
                replace_b3dm_with_glb(value, base_path)
    elif isinstance(node, list):
        for item in node:
            if isinstance(item, (dict, list)):
                replace_b3dm_with_glb(item, base_path)

def update_json(file_abs_path):
    global json_counter
    try:
        with open(file_abs_path, "r") as f:
            file_data = json.load(f)
        replace_b3dm_with_glb(file_data, os.path.dirname(file_abs_path))
        with open(file_abs_path, "w") as f:
            json.dump(file_data, f, indent=4)
        json_counter += 1
    except json.JSONDecodeError:
        print(f"Invalid JSON in file: {file_abs_path}")
    except PermissionError:
        print(f"Permission denied when reading or writing file: {file_abs_path}")
    except OSError:
        print(f"Not enough disk space to write file: {file_abs_path}")

parser = argparse.ArgumentParser(description="Convert .b3dm files to .glb and update json.")
parser.add_argument("directory_path", help="Path to the directory containing the json and .b3dm files.")
args = parser.parse_args()

start_time = time.time()

for root, dirs, files in os.walk(args.directory_path):
    for file in files:
        file_abs_path = os.path.join(root, file)
        if file_abs_path.endswith(".json"):
            update_json(file_abs_path)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
print(f"Processed B3DM files: {b3dm_counter}")
print(f"Processed JSON files: {json_counter}")
