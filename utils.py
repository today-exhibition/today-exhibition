import json


def load_secrets():
    with open("./secrets.json", "r") as secrets_file:
        secrets = json.load(secrets_file)
    return secrets