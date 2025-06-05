Duplicate Photo & Video Finder with Safe Deletion

This Python script scans two specified folders (including all their subdirectories) for duplicate .jpg, .jpeg, and .mp4 files by comparing their SHA256 hashes. It identifies files in Folder 1 that are duplicates of files in Folder 2 and offers to safely delete those duplicates from Folder 1 by moving them to the recycle bin.

Features

    Recursively scans both folders for supported media files.

    Automatically excludes nested folder scanning if one folder is inside the other to avoid double counting.

    Uses SHA256 hashing for accurate duplicate detection.

    Provides progress feedback in the terminal during hashing.

    Prompts for user confirmation before deleting any files.

    Safely deletes files by moving them to the recycle bin using the send2trash library (so files can be restored later).

Requirements

    Python 3.6 or higher

    send2trash library

To install dependencies, run:

pip install send2trash

Usage

    Clone or download this repository.

    Open the script and set your folder paths in the main() function:

folder1 = r"YOUR_FOLDER_1_PATH"

folder2 = r"YOUR_FOLDER_2_PATH"

    Run the script:

python duplicate_finder.py

    Watch the progress as the script hashes files.

    After scanning, if duplicates are found in Folder 1 that also exist in Folder 2, you will be prompted to confirm deletion.

    Type 'yes' to move duplicates to the recycle bin or anything else to cancel.

How It Works

    The script gathers all .jpg, .jpeg, and .mp4 files recursively from both folders.

    If Folder 1 is inside Folder 2, scanning Folder 2 excludes Folder 1, and vice versa.

    Each file’s SHA256 hash is computed for precise comparison.

    Files in Folder 1 that have identical hashes to files in Folder 2 are listed as duplicates.

    Upon confirmation, these duplicates are moved to the recycle bin instead of being permanently deleted.

Important Notes

    Deletion is only performed on Folder 1.

    The use of send2trash ensures files are not permanently deleted immediately.

    Make sure you have sufficient permissions to delete/move files in Folder 1.

    The script processes files case-insensitively for extensions (.jpg, .jpeg, .mp4).