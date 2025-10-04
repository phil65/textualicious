"""Textual widget for browsing local and remote filesystems using upath."""

from __future__ import annotations

from textual.widgets import DirectoryTree
from upath import UPath


class UniversalDirectoryTree(DirectoryTree):
    """DirectoryTree widget supporting local and remote filesystems via upath."""

    PATH = UPath  # type: ignore

    def __init__(
        self,
        path: str | UPath,
        *,
        name: str | None = None,
        id: str | None = None,  # noqa: A002
        classes: str | None = None,
        disabled: bool = False,
    ):
        super().__init__(
            path,  # type: ignore
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )


if __name__ == "__main__":
    from textualicious import functional

    path = UPath("github://", org="phil65", repo="mknodes")
    functional.show(UniversalDirectoryTree(path))
