from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from textual.message import Message
from textual.widgets import RichLog

from textualicious.log_widget.widget_handler import WidgetHandler


if TYPE_CHECKING:
    from rich.text import Text


class LoggingWidget(RichLog):
    """Widget that acts as both log display and handler."""

    class LogMessage(Message):
        """Internal message for log events."""

        def __init__(self, text: Text):
            self.text = text
            super().__init__()

    DEFAULT_CSS = """
    LoggingWidget {
        height: 1fr;
        border: heavy $background;
        padding: 1;
    }
    """

    def __init__(
        self,
        *,
        level: int = logging.DEBUG,
        format_string: str = "%(asctime)s - %(levelname)s - %(message)s",
        id: str | None = None,  # noqa: A002
    ):
        super().__init__(id=id, wrap=True, markup=True)
        self.formatter = logging.Formatter(format_string)
        handler = WidgetHandler(self)
        handler.setLevel(level)
        self.handler = handler

    def on_logging_widget_log_message(self, message: LogMessage) -> None:
        """Handle log message event."""
        self.write(message.text)
