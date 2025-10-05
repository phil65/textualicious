"""Widget for displaying icons from various icon fonts."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.widgets import Static


if TYPE_CHECKING:
    from textual.app import ComposeResult

ICON_MAP = {
    "fa.heart": ("\uf004", "Font Awesome 5 Free"),
    "fa.star": ("\uf005", "Font Awesome 5 Free"),
    "mdi.access-point": ("\uf0003", "Material Design Icons"),
    "ph.horse": ("\ue089", "Phosphor Icons"),
    "ri.aliens-fill": ("\uebca", "Remix Icon"),
    "msc.github": ("\uf09b", "GitHub Octicons"),
}


class Icon(Static):
    """A widget that displays an icon from a font."""

    DEFAULT_CSS = """
    Icon {
        width: auto;
        height: 1;
        content-align: center middle;
    }
    """

    def __init__(self, icon_name: str, *, font_size: int | None = None, **kwargs) -> None:
        """Initialize the icon widget.

        Args:
            icon_name: Name of the icon in format "prefix.name"
            font_size: Optional font size for the icon
            **kwargs: Additional arguments passed to the parent class
        """
        # Initialize with empty content - will be filled when mounted
        super().__init__("", **kwargs)
        self.icon_name = icon_name
        self.font_size = font_size

    async def on_mount(self) -> None:
        """Load and display the icon when the widget is mounted."""
        try:
            # Use a direct approach to work with font icons
            icon_char, font_family = await self._get_icon_info(self.icon_name)

            # Update the content with the icon character
            self.update(icon_char)

            # Set the font family and size
            self.styles.set_rule("font-family", font_family)
            if self.font_size is not None:
                self.styles.set_rule("font-size", f"{self.font_size}")
        except Exception as e:  # noqa: BLE001
            # If icon loading fails, show a fallback
            self.update("I")
            self.log.error(f"Failed to load icon {self.icon_name}: {e}")  # noqa: G004, TRY400

    async def _get_icon_info(self, icon_name: str) -> tuple[str, str]:
        """Get icon character and font family for the given icon name.

        This is a simplified version that returns hardcoded values for demo.
        In production, this would interact with a proper icon library.

        Args:
            icon_name: Icon name in format "prefix.name"

        Returns:
            Tuple of (icon character, font family name)
        """
        # Map of known icons to unicode characters and font families
        # Return the mapping or a default
        if icon_name in ICON_MAP:
            return ICON_MAP[icon_name]
        return ("I", "monospace")


def show_icons() -> None:
    """Show a demo of various icons."""
    from textual.app import App
    from textual.containers import Grid
    from textual.widgets import Footer, Header

    class IconDemo(App):
        """Demo app showing various icons."""

        CSS = """
        Grid {
            grid-size: 3;
            grid-gutter: 2;
            padding: 2;
        }

        Icon {
            width: 100%;
            height: 100%;
            border: solid green;
            background: #222222;
            color: #ffffff;
        }
        """

        def compose(self) -> ComposeResult:
            """Compose the app layout."""
            yield Header()
            with Grid():
                yield Icon("fa.heart", font_size=24)
                yield Icon("mdi.access-point", font_size=24)
                yield Icon("ph.horse", font_size=24)
                yield Icon("ri.aliens-fill", font_size=24)
                yield Icon("msc.github", font_size=24)
                yield Icon("fa.star", font_size=24)
            yield Footer()

    app = IconDemo()
    app.run()


if __name__ == "__main__":
    show_icons()
