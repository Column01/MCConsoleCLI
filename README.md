# MCConsoleCLI

This is a command-line interface (CLI) tool that interacts with a [MCConsoleAPI](https://github.com/Column01/MCConsoleAPI) to start and stop servers, as well as list running servers.

## Installation

1. Install Python 3.11+
2. Clone (or download) the repo: `git clone https://github.com/Column01/MCConsoleCLI && cd MCConsoleCLI`
3. Install with pip: `python -m pip install .`

## Configuration

1. Edit the `config.json` file inside the CLI directory and enter the url and port for your API server

2. Create an `api_key.txt` file in the same directory as the script and place your API key in it as a single line of text.

## Usage

To use the CLI tool, you can run the main script with the following command:

```bash
mcc-cli <command> [server_name] [server_path]
```

### Commands

- `start`: Start a server with the specified server name and optional server path.
  - `server_name`: Required argument specifying the name of the server to start.
  - `server_path`: Optional argument specifying the path of the server to start.

- `stop`: Stop a server with the specified server name.
  - `server_name`: Required argument specifying the name of the server to stop.

- `list`: List all running servers.

- `attach`: Starts an instance of the (**WIP**) terminal UI

### Examples

Start a server:

```bash
mcc-cli start my_server /path/to/server
```

Stop a server:

```bash
mcc-cli stop my_server
```

List running servers:

```bash
mcc-cli list
```

Start the (wip) terminal UI:

```bash
mcc-cli attach
```
