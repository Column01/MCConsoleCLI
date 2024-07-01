from textual.containers import Container, Vertical
from textual.widgets import Footer, Header


class StyledHeader(Header):
    DEFAULT_CSS = """
    StyledHeader {
        dock: top;
    }
    """


class StyledFooter(Footer):
    DEFAULT_CSS = """
    StyledFooter {
        dock: bottom;
    }
    """


class ColumnsContainer(Vertical):
    DEFAULT_CSS = """
    ColumnsContainer {
        width: 1fr;
        height: 1fr;
        border: solid #4a4a4a;
    }
    """


class InputContainer(Container):
    DEFAULT_CSS = """
    InputContainer {
        height: auto;
        dock: bottom;
        padding: 1;
        layout: horizontal;
    }
    """
