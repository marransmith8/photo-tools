import os
import hashlib
from send2trash import send2trash

def file_hash(path, chunk_size=8192):
    """Calculate SHA256 hash of a file."""
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(chunk_size):
                h.update(chunk)
    except Exception as e:
        print(f"Failed to hash {path}: {e}")
        return None
    return h.hexdigest()

def gather_files(root_dir, exclude_dir=None, extensions=('.jpg', '.jpeg', '.mp4')):
    """Recursively gather files with given extensions under root_dir, optionally excluding exclude_dir."""
    files = {}
    root_dir = os.path.abspath(root_dir)
    exclude_dir = os.path.abspath(exclude_dir) if exclude_dir else None

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip excluded dir (and its subdirs)
        if exclude_dir and os.path.commonpath([exclude_dir, dirpath]) == exclude_dir:
            continue

        for filename in filenames:
            if filename.lower().endswith(extensions):
                full_path = os.path.join(dirpath, filename)
                files[full_path] = None  # placeholder for hash
    return files

def hash_files(file_paths):
    """Compute hashes for files and return dict hash -> list of files."""
    hash_map = {}
    total = len(file_paths)
    for i, path in enumerate(file_paths, 1):
        h = file_hash(path)
        if h:
            hash_map.setdefault(h, []).append(path)
        # Progress output
        print(f"\rHashing files: {i}/{total} ({(i/total)*100:.1f}%)", end='', flush=True)
    print()  # Newline after progress
    return hash_map

def find_duplicates_with_matches(folder1_hashes, folder2_hashes):
    """Return list of tuples (folder1_file, matching_folder2_file) for duplicates."""
    duplicates = []
    for h in folder1_hashes:
        if h in folder2_hashes:
            # For each duplicate in Folder 1, pair with first match in Folder 2
            for file1 in folder1_hashes[h]:
                file2 = folder2_hashes[h][0]
                duplicates.append((file1, file2))
    return duplicates

def confirm_delete(duplicates):
    print(f"\nFound {len(duplicates)} duplicate files in Folder 1 that also exist in Folder 2.")
    print("Files to be deleted from Folder 1 (moved to recycle bin) with their duplicate in Folder 2:")
    for file1, file2 in duplicates:
        print(f"{file1}  <==>  {file2}")
    print("\nDo you want to move these files to the recycle bin? Type 'yes' to confirm:")
    choice = input("> ").strip().lower()
    return choice == 'yes'

def delete_files(files):
    for f in files:
        try:
            send2trash(f)
            print(f"Moved to recycle bin: {f}")
        except Exception as e:
            print(f"Failed to move to recycle bin {f}: {e}")

def main():
    # Define your folders here:
    folder1 = r"A:\Desktop\Phone Photos\2021"
    folder2 = r"A:\My Photos & Videos\Albums\2022\689 Isle of Arran 06-01-2022y"

    folder1_abs = os.path.abspath(folder1)
    folder2_abs = os.path.abspath(folder2)

    exclude_for_folder1 = None
    exclude_for_folder2 = None

    if os.path.commonpath([folder1_abs, folder2_abs]) == folder1_abs:
        # Folder 2 is inside Folder 1, exclude Folder 2 when scanning Folder 1
        exclude_for_folder1 = folder2_abs
    elif os.path.commonpath([folder1_abs, folder2_abs]) == folder2_abs:
        # Folder 1 is inside Folder 2, exclude Folder 1 when scanning Folder 2
        exclude_for_folder2 = folder1_abs

    print(f"Scanning Folder 1: {folder1} (excluding {exclude_for_folder1})")
    folder1_files = gather_files(folder1, exclude_dir=exclude_for_folder1)

    print(f"Scanning Folder 2: {folder2} (excluding {exclude_for_folder2})")
    folder2_files = gather_files(folder2, exclude_dir=exclude_for_folder2)

    print("Hashing files in Folder 1...")
    folder1_hashes = hash_files(folder1_files.keys())

    print("Hashing files in Folder 2...")
    folder2_hashes = hash_files(folder2_files.keys())

    duplicates = find_duplicates_with_matches(folder1_hashes, folder2_hashes)

    if not duplicates:
        print("No duplicates found.")
        return

    if confirm_delete(duplicates):
        # Only delete the Folder 1 files (first elements in the tuples)
        delete_files([file1 for file1, _ in duplicates])
    else:
        print("Deletion cancelled.")

if __name__ == "__main__":
    main()
