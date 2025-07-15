from textual.app import App, ComposeResult, on
from textual.containers import Center
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, RichLog, Select

from .server import Server
from .util import get_api_key, get_servers, get_url_and_port
from .widgets import ColumnsContainer, InputContainer


class MCConsoleCLIScreen(Screen):
    CSS = """
    #sidebar {
        dock: right;
        width: 20;
        height: 100%;
        border: solid #4a4a4a;
        scrollbar-size: 0 0;
    }

    #output {
        border: solid #4a4a4a;
    }

    #input {
        border: solid #4a4a4a;
        width: 75%;
    }

    Header {
        dock: top;
    }

    Footer {
        dock: bottom;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(id="header")
        yield Footer(id="footer")

        with ColumnsContainer(id="output-columns"):
            self.output = RichLog(id="output")
            self.output.write("Output Test")
            yield self.output
            self.sidebar = RichLog(id="sidebar")
            self.sidebar.write("Sidebar Test")
            yield self.sidebar
        with InputContainer(id="input-columns"):
            yield Input(id="input", placeholder="Send a Command")
            yield Center(Button("Submit", id="submit"))
            self.dropdown = Select(id="dropdown", options=[])
            yield Center(self.dropdown)

    @on(Input.Submitted, "#input")
    def input_submit(self, event):
        print(event.value)
        if event.value != "":
            self.output.write(event.value)
            event.input.value = ""

    @on(Button.Pressed, "#submit")
    def button_submit(self):
        _input = self.query_one("#input", Input)
        input_value = _input.value
        if input_value != "":
            self.output.write(input_value)
            _input.value = ""


class MCConsoleCLI(App):
    def on_mount(self) -> None:
        self._screen = MCConsoleCLIScreen()
        self.push_screen(self._screen)

        # Call the app initialization function once the UI is setup
        self.call_later(self.initialize_app)

    def on_unmount(self) -> None:
        for server in self.servers.values():
            server.stop()
        exit(0)

    async def initialize_app(self):
        # Cache of connected server consoles
        self.servers = {}

        # Get some configuration info
        self.url, self.port = get_url_and_port()
        self.api_key = get_api_key()

        # Gets a list of servers
        await self.refresh_servers()

    async def refresh_servers(self) -> None:
        # Remove no longer running servers
        to_remove = [
            server
            for server in self.servers.keys()
            if self.servers[server].stop_event.is_set()
        ]
        _ = [self.servers.pop(server, None) for server in to_remove]

        server_list = get_servers(self.api_key)
        if isinstance(server_list, str):
            quit(server_list)
        elif len(server_list) == 0:
            quit("No servers running. You can start one using the `start` command")
        else:
            # Make a connection to all running servers
            for server in server_list:
                server_name = server["name"]
                if server_name not in self.servers:
                    self.servers[server_name] = Server(self, server_name)

            # Populate the dropdown with the servers list
            options = [(item["name"], item["name"]) for item in server_list]
            self._screen.dropdown.set_options(options)


if __name__ == "__main__":
    app = MCConsoleCLI()
    app.run()
