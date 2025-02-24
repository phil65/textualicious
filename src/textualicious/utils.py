"""Utilities for capturing Textual screen content as ASCII art."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from rich.console import Console
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.widgets import Button, Footer, Header, Input, Static


if TYPE_CHECKING:
    from textual.screen import Screen


def capture_screen_ascii(screen: Screen) -> str:
    """Capture the screen content as plain ASCII representation."""
    # Create a console for plain text output
    console = Console(
        force_terminal=False,
        color_system=None,
        legacy_windows=True,
        width=screen.size.width,
        height=screen.size.height,
    )

    # Get the screen content as strips
    strips = screen._compositor.render_strips()

    # Convert strips to plain text, line by line
    with console.capture() as capture:
        for strip in strips:
            # Convert segments to text
            text = "".join(segment.text for segment in strip)
            console.print(text)

    return capture.get()


class CaptureViewer(Static):
    """Widget to display the screen capture."""

    DEFAULT_CSS = """
    CaptureViewer {
        width: 100%;
        height: auto;
        border: solid green;
        padding: 1;
        overflow: auto;
        min-height: 20;
    }
    """


class DemoApp(App):
    """Demo application showing screen capture functionality."""

    BINDINGS: ClassVar = [Binding("c", "capture", "Capture Screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            # Left side - interactive elements
            with Container():
                yield Button("Click me!")
                yield Input(placeholder="Type something...")
            # Right side - capture viewer
            yield CaptureViewer("Capture will appear here\nPress 'c' to capture")
        yield Footer()

    def action_capture(self) -> None:
        """Capture the screen when 'c' is pressed."""
        result = capture_screen_ascii(self.screen)
        # Write to file with UTF-8 encoding
        Path("screen_capture.txt").write_text(result, encoding="utf-8")
        self.notify("Capture saved to screen_capture.txt")


if __name__ == "__main__":
    app = DemoApp()
    app.run()
