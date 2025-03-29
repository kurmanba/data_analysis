import os
import re
import shutil
import sys


def get_folder_index(num):
    """Returns the appropriate folder index based on number ranges."""
    if num <= 50:
        return 1
    elif num <= 100:
        return 2
    elif num <= 150:
        return 3
    elif num <= 200:
        return 4
    elif num <= 250:
        return 5
    else:
        return 6


def organize_csv_files(base_path):
    # Ensure directories 1-6 exist
    for i in range(1, 7):
        os.makedirs(os.path.join(base_path, str(i)), exist_ok=True)

    # Regex pattern to match filenames like TEK00000.CSV (case insensitive)
    pattern = re.compile(r"TEK(\d{5})\.CSV", re.IGNORECASE)

    # Scan for matching files
    for filename in os.listdir(base_path):
        match = pattern.match(filename)
        if match:
            num = int(match.group(1))  # Extract the numeric part
            folder_index = get_folder_index(num)  # Assign correct folder
            src = os.path.join(base_path, filename)
            dest = os.path.join(base_path, str(folder_index), filename)
            shutil.move(src, dest)
            print(f"Moved {filename} to folder {folder_index}")


# base_directory = "/Users/alisher/IdeaProjects/TEB_REMAKE/Experimtents/EG_00625_standard"  # Change this to the directory where CSVs are located
# organize_csv_files(base_directory)


def print_tree(directory, indent=""):
    try:
        entries = sorted(os.listdir(directory))  # Sort for consistent order
        for i, entry in enumerate(entries):
            path = os.path.join(directory, entry)
            is_last = (i == len(entries) - 1)
            prefix = "└── " if is_last else "├── "
            print(indent + prefix + entry)
            if os.path.isdir(path):
                new_indent = indent + ("    " if is_last else "│   ")
                print_tree(path, new_indent)
    except PermissionError:
        print(indent + "└── [Permission Denied]")


if __name__ == "__main__":
    directory = "/Users/alisher/IdeaProjects/TEB_REMAKE/raw_data"
    # print_tree(directory)
    folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

    # Print the folders
    for root, dirs, _ in os.walk(directory):
        for dir_name in dirs:
            print(os.path.join(root, dir_name))