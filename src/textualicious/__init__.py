from __future__ import annotations

from importlib.metadata import version

__version__ = version("textualicious")

from textualicious.dataclass_table import DataClassTable
from textualicious.dataclass_viewer import DataClassViewer
from textualicious.log_widget import LoggingWidget
from textualicious.help_screen import HelpScreen
from textualicious.functional import show, show_path

__all__ = [
    "__version__",
    "DataClassTable",
    "DataClassViewer",
    "HelpScreen",
    "LoggingWidget",
    "show",
    "show_path",
]