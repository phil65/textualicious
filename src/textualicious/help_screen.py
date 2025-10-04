"""Help screen. Credits to Elia (https://github.com/darrenburns/elia)."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Footer, Markdown


if TYPE_CHECKING:
    from textual.app import ComposeResult


class HelpScreen(ModalScreen[None]):
    BINDINGS: ClassVar = [
        Binding("q", "app.quit", "Quit", show=False),
        Binding("escape,f1,?", "app.pop_screen()", "Close help", key_display="esc"),
    ]

    def __init__(self, markdown: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.help_text = markdown

    def compose(self) -> ComposeResult:
        with Vertical(id="help-container") as vertical:
            vertical.border_title = "Help"
            with VerticalScroll():
                yield Markdown(self.help_text, id="help-markdown")
            yield Markdown(
                "Use `pageup`, `pagedown`, `up`, and `down` to scroll.",
                id="help-scroll-keys-info",
            )
        yield Footer()


if __name__ == "__main__":
    from textualicious import functional

    functional.show(HelpScreen("This is a test"))
