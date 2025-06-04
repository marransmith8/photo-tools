# Photo & Video Organizer by Date

This Python script organizes `.jpg`, `.jpeg`, and `.mp4` files from a specified source directory into folders by the date the photos or videos were taken or created. It supports organizing by year, month, and day, with an option to only scan the top-level folder (no subdirectories).

## Features

- Organizes files into folders by:
  - Year only (`year`)
  - Year and month (`month`)
  - Year, month, and day (`day`)
- Reads EXIF metadata to get the original date for photos
- Uses file modification date for videos
- Scans only the top-level folder of the source directory (does not recurse into subfolders)
- Prevents overwriting by automatically renaming duplicate files with a suffix (`_1`, `_2`, etc.)
- Displays a preview of file moves and asks for confirmation before proceeding

## Requirements

- Python 3.6 or higher
- [Pillow](https://python-pillow.org/) library for image metadata extraction

### Installation

Install the required library via pip:

```bash
pip install Pillow