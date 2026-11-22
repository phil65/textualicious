# AGENTS.md

## Overview

`textualicious` is a small library of reusable [Textual](https://textual.textualize.io/)
widgets and screens: tables/viewers for dataclass-like objects (via `fieldz`), a logging
widget that doubles as a `logging.Handler`, a help screen, a directory tree for local and
remote filesystems (via `universal-pathlib`), and helpers to show a widget in a throwaway app.

## Architecture

All code lives in `src/textualicious/` (uv_build backend, `py.typed` ships).

- `__init__.py`: public API (`DataClassTable`, `DataClassViewer`, `HelpScreen`,
  `LoggingWidget`, `show`, `show_path`). Everything else is imported from its submodule.
- `dataclass_table.py`: `DataClassTable[T]` (a `DataTable`). Columns come from
  `fieldz.fields(item_type)`; underscore fields are hidden unless `show_hidden=True`.
  Keeps a `RowKey -> item` map and posts its own `DataClassTable.RowSelected(item)` when
  Textual's `DataTable.RowSelected` arrives (intentional shadowing of the parent class name).
- `dataclass_viewer.py`: `DataClassViewer` (a `Static`) renders one object as a Rich
  `Table` (field / value / type / description). Raises `ValueError` for non-dataclass-like input.
- `log_widget/`: `LoggingWidget` (a `RichLog`) owns a `WidgetHandler` (`widget.handler`).
  The handler formats records with `widget.formatter` and posts a `LoggingWidget.LogMessage`,
  so logging is thread-safe via Textual's message queue. Attach with
  `logging.getLogger().addHandler(widget.handler)`.
- `log_screen.py`: `LogWindow`, a `ModalScreen` wrapping a `LoggingWidget` (`c` clears).
- `help_screen.py`: `HelpScreen(markdown)`, a modal Markdown help screen.
- `upath_tree.py`: `UniversalDirectoryTree`, a `DirectoryTree` with `PATH = UPath`.
- `icon_widget.py`: `Icon` widget with a small hard-coded `ICON_MAP` (demo quality).
- `utils.py`: `capture_screen_ascii(screen)` (uses private `screen._compositor`) plus a demo app.
- `functional.py`: `show(widget_or_screen)` runs a minimal app; `show_path(path)` shows a
  `UniversalDirectoryTree`. Imports are lazy.
- `log.py`: `get_logger(name)` returns `textualicious.<name>` loggers.

Most modules have an `if __name__ == "__main__":` demo using `functional.show`.

## Where to look

| Task | Location |
| --- | --- |
| Public exports | `src/textualicious/__init__.py` |
| Dataclass table / row selection | `src/textualicious/dataclass_table.py` |
| Single-object view | `src/textualicious/dataclass_viewer.py` |
| Log display / handler | `src/textualicious/log_widget/` |
| Modal screens | `src/textualicious/help_screen.py`, `src/textualicious/log_screen.py` |
| Remote filesystem tree | `src/textualicious/upath_tree.py` |
| Demo runner | `src/textualicious/functional.py` |
| Tests and fixtures | `tests/test_widgets.py`, `tests/conftest.py` |
| CI | `.github/workflows/build.yml`, `.github/workflows/documentation.yml` |
| Task shortcuts | `duties.py` |

## Commands

```bash
uv sync --all-extras                 # setup (default groups: dev, lint, docs)
uv run pytest                        # tests (pytest-asyncio, asyncio_mode = "auto")
uvx ruff check . && uvx ruff format --check .
uv run ty check                      # type check (src/ only); warnings fail CI
uv run deptry src                    # dependency hygiene
uv run mkdocs-mknodes build          # docs (output in site/)
uv build
uvx duty lint                        # duties.py tasks: build, serve, test, clean, update, lint, lint_check, version
```

## Conventions

- Python >= 3.13, PEP 695 generics (`class DataClassTable[T]`),
  `from __future__ import annotations`, type-only imports under `TYPE_CHECKING`.
- Ruff line length 100, Google-style docstrings, preview formatting.
- Tests: async tests use `App.run_test()` (headless pilot) with a small host `App`; plain
  widget construction tests run without an app. Test-only deps go in the `dev` group.
- Type checker is ty; use targeted `# ty: ignore[rule]` only (mypy-style `# type: ignore[...]`
  codes do not apply).

## Pitfalls

- Copier-managed project (`.copier-answers.yml`, template `phil65/copier-phil65`): workflows,
  `duties.py`, `.pre-commit-config.yaml`, `mkdocs.yml` and most of `pyproject.toml` come from
  the template. Add dependencies only below the `# Only add below (Copier)` markers.
- Runtime deps: `textual`, `rich`, `fieldz`, `universal-pathlib`. Remote protocols for
  `UniversalDirectoryTree` (e.g. `github://`) need the matching fsspec backend installed.
- Docs use the mkdocs-mknodes default site: README is the index page, API pages are generated;
  `docs/` is intentionally empty. Avoid imports in package `__main__` blocks that could create
  cyclic aliases for griffe.
- `uv.lock` is gitignored.
- Pre-commit hooks run ruff, tombi, ty and the full test suite on every commit.
