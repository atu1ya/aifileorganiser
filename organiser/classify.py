import os
from pathlib import Path

def classify_file(file_path):
    """Classify a file by type (extension)."""
    ext = Path(file_path).suffix.lower()
    if ext in ['.txt', '.doc', '.docx', '.pdf', '.md']:
        return 'Documents'
    elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
        return 'Images'
    elif ext in ['.mp4', '.avi', '.mov', '.mkv']:
        return 'Videos'
    elif ext in ['.xls', '.xlsx', '.csv']:
        return 'Spreadsheets'
    elif ext in ['.ppt', '.pptx']:
        return 'Presentations'
    elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
        return 'Archives'
    else:
        return 'Other'
