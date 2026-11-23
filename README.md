# Textualicious

> [!WARNING]
> **This project is archived and no longer maintained.** Its widgets were experiments;
> the parts that proved useful live on in [acptui](https://github.com/phil65/acptui)
> (a file tree over any [upathtools](https://github.com/phil65/upathtools) filesystem,
> text screenshots, help and log screens). The last release (1.0.1) stays on PyPI.

[![PyPI License](https://img.shields.io/pypi/l/textualicious.svg)](https://pypi.org/project/textualicious/)
[![Package status](https://img.shields.io/pypi/status/textualicious.svg)](https://pypi.org/project/textualicious/)
[![Monthly downloads](https://img.shields.io/pypi/dm/textualicious.svg)](https://pypi.org/project/textualicious/)
[![Distribution format](https://img.shields.io/pypi/format/textualicious.svg)](https://pypi.org/project/textualicious/)
[![Wheel availability](https://img.shields.io/pypi/wheel/textualicious.svg)](https://pypi.org/project/textualicious/)
[![Python version](https://img.shields.io/pypi/pyversions/textualicious.svg)](https://pypi.org/project/textualicious/)
[![Implementation](https://img.shields.io/pypi/implementation/textualicious.svg)](https://pypi.org/project/textualicious/)
[![Releases](https://img.shields.io/github/downloads/phil65/textualicious/total.svg)](https://github.com/phil65/textualicious/releases)
[![Github Contributors](https://img.shields.io/github/contributors/phil65/textualicious)](https://github.com/phil65/textualicious/graphs/contributors)
[![Github Forks](https://img.shields.io/github/forks/phil65/textualicious)](https://github.com/phil65/textualicious/forks)
[![Github Issues](https://img.shields.io/github/issues/phil65/textualicious)](https://github.com/phil65/textualicious/issues)
[![Github Issues](https://img.shields.io/github/issues-pr/phil65/textualicious)](https://github.com/phil65/textualicious/pulls)
[![Github Watchers](https://img.shields.io/github/watchers/phil65/textualicious)](https://github.com/phil65/textualicious/watchers)
[![Github Stars](https://img.shields.io/github/stars/phil65/textualicious)](https://github.com/phil65/textualicious/stars)
[![Github Repository size](https://img.shields.io/github/repo-size/phil65/textualicious)](https://github.com/phil65/textualicious)
[![Github last commit](https://img.shields.io/github/last-commit/phil65/textualicious)](https://github.com/phil65/textualicious/commits)
[![Github release date](https://img.shields.io/github/release-date/phil65/textualicious)](https://github.com/phil65/textualicious/releases)
[![Github language count](https://img.shields.io/github/languages/count/phil65/textualicious)](https://github.com/phil65/textualicious)
[![Github commits this month](https://img.shields.io/github/commit-activity/m/phil65/textualicious)](https://github.com/phil65/textualicious)
[![Package status](https://codecov.io/gh/phil65/textualicious/branch/main/graph/badge.svg)](https://codecov.io/gh/phil65/textualicious/)
[![PyUp](https://pyup.io/repos/github/phil65/textualicious/shield.svg)](https://pyup.io/repos/github/phil65/textualicious/)

[Read the documentation!](https://phil65.github.io/textualicious/)

Reusable widgets and screens for [Textual](https://textual.textualize.io/) apps:
tables and viewers for dataclass-like objects, a logging widget, modal help/log screens
and a directory tree for local and remote filesystems.

## Installation

```bash
pip install textualicious
```

Requires Python 3.13+.

## Quickstart

```python
from dataclasses import dataclass
import logging

from textual.app import App, ComposeResult

from textualicious import DataClassTable, DataClassViewer, LoggingWidget


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


TASKS = [Task(1, "Write docs"), Task(2, "Fix bugs", done=True)]


class TaskApp(App):
    def compose(self) -> ComposeResult:
        yield DataClassTable(Task, items=TASKS, cursor_type="row")
        yield DataClassViewer(TASKS[0])
        yield LoggingWidget()

    def on_mount(self) -> None:
        # The widget doubles as a logging handler
        logging.getLogger().addHandler(self.query_one(LoggingWidget).handler)

    def on_data_class_table_row_selected(self, event: DataClassTable.RowSelected) -> None:
        logging.getLogger().warning("Selected %s", event.item)


if __name__ == "__main__":
    TaskApp().run()
```

To try a single widget or screen without writing an app, use `show`:

```python
from textualicious import HelpScreen, show, show_path

show(HelpScreen("# Help\n\nPress `esc` to close."))
show_path(".")  # browse a directory (any universal-pathlib / fsspec URL works)
```

## Features

- **`DataClassTable`**: a `DataTable` for lists of dataclass-like objects (anything
  [fieldz](https://github.com/pyapp-kit/fieldz) understands: dataclasses, pydantic, attrs, ...).
  Columns come from the fields; posts `DataClassTable.RowSelected` with the selected item.
- **`DataClassViewer`**: shows one object as a field / value / type / description table.
- **`LoggingWidget`**: a `RichLog` with an attached `logging.Handler` (`widget.handler`),
  colored by log level. `textualicious.log_screen.LogWindow` wraps it in a modal screen.
- **`HelpScreen`**: a modal screen rendering Markdown help text.
- **`UniversalDirectoryTree`** (`textualicious.upath_tree`): a `DirectoryTree` backed by
  [universal-pathlib](https://github.com/fsspec/universal_pathlib), so it can browse remote
  filesystems (S3, GitHub, ...; install the matching fsspec backend).
- **`show` / `show_path`**: run a widget or screen in a minimal app for quick previews.
