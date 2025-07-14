import argparse

import requests

from ui import MCConsoleCLI
from util import get_api_key, get_url_and_port, get_servers


url, port = get_url_and_port()
api_key = get_api_key()

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
        start_url = f"{url}:{port}/servers/{args.server_name}/start"
        headers = {"x-api-key": api_key}
        params = {}

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
        stop_url = f"{url}:{port}/servers/{args.server_name}/stop"
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
elif args.command == "list":
    servers = get_servers(api_key)
    if isinstance(servers, list):
        if len(servers) > 0:
            print("Running Minecraft Servers:")
            for server in servers:
                print(f"  Server Name: {server['name']}")
                print(f"  Server Path: {server['path']}")
                print()
        else:
            print("No Minecraft Servers are running")
    else:
        # Error messages
        print(servers)

# Starts the textual UI
elif args.command == "attach":
    app = MCConsoleCLI()
    app.run()
else:
    print(f"Invalid command: {args.command}")
