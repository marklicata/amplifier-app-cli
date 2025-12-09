"""Input area widget for chat interface.

Phase 2: Enhanced Chat Interface
- Multi-line text input
- Submit on Enter, new line on Shift+Enter
- Clear input after submission
- Input hints and placeholder text
"""

from __future__ import annotations

from typing import Any

from textual.containers import Container
from textual.message import Message
from textual.widgets import TextArea


class InputSubmitted(Message):
    """Message sent when user submits input.
    
    Attributes:
        value: The submitted text
    """
    
    def __init__(self, value: str) -> None:
        """Initialize message.
        
        Args:
            value: The text that was submitted
        """
        super().__init__()
        self.value = value


class InputArea(Container):
    """Multi-line text input area for chat.
    
    Features:
    - Enter to submit (sends InputSubmitted message)
    - Shift+Enter for new line
    - Auto-clear after submission
    - Placeholder text
    - Focus management
    """
    
    DEFAULT_CSS = """
    InputArea {
        height: auto;
        dock: bottom;
        background: $panel;
        border-top: solid $primary;
        padding: 1;
    }
    
    InputArea TextArea {
        height: auto;
        min-height: 3;
        max-height: 10;
        background: $surface;
        border: solid $accent;
    }
    
    InputArea .input-hint {
        color: $text-muted;
        text-align: center;
        padding: 0 1;
    }
    """
    
    def __init__(
        self,
        placeholder: str = "Type your message...",
        show_hint: bool = True,
        **kwargs: Any,
    ):
        """Initialize input area.
        
        Args:
            placeholder: Placeholder text when empty
            show_hint: Whether to show keyboard hint
            **kwargs: Additional container kwargs
        """
        super().__init__(**kwargs)
        self.placeholder = placeholder
        self.show_hint = show_hint
    
    def compose(self):
        """Create child widgets."""
        textarea = TextArea(
            id="chat-input",
            language="markdown",
        )
        textarea.show_line_numbers = False
        
        yield textarea
        
        if self.show_hint:
            from textual.widgets import Static
            yield Static(
                "Enter: Send  •  Shift+Enter: New line  •  Ctrl+C: Cancel",
                classes="input-hint",
            )
    
    def on_mount(self) -> None:
        """Set up input area after mounting."""
        textarea = self.query_one("#chat-input", TextArea)
        
        # Focus the input
        textarea.focus()
    
    async def on_text_area_submitted(self, event: TextArea.Submitted) -> None:
        """Handle Enter key press (submit).
        
        Args:
            event: The submitted event from TextArea
        """
        textarea = self.query_one("#chat-input", TextArea)
        
        # Get the text
        text = textarea.text.strip()
        
        # Only submit if not empty
        if text:
            # Post InputSubmitted message
            self.post_message(InputSubmitted(text))
            
            # Clear the input
            textarea.clear()
            
            # Keep focus
            textarea.focus()
    
    def clear(self) -> None:
        """Clear the input area."""
        textarea = self.query_one("#chat-input", TextArea)
        textarea.clear()
    
    def get_text(self) -> str:
        """Get current input text.
        
        Returns:
            Current text in input area
        """
        textarea = self.query_one("#chat-input", TextArea)
        return textarea.text
    
    def set_text(self, text: str) -> None:
        """Set input text.
        
        Args:
            text: Text to set
        """
        textarea = self.query_one("#chat-input", TextArea)
        textarea.text = text
    
    def focus_input(self) -> None:
        """Focus the input area."""
        textarea = self.query_one("#chat-input", TextArea)
        textarea.focus()


__all__ = ["InputArea", "InputSubmitted"]
