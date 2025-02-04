from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from rich.text import Text


if TYPE_CHECKING:
    from textualicious.log_widget import LoggingWidget


class WidgetHandler(logging.Handler):
    def __init__(self, widget: LoggingWidget):
        super().__init__()
        self.widget = widget

    def emit(self, record: logging.LogRecord) -> None:
        from textualicious.log_widget import LoggingWidget

        try:
            assert self.widget.formatter
            msg = self.widget.formatter.format(record)
            style = {
                logging.DEBUG: "dim",
                logging.INFO: "white",
                logging.WARNING: "yellow",
                logging.ERROR: "red",
                logging.CRITICAL: "red bold",
            }.get(record.levelno, "white")

            text = Text(msg + "\n", style=style)
            self.widget.post_message(LoggingWidget.LogMessage(text))
        except Exception:  # noqa: BLE001
            self.handleError(record)
