from textual.app import App, ComposeResult, on
from textual.containers import Center, Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, RichLog


class StyledHeader(Header):
    DEFAULT_CSS = """
    Header {
        height: 3;
        dock: top;
        background: #1e1e1e;
        color: #ffffff;
    }
    """


class StyledFooter(Footer):
    DEFAULT_CSS = """
    Footer {
        height: 3;
        dock: bottom;
        background: #1e1e1e;
        color: #ffffff;
    }
    """


class ColumnsContainer(Vertical):
    DEFAULT_CSS = """
    ColumnsContainer {
        width: 1fr;
        height: 1fr;
        border: solid #4a4a4a;
        background: #282828;
    }
    """


class InputContainer(Container):
    DEFAULT_CSS = """
    InputContainer {
        height: auto;
        dock: bottom;
        padding: 1;
        background: #1e1e1e;
        layout: horizontal;
    }
    """


class SubmitButton(Button):
    DEFAULT_CSS = """
    SubmitButton {
        width: auto;
        background: #4a4a4a;
        color: #ffffff;
        margin-left: 1;
    }
    """


class MCConsoleCLI(Screen):
    CSS = """
    #sidebar {
        dock: right;
        width: 20;
        height: 100%;
        color: #ffffff;
        background: #333333;
        border: solid #4a4a4a;
        scrollbar-size: 0 0;
    }

    #output {
        color: #ffffff;
        border: solid #4a4a4a;
    }

    #input {
        background: #1e1e1e;
        color: #ffffff;
        border: solid #4a4a4a;
        width: 90%;
    }
    """

    def compose(self) -> ComposeResult:
        yield StyledHeader(id="header")
        yield StyledFooter(id="footer")
        with ColumnsContainer(id="output-columns"):
            self.output = RichLog(id="output")
            self.output.write("Output Test")
            yield self.output
            self.sidebar = RichLog(id="sidebar")
            self.sidebar.write("Sidebar Test")
            yield self.sidebar
        with InputContainer(id="input-columns"):
            yield Input(id="input", placeholder="Send a Command")
            yield Center(SubmitButton("Submit", id="submit"))

    @on(Input.Submitted, "#input")
    def input_submit(self, event):
        self.output.write(event.value)
        event.input.value = ""

    @on(Button.Pressed, "#submit")
    def button_submit(self):
        _input = self.query_one("#input", Input)
        input_value = _input.value
        self.output.write(input_value)
        _input.value = ""


class MCConsoleCLILayout(App):
    def on_mount(self) -> None:
        self.title = "MCConsoleCLI"
        self.push_screen(MCConsoleCLI())


if __name__ == "__main__":
    app = MCConsoleCLILayout()
    app.run()
