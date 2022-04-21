import json


def get_config(SCRIPT_PATH):
    with open(f"{SCRIPT_PATH}/misc/config.json", "r") as f:
        data = f.read()
    return json.loads(data)


def set_config(config, SCRIPT_PATH):
    with open(f"{SCRIPT_PATH}/misc/config.json", "w") as f:
        f.write(json.dumps(config, indent=4))
