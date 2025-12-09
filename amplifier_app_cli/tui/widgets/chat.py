"""Chat widgets for Amplifier TUI.

Phase 2: Enhanced Chat Interface
- Message bubbles for user and assistant
- Scrollable chat display
- Streaming message support
- Rich markdown rendering
"""

from __future__ import annotations

from typing import Any

from rich.console import RenderableType
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import Static


class MessageBubble(Static):
    """A single message bubble in the chat.
    
    Displays user or assistant messages with appropriate styling.
    Supports streaming (message content updates as it arrives).
    """
    
    DEFAULT_CSS = """
    MessageBubble {
        height: auto;
        margin: 1 0;
        padding: 1 2;
    }
    
    MessageBubble.user {
        background: $primary-darken-1;
        border: tall $primary;
    }
    
    MessageBubble.assistant {
        background: $panel;
        border: tall $accent;
    }
    
    MessageBubble.system {
        background: $surface;
        border: tall $warning;
    }
    
    MessageBubble.streaming {
        border: tall $success;
    }
    """
    
    content = reactive("")
    role = reactive("assistant")
    streaming = reactive(False)
    
    def __init__(
        self,
        content: str = "",
        role: str = "assistant",
        streaming: bool = False,
        show_avatar: bool = True,
        **kwargs: Any,
    ):
        """Initialize message bubble.
        
        Args:
            content: Message text content
            role: Message role ('user', 'assistant', 'system')
            streaming: Whether message is currently streaming
            show_avatar: Whether to show role avatar/icon
            **kwargs: Additional widget kwargs
        """
        super().__init__(**kwargs)
        self.content = content
        self.role = role
        self.streaming = streaming
        self.show_avatar = show_avatar
        
        # Add role class for styling
        self.add_class(role)
        if streaming:
            self.add_class("streaming")
    
    def watch_streaming(self, streaming: bool) -> None:
        """Update classes when streaming status changes."""
        if streaming:
            self.add_class("streaming")
        else:
            self.remove_class("streaming")
    
    def watch_content(self, content: str) -> None:
        """Refresh display when content changes."""
        self.refresh()
    
    def append_content(self, chunk: str) -> None:
        """Append a chunk to the message content.
        
        Used for streaming messages.
        
        Args:
            chunk: Text chunk to append
        """
        self.content += chunk
    
    def finalize_streaming(self) -> None:
        """Mark message as complete (no longer streaming)."""
        self.streaming = False
    
    def render(self) -> RenderableType:
        """Render the message bubble."""
        # Avatar/role indicator
        avatar_map = {
            "user": "👤",
            "assistant": "🤖",
            "system": "⚙️",
        }
        avatar = avatar_map.get(self.role, "")
        
        # Role label
        role_map = {
            "user": "You",
            "assistant": "Amplifier",
            "system": "System",
        }
        role_label = role_map.get(self.role, self.role.capitalize())
        
        # Build header
        header = Text()
        if self.show_avatar:
            header.append(f"{avatar} ", style="bold")
        header.append(role_label, style="bold green" if self.role == "user" else "bold cyan")
        
        if self.streaming:
            header.append(" ", style="dim")
            header.append("▸", style="bold green blink")  # Streaming indicator
        
        # Render content
        if self.role == "user":
            # User messages: simple text
            content_renderable = Text(self.content)
        else:
            # Assistant messages: markdown
            try:
                content_renderable = Markdown(self.content)
            except Exception:
                # Fallback to plain text if markdown fails
                content_renderable = Text(self.content)
        
        # Combine header and content
        return Panel(
            content_renderable,
            title=header,
            title_align="left",
            border_style="dim",
        )


class ChatWidget(Static):
    """Scrollable chat message display.
    
    Manages a list of message bubbles and provides methods to add
    new messages or stream content to existing messages.
    """
    
    DEFAULT_CSS = """
    ChatWidget {
        height: 1fr;
        border: solid $primary;
        background: $surface;
    }
    
    ChatWidget > VerticalScroll {
        height: 1fr;
        padding: 1;
    }
    """
    
    def __init__(self, **kwargs: Any):
        """Initialize chat widget."""
        super().__init__(**kwargs)
        self.messages: list[MessageBubble] = []
        self._streaming_message: MessageBubble | None = None
    
    def compose(self):
        """Create child widgets."""
        yield VerticalScroll(id="message-container")
    
    def add_message(
        self,
        content: str,
        role: str = "assistant",
        show_avatar: bool = True,
    ) -> MessageBubble:
        """Add a complete message to the chat.
        
        Args:
            content: Message text
            role: Message role ('user', 'assistant', 'system')
            show_avatar: Whether to show role avatar
            
        Returns:
            The created MessageBubble
        """
        bubble = MessageBubble(
            content=content,
            role=role,
            streaming=False,
            show_avatar=show_avatar,
        )
        
        self.messages.append(bubble)
        
        container = self.query_one("#message-container", VerticalScroll)
        container.mount(bubble)
        
        # Auto-scroll to bottom
        self.call_after_refresh(self._scroll_to_bottom)
        
        return bubble
    
    def start_streaming_message(
        self,
        role: str = "assistant",
        show_avatar: bool = True,
    ) -> MessageBubble:
        """Start a new streaming message.
        
        Args:
            role: Message role
            show_avatar: Whether to show role avatar
            
        Returns:
            The streaming MessageBubble
        """
        bubble = MessageBubble(
            content="",
            role=role,
            streaming=True,
            show_avatar=show_avatar,
        )
        
        self.messages.append(bubble)
        self._streaming_message = bubble
        
        container = self.query_one("#message-container", VerticalScroll)
        container.mount(bubble)
        
        # Auto-scroll to bottom
        self.call_after_refresh(self._scroll_to_bottom)
        
        return bubble
    
    def append_to_streaming(self, chunk: str) -> None:
        """Append content to the current streaming message.
        
        Args:
            chunk: Text chunk to append
        """
        if self._streaming_message:
            self._streaming_message.append_content(chunk)
            # Auto-scroll to bottom
            self.call_after_refresh(self._scroll_to_bottom)
    
    def finalize_streaming(self) -> None:
        """Mark the current streaming message as complete."""
        if self._streaming_message:
            self._streaming_message.finalize_streaming()
            self._streaming_message = None
    
    def clear_messages(self) -> None:
        """Clear all messages from the chat."""
        container = self.query_one("#message-container", VerticalScroll)
        
        # Remove all message bubbles
        for message in self.messages:
            message.remove()
        
        self.messages.clear()
        self._streaming_message = None
    
    def _scroll_to_bottom(self) -> None:
        """Scroll chat to show the latest message."""
        container = self.query_one("#message-container", VerticalScroll)
        # Scroll to the end
        container.scroll_end(animate=False)


__all__ = ["MessageBubble", "ChatWidget"]
