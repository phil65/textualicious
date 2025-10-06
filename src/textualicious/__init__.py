"""Textualicious: main package.

Textual widgets and integrations.
"""

from __future__ import annotations

from importlib.metadata import version

__version__ = version("textualicious")
__title__ = "Textualicious"

__author__ = "Philipp Temminghoff"
__author_email__ = "philipptemminghoff@googlemail.com"
__copyright__ = "Copyright (c) 2025 Philipp Temminghoff"
__license__ = "MIT"
__url__ = "https://github.com/phil65/textualicious"

from textualicious.dataclass_table import DataClassTable
from textualicious.dataclass_viewer import DataClassViewer
from textualicious.log_widget import LoggingWidget
from textualicious.help_screen import HelpScreen
from textualicious.functional import show, show_path

__all__ = [
    "DataClassTable",
    "DataClassViewer",
    "HelpScreen",
    "LoggingWidget",
    "__version__",
    "show",
    "show_path",
]
