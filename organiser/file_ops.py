# File operations: moving, renaming, folder creation



import os
import shutil
from pathlib import Path


def list_files(source_folder):
    return [str(p) for p in Path(source_folder).rglob('*') if p.is_file()]


def create_folder(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def move_file(src, dest):
    shutil.move(src, dest)


def get_human_readable_folder(file_path):
    ext = Path(file_path).suffix.lower()
    if ext in ['.txt', '.doc', '.docx', '.pdf']:
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
