import argparse
import json

import requests

from ui import MCConsoleCLI

# Read settings from config.json
with open("config.json") as config_file:
    config = json.load(config_file)

url = config["url"]
port = config["port"]

# Read API key from api_key.txt
with open("api_key.txt") as api_key_file:
    api_key = api_key_file.read().strip()

# Parse command line arguments
parser = argparse.ArgumentParser(description="CLI tool to interact with an HTTP server")
parser.add_argument("command", help="Command to execute (start)")
parser.add_argument(
    "server_name", nargs="?", help="Server name (required for start command)"
)
parser.add_argument(
    "server_path", nargs="?", help="Server path (optional for start command)"
)

args = parser.parse_args()

# Start server command
if args.command == "start":
    if args.server_name:
        # Perform start action with the specified server name and optional server path
        start_url = f"{url}:{port}/start_server"
        headers = {"x-api-key": api_key}
        params = {"server_name": args.server_name}

        if args.server_path:
            params["server_path"] = args.server_path

        response = requests.post(start_url, headers=headers, params=params)

        if response.status_code == 200:
            message = response.json()["message"]
            print(message)
        else:
            print(
                f"Failed to start server '{args.server_name}'. Status code: {response.status_code}"
            )
            message = response.json()["message"]
            print(message)
    else:
        print("Please provide a server name for the start command.")

# Stop server command
elif args.command == "stop":
    if args.server_name:
        # Perform stop action with the specified server name
        stop_url = f"{url}:{port}/stop_server"
        headers = {"x-api-key": api_key}
        params = {"server_name": args.server_name}

        response = requests.post(stop_url, headers=headers, params=params)

        if response.status_code == 200:
            message = response.json()["message"]
            print(message)
        else:
            print(
                f"Failed to stop server '{args.server_name}'. Status code: {response.status_code}"
            )
            message = response.json()["message"]
            print(message)
    else:
        print("Please provide a server name for the stop command.")

# List servers command
elif args.command == "servers":
    # Perform servers command to list running servers
    servers_url = f"{url}:{port}/servers"
    headers = {"x-api-key": api_key}

    response = requests.get(servers_url, headers=headers)

    if response.status_code == 200:
        servers_data = response.json()
        servers = servers_data["servers"]

        if len(servers) > 0:
            print("Running servers:")
            for server in servers:
                print(f"  Server Name: {server['name']}")
                print(f"  Server Path: {server['path']}")
                print()
        else:
            print("No running servers found.")
    else:
        print(
            f"Failed to retrieve running servers. Status code: {response.status_code}"
        )
        message = response.json()["message"]
        print(message)

# Starts the textual UI
elif args.command == "attach":
    app = MCConsoleCLI()
    app.run()

else:
    print(f"Invalid command: {args.command}")
