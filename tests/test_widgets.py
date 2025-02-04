"""Tests for the DataClassTable widget."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pytest
from textual.app import App, ComposeResult

from textualicious.dataclass_table import DataClassTable
from textualicious.dataclass_viewer import DataClassViewer
from textualicious.log_widget import LoggingWidget


if TYPE_CHECKING:
    from .conftest import SampleData


class TableTestApp(App[None]):
    """Test application for DataClassTable testing."""

    def __init__(
        self,
        item_type: type,
        *args,
        **kwargs,
    ) -> None:
        self.item_type = item_type
        super().__init__(*args, **kwargs)
        self.table: DataClassTable | None = None

    def compose(self) -> ComposeResult:
        self.table = DataClassTable(self.item_type)
        yield self.table


@pytest.mark.asyncio
async def test_dataclass_table_initialization(sample_data: SampleData) -> None:
    """Test basic initialization of DataClassTable."""
    app = TableTestApp(type(sample_data))
    async with app.run_test():
        table = app.table
        assert table is not None
        assert table._item_type is type(sample_data)


@pytest.mark.asyncio
async def test_dataclass_table_add_item(sample_data: SampleData) -> None:
    """Test adding an item to the table."""
    app = TableTestApp(type(sample_data))
    async with app.run_test():
        table = app.table
        assert table is not None

        table.add_item(sample_data)
        assert len(table._items) == 1

        first_row_key = next(iter(table._items))
        assert table.get_item(first_row_key) == sample_data


@pytest.mark.asyncio
async def test_dataclass_table_clear_items(sample_data: SampleData) -> None:
    """Test clearing items from the table."""
    app = TableTestApp(type(sample_data))
    async with app.run_test():
        table = app.table
        assert table is not None

        table.add_item(sample_data)
        assert len(table._items) > 0

        table.clear_items()
        assert len(table._items) == 0


@pytest.mark.asyncio
async def test_dataclass_table_invalid_item(sample_data: SampleData) -> None:
    """Test adding invalid item type."""
    app = TableTestApp(type(sample_data))
    async with app.run_test():
        table = app.table
        assert table is not None

        with pytest.raises(TypeError):
            table.add_item("invalid item")  # type: ignore


def test_model_viewer_initialization(sample_data: SampleData) -> None:
    """Test basic initialization of DataClassViewer."""
    viewer = DataClassViewer(sample_data)
    assert viewer is not None
    assert viewer.obj == sample_data


def test_model_viewer_show_options(sample_data: SampleData) -> None:
    """Test different display options."""
    viewer = DataClassViewer(
        sample_data,
        show_types=False,
        show_descriptions=False,
        show_hidden=True,
    )
    assert not viewer.show_types
    assert not viewer.show_descriptions
    assert viewer.show_hidden


def test_model_viewer_invalid_object() -> None:
    """Test initialization with invalid object."""
    with pytest.raises(ValueError):  # noqa: PT011
        DataClassViewer("not a dataclass")  # type: ignore


def test_log_widget_initialization() -> None:
    """Test basic initialization of LoggingWidget."""
    widget = LoggingWidget()
    assert widget is not None
    assert isinstance(widget.handler, logging.Handler)


def test_log_widget_custom_level() -> None:
    """Test setting custom log level."""
    widget = LoggingWidget(level=logging.WARNING)
    assert widget.handler.level == logging.WARNING


def test_log_widget_custom_format() -> None:
    """Test setting custom format string."""
    format_string = "%(levelname)s: %(message)s"
    widget = LoggingWidget(format_string=format_string)
    assert widget.formatter._fmt == format_string  # type: ignore
