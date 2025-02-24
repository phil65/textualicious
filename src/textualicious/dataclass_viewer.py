"""Widget for displaying dataclass-like objects in a table format."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rich.table import Table
from textual.widgets import Static


if TYPE_CHECKING:
    from rich.style import StyleType


class DataClassViewer(Static):
    """Display a dataclass-like object in a table format."""

    DEFAULT_CSS = """
    DataClassViewer {
        padding: 1;
    }
    """

    def __init__(
        self,
        obj: Any,
        *,
        show_types: bool = True,
        show_descriptions: bool = True,
        show_hidden: bool = False,
        field_style: StyleType | None = None,
        value_style: StyleType | None = None,
        type_style: StyleType = "dim",
        description_style: StyleType = "italic blue",
    ):
        """Initialize the model viewer.

        Args:
            obj: Any dataclass-like object to display
            show_types: Whether to show field types
            show_descriptions: Whether to show field descriptions
            show_hidden: Whether to show fields starting with underscore
            field_style: Style for field names
            value_style: Style for field values
            type_style: Style for type annotations
            description_style: Style for field descriptions
        """
        super().__init__("")
        self.obj = obj
        self.show_types = show_types
        self.show_descriptions = show_descriptions
        self.show_hidden = show_hidden
        self.field_style = field_style
        self.value_style = value_style
        self.type_style = type_style
        self.description_style = description_style
        self._update_content()

    def _update_content(self) -> None:
        """Update the displayed content."""
        from fieldz import fields

        table = Table(show_header=False, pad_edge=False, show_edge=True)

        # Add columns
        table.add_column("Field", style=self.field_style)
        table.add_column("Value", style=self.value_style)
        if self.show_types:
            table.add_column("Type", style=self.type_style)
        if self.show_descriptions:
            table.add_column("Description", style=self.description_style)

        try:
            obj_fields = fields(self.obj)
        except TypeError as e:
            msg = f"Unable to inspect fields of {type(self.obj)}"
            raise ValueError(msg) from e

        # Add rows for each field
        for field in obj_fields:
            if field.name.startswith("_") and not self.show_hidden:
                continue

            value = getattr(self.obj, field.name)
            row: list[Any] = [field.name, str(value)]

            if self.show_types:
                type_name = field.type if field.type else "N/A"
                row.append(type_name)

            if self.show_descriptions:
                description = field.description or ""
                row.append(description)

            table.add_row(*row)

        self.update(table)


if __name__ == "__main__":
    from dataclasses import dataclass

    from textualicious import functional

    @dataclass
    class Test:
        a: int
        b: str

    functional.show(DataClassViewer(Test(1, "test")))
