__version__ = "0.1.1"

import os
from textualicious.dataclass_table import DataClassTable
from textualicious.dataclass_viewer import DataClassViewer
from textualicious.log_widget import LoggingWidget
from textualicious.help_screen import HelpScreen


def show_path(path: str | os.PathLike[str]) -> None:
    """Show the contents of a path in a UniversalDirectoryTree widget."""
    from textualicious.upath_tree import UniversalDirectoryTree
    from textual.app import App, ComposeResult
    from textual.widgets import Footer, Header
    from upath import UPath

    path_obj = UPath(path)

    class DemoApp(App):
        """Demo app showing the UniversalDirectoryTree widget."""

        def __init__(self, path: str | os.PathLike[str]) -> None:
            super().__init__()
            self.path = UPath(path)

        def compose(self) -> ComposeResult:
            yield Header()
            yield UniversalDirectoryTree(self.path)
            yield Footer()

    app = DemoApp(path_obj)
    app.run()


__all__ = [
    "DataClassTable",
    "DataClassViewer",
    "HelpScreen",
    "LoggingWidget",
    "show_path",
]
