import os
import datetime
from pathlib import Path

def classify_file(file_path, by_date=False):
    """Classify a file by type (extension) and optionally by date."""
    ext = Path(file_path).suffix.lower()
    if ext in ['.txt', '.doc', '.docx', '.pdf', '.md']:
        folder = 'Documents'
    elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
        folder = 'Images'
    elif ext in ['.mp4', '.avi', '.mov', '.mkv']:
        folder = 'Videos'
    elif ext in ['.xls', '.xlsx', '.csv']:
        folder = 'Spreadsheets'
    elif ext in ['.ppt', '.pptx']:
        folder = 'Presentations'
    elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
        folder = 'Archives'
    else:
        folder = 'Other'

    if by_date:
        # Use file creation or modification year-month as subfolder
        try:
            timestamp = os.path.getmtime(file_path)
        except Exception:
            timestamp = None
        if timestamp:
            date_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m')
            folder = os.path.join(folder, date_str)
    return folder
