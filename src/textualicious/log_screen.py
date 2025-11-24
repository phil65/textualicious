"""Textual log screen."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from textual.binding import Binding
from textual.containers import Container
from textual.screen import ModalScreen


if TYPE_CHECKING:
    from textual.app import ComposeResult

    from textualicious import LoggingWidget


class LogWindow(ModalScreen[None]):
    """Modal window showing application logs."""

    BINDINGS: ClassVar = [
        Binding("escape", "app.pop_screen", "Close"),
        Binding("c", "clear", "Clear"),
    ]

    DEFAULT_CSS = """
    LogWindow {
        align: center middle;
    }

    #log-container {
        width: 90%;
        height: 90%;
        background: $surface;
        border: thick $background;
        padding: 1;
    }
    """

    def __init__(self, log_widget: LoggingWidget):
        super().__init__()
        self.log_widget = log_widget

    def compose(self) -> ComposeResult:
        with Container(id="log-container"):
            yield self.log_widget

    def action_clear(self):
        """Clear log content."""
        self.log_widget.clear()
