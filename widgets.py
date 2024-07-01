from textual.containers import Container, Vertical
from textual.widgets import Button, Footer, Header


class StyledHeader(Header):
    DEFAULT_CSS = """
    StyledHeader {
        dock: top;
        background: #1e1e1e;
        color: #ffffff;
    }
    """


class StyledFooter(Footer):
    DEFAULT_CSS = """
    StyledFooter {
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
    }
    """
