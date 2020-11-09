import os
import socket
import json


def _merge(destination, *sources):
    for source in sources:
        for key, value in source.items():
            if isinstance(value, dict) and isinstance(destination.get(key, {}), dict):
                destination_value = destination.setdefault(key, {})
                _merge(destination_value, value)
            else:
                destination[key] = value
    return destination


def _load_json_from(path):
    try:
        with open(path) as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def load_config(config_dir=os.path.join(os.getcwd(), "config"),
                secrets_path="/etc/decrypted-config/config.json"):

    def load_config_file(file_name):
        return _load_json_from(os.path.join(config_dir, file_name))

    env = os.getenv("ENV", "local")

    return _merge({},
                  load_config_file("default.json"),
                  load_config_file(f"{env}.json"),
                  _load_json_from(secrets_path))
