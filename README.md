# MCConsoleCLI

This is a command-line interface (CLI) tool that interacts with a [MCConsoleAPI](https://github.com/Column01/MCConsoleAPI) to start and stop servers, as well as list running servers. I plan to add a proper CLI for working with servers soon!

## Prerequisites

- Python 3.x
- `requests` library (can be installed via `pip install requests`)

## Configuration

1. Edit the `config.json` file and enter the url and port for your API server

2. Create an `api_key.txt` file in the same directory as the script and place your API key in it as a single line of text.

## Usage

To use the CLI tool, run the script with the appropriate command and arguments:

```bash
python main.py <command> [server_name] [server_path]
```

### Commands

- `start`: Start a server with the specified server name and optional server path.
  - `server_name`: Required argument specifying the name of the server to start.
  - `server_path`: Optional argument specifying the path of the server to start.

- `stop`: Stop a server with the specified server name.
  - `server_name`: Required argument specifying the name of the server to stop.

- `servers`: List all running servers.

### Examples

Start a server:

```bash
python main.py start my_server /path/to/server
```

Stop a server:

```bash
python main.py stop my_server
```

List running servers:

```bash
python main.py servers
```
