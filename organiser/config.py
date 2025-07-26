import os
import json

CONFIG_FILE = os.path.expanduser('~/.aifileorganiser_config.json')

DEFAULT_CONFIG = {
    "last_source_folder": "",
    "last_destination_folder": "",
    "use_ai_sorting": False,
    "by_date": False
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load config: {e}")
    return DEFAULT_CONFIG.copy()

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to save config: {e}")

def update_config(**kwargs):
    config = load_config()
    config.update(kwargs)
    save_config(config)
