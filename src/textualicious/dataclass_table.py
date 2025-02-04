"""Generic data table implementations for dataclass-like objects."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fieldz import fields
from textual.message import Message
from textual.widgets import DataTable


if TYPE_CHECKING:
    from textual.widgets._data_table import CursorType, RowKey


class DataClassTable[T](DataTable):
    """A DataTable that displays a list of dataclass-like objects."""

    class RowSelected(Message):
        """Emitted when a row is selected."""

        def __init__(self, item: Any) -> None:
            self.item = item
            super().__init__()

    def __init__(
        self,
        item_type: type[T],
        *,
        show_hidden: bool = False,
        show_header: bool = True,
        show_row_labels: bool = True,
        fixed_rows: int = 0,
        fixed_columns: int = 0,
        zebra_stripes: bool = False,
        header_height: int = 1,
        show_cursor: bool = True,
        cursor_type: CursorType = "cell",
        cell_padding: int = 1,
        name: str | None = None,
        id: str | None = None,  # noqa: A002
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Initialize the table.

        Args:
            item_type: The type of items to display
            show_hidden: Whether to show fields starting with underscore
            show_header: Whether the table header should be visible
            show_row_labels: Whether the row labels should be shown
            fixed_rows: Number of rows to fix at the top
            fixed_columns: Number of columns to fix at the left
            zebra_stripes: Enable alternating row colors
            header_height: Height of the header row
            show_cursor: Whether to show the cursor
            cursor_type: Type of cursor ("cell", "row", "column", or "none")
            cell_padding: Padding between cells
            name: The name of the widget
            id: The ID of the widget
            classes: CSS classes
            disabled: Whether the widget is disabled
        """
        super().__init__(
            show_header=show_header,
            show_row_labels=show_row_labels,
            fixed_rows=fixed_rows,
            fixed_columns=fixed_columns,
            zebra_stripes=zebra_stripes,
            header_height=header_height,
            show_cursor=show_cursor,
            cursor_type=cursor_type,
            cell_padding=cell_padding,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self._item_type = item_type
        self._show_hidden = show_hidden
        self._items: dict[RowKey, T] = {}
        self._setup_columns()

    def _setup_columns(self) -> None:
        """Set up columns based on the item type's fields."""
        try:
            obj_fields = fields(self._item_type)
        except TypeError as e:
            msg = f"Unable to inspect fields of {self._item_type}"
            raise ValueError(msg) from e

        for field in obj_fields:
            if field.name.startswith("_") and not self._show_hidden:
                continue

            header = field.name
            self.add_column(header, key=field.name)

    def add_item(self, item: T) -> None:
        """Add an item to the table.

        Args:
            item: Instance of the item type
        """
        if not isinstance(item, self._item_type):
            msg = f"Expected {self._item_type.__name__}, got {type(item).__name__}"
            raise TypeError(msg)

        try:
            obj_fields = fields(item)
        except TypeError as e:
            msg = f"Unable to inspect fields of {item}"
            raise ValueError(msg) from e

        row_values = []
        for field in obj_fields:
            if field.name.startswith("_") and not self._show_hidden:
                continue
            row_values.append(getattr(item, field.name))

        row_key = self.add_row(*row_values)
        self._items[row_key] = item

    def clear_items(self) -> None:
        """Remove all items from the table."""
        self.clear()
        self._items.clear()

    def get_item(self, row: RowKey) -> T | None:
        """Get the item at the specified row."""
        return self._items.get(row)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection."""
        if item := self.get_item(event.row_key):
            self.post_message(self.RowSelected(item))


if __name__ == "__main__":
    from dataclasses import dataclass
    from datetime import datetime

    from textual.app import App

    @dataclass
    class TaskItem:
        """Example task item for demonstration."""

        id: int
        title: str
        due_date: datetime
        completed: bool

    class DemoApp(App):
        """Demo application showing DataClassTable usage."""

        def compose(self):
            table = DataClassTable(TaskItem, cursor_type="row")
            # Add some sample data
            table.add_item(
                TaskItem(1, "Write documentation", datetime(2024, 1, 15), False)
            )
            table.add_item(TaskItem(2, "Fix bugs", datetime(2024, 1, 16), True))
            table.add_item(TaskItem(3, "Release version", datetime(2024, 1, 17), False))
            yield table

    app = DemoApp()
    app.run()
