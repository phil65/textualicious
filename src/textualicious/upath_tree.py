"""Textual widget for browsing local and remote filesystems using upath."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.widgets import DirectoryTree
from upath import UPath


if TYPE_CHECKING:
    import os


class UniversalDirectoryTree(DirectoryTree):
    """DirectoryTree widget supporting local and remote filesystems via upath."""

    PATH = UPath


def show_path(path: str | os.PathLike[str]) -> None:
    """Show the contents of a path in a UniversalDirectoryTree widget."""
    from textual.app import App, ComposeResult
    from textual.widgets import Footer, Header

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


if __name__ == "__main__":
    show_path("github://phil65:mknodes@main")
