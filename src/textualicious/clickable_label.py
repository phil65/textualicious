"""A label that can be clicked."""

from __future__ import annotations

from dataclasses import dataclass

from rich.text import Text
from textual.message import Message
from textual.widgets import Label


@dataclass
class SendToClipboard(Message):
    """Used to send a string to the clipboard."""

    message: str
    notify: bool = True


class ClickableLabel(Label):
    """A label that can be clicked."""

    @dataclass
    class Click(Message):
        """A message that is sent when the label is clicked."""

        label: ClickableLabel
        """The label that was clicked."""

        @property
        def control(self) -> ClickableLabel:
            """Return the label that was clicked."""
            return self.label

    @property
    def plain_text(self) -> str:
        """Return the plain text of the label."""
        match self.renderable:
            case str():
                return self.renderable
            case Text():
                return self.renderable.plain
            case _:
                msg = "Unknown renderable type"
                raise ValueError(msg)

    def on_click(self) -> None:
        """Called when the label is clicked."""
        self.post_message(self.Click(self))


class CopyToClipboardLabel(ClickableLabel):
    """A label that copies its text to the clipboard when clicked."""

    def __init__(self, text: str | Text, max_len: int = 0, **kwargs) -> None:
        """Initialize the label."""
        super().__init__(text, **kwargs)
        self.max_len = max_len
        self.tooltip = "Copy to clipboard"

    @property
    def sanitized_text(self) -> str:
        """Return the text to be copied to the clipboard."""
        txt = self.plain_text
        if self.max_len > 0:
            txt = txt[: self.max_len]
        return txt

    def on_click(self) -> None:
        """Called when the label is clicked to post message to clipboard."""
        super().on_click()
        self.post_message(SendToClipboard(self.sanitized_text))


if __name__ == "__main__":
    from textualicious import functional

    label = "test"
    functional.show(ClickableLabel(label))
