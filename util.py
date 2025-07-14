import json

import requests


def get_servers(api_key: str) -> list | str:
    # Perform servers command to list running servers
    url, port = get_url_and_port()
    servers_url = f"{url}:{port}/servers"
    headers = {"x-api-key": api_key}

    response = requests.get(servers_url, headers=headers)

    if response.status_code == 200:
        servers_data = response.json()
        return servers_data["servers"]
    else:
        print(
            f"Failed to retrieve running servers. Status code: {response.status_code}"
        )
        return response.json()["message"]


def get_url_and_port() -> tuple[str, str]:
    # Read settings from config.json
    with open("config.json") as config_file:
        data = json.load(config_file)
        return data["url"], data["port"]


def get_api_key() -> str:
    # Read API key from api_key.txt
    with open("api_key.txt") as api_key_file:
        return api_key_file.read().strip()
