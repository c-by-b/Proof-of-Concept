# Proof-of-Concept/config.py
import os
import socket
import yaml


_config = None
_online_status = None

def load_config():
    global _config
    if _config is None:
        config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        with open(config_path, "r") as f:
            _config = yaml.safe_load(f)
    return _config

def set_online_status(status: bool | None):
    global _online_status
    _online_status = status

def get_online_status():
    global _online_status
    if _online_status is not None:
        return _online_status

    env_val = os.getenv("CBYB_ONLINE_STATUS")
    if env_val is not None:
        return env_val.lower() == "online"

    config = _load_config()
    yaml_val = config.get("online")
    if yaml_val is not None:
        return bool(yaml_val)

    return _auto_detect_online()

def _auto_detect_online():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False
