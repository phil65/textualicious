"""Textual widget for browsing local and remote filesystems using upath."""

from __future__ import annotations

from textual.widgets import DirectoryTree
from upath import UPath


class UniversalDirectoryTree(DirectoryTree):
    """DirectoryTree widget supporting local and remote filesystems via upath."""

    PATH = UPath
