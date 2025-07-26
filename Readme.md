
# AI File Organiser

## Overview
A Python desktop app that automatically organises files, detects duplicates, and uses local AI models for smart sorting. Runs fully offline and cross-platform (Windows/macOS).

## Features
- File classification by extension
- Human-readable folder structure
- Duplicate detection (SHA-256, optional fuzzy matching)
- Optional AI-powered sorting and folder naming
- Simple PySide6 GUI
- Logging and stats

## Requirements
- Python 3.11+
- Windows or macOS
- Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```

## Usage
1. Run the app:
   ```sh
   python -m organiser.main
   ```
2. Use the GUI to select source/destination folders and options.
3. View logs in `organiser.log`.

## Packaging
- To create an executable:
  ```sh
  pyinstaller organiser/main.py
  ```
  Output will be in the `dist` folder.

## Notes
- All AI features run locally (no cloud APIs).
- Files are moved, not deleted automatically.
- Cross-platform file operations via `os`, `shutil`, `pathlib`.
- For fuzzy duplicate detection, install `pyssdeep`.
- For AI sorting, install `sentence-transformers`, `scikit-learn`, `numpy`.
- For local LLM folder naming, integrate with Ollama or llama.cpp.

## License
MIT
