import os
import shutil
from datetime import datetime
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import argparse

def get_exif_date_taken(file_path):
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if exif_data:
            for tag, val in exif_data.items():
                if TAGS.get(tag) == 'DateTimeOriginal':
                    return datetime.strptime(val, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print(f"EXIF error for {file_path}: {e}")
    return None

def get_file_modification_date(file_path):
    t = os.path.getmtime(file_path)
    return datetime.fromtimestamp(t)

def get_target_path(base_dir, date_obj, structure):
    path_parts = [str(date_obj.year)]
    if structure in ['month', 'day']:
        path_parts.append(f"{date_obj.month:02}")
    if structure == 'day':
        path_parts.append(f"{date_obj.day:02}")
    return os.path.join(base_dir, *path_parts)

def unique_path(dest_path):
    """
    If dest_path exists, add suffix _1, _2, etc. before the extension until unique.
    """
    if not os.path.exists(dest_path):
        return dest_path

    base, ext = os.path.splitext(dest_path)
    counter = 1
    new_path = f"{base}_{counter}{ext}"
    while os.path.exists(new_path):
        counter += 1
        new_path = f"{base}_{counter}{ext}"
    return new_path

def organize_files_with_preview(source_dir, output_dir, structure='year'):
    supported = ('.jpg', '.jpeg', '.mp4')
    # List only files in the top-level source_dir (no subdirectories)
    files = [os.path.join(source_dir, f) for f in os.listdir(source_dir)
             if os.path.isfile(os.path.join(source_dir, f)) and f.lower().endswith(supported)]
    actions = []

    print("\nProposed file moves:\n")

    for file_path in files:
        ext = file_path.lower().split('.')[-1]

        if ext in ['jpg', 'jpeg']:
            date_taken = get_exif_date_taken(file_path) or get_file_modification_date(file_path)
        elif ext == 'mp4':
            date_taken = get_file_modification_date(file_path)
        else:
            continue

        target_folder = get_target_path(output_dir, date_taken, structure)
        os.makedirs(target_folder, exist_ok=True)

        target_path = os.path.join(target_folder, os.path.basename(file_path))
        unique_target_path = unique_path(target_path)  # handle duplicates

        actions.append((file_path, unique_target_path))
        print(f"{file_path}  ->  {unique_target_path}")

    # Confirm with user
    print("\nDo you want to proceed with moving these files? [y/n]")
    choice = input("> ").strip().lower()

    if choice != 'y':
        print("Operation cancelled.")
        return

    print("\nMoving files...\n")
    for src, dst in actions:
        try:
            shutil.move(src, dst)
            print(f"Moved: {src} -> {dst}")
        except Exception as e:
            print(f"Failed to move {src}: {e}")

    print("\nDone.")

if __name__ == '__main__':
    # Hardcoded paths example, change as needed
    source = r"A:\OneDrive\Photos\Unsorted"
    output = r"A:\OneDrive\Photos\Organized"
    structure = "day"  # Options: "year", "month", "day"

    organize_files_with_preview(source, output, structure)
