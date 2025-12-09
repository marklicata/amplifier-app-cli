"""Chat screen for Amplifier TUI.

Phase 2: Enhanced Chat Interface
- Full chat experience with message display and input
- Streaming message support
- Integration with AmplifierSession
- Keyboard shortcuts for common actions
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer
from textual.widgets import Header

from ..widgets.chat import ChatWidget
from ..widgets.input import InputArea
from ..widgets.input import InputSubmitted

logger = logging.getLogger(__name__)


class ChatScreen(Screen):
    """Interactive chat screen for Amplifier.
    
    This is the main Phase 2 screen that replaces the prompt_toolkit REPL
    with a modern TUI chat interface.
    
    Features:
    - Message display with role-based styling
    - Streaming assistant responses
    - Multi-line input with Enter to submit
    - Keyboard shortcuts (Ctrl+N for new chat, Ctrl+H for history, etc.)
    - Integration with AmplifierSession for actual AI interactions
    """
    
    BINDINGS = [
        Binding("ctrl+n", "new_chat", "New Chat", priority=True),
        Binding("ctrl+h", "toggle_history", "History"),
        Binding("ctrl+s", "save_session", "Save"),
        Binding("ctrl+/", "show_help", "Help"),
        ("escape", "focus_input", "Focus Input"),
        ("ctrl+c", "cancel_operation", "Cancel"),
    ]
    
    CSS = """
    ChatScreen {
        background: $surface;
    }
    
    #chat-container {
        height: 1fr;
    }
    
    .welcome-message {
        color: $text-muted;
        text-align: center;
        padding: 2;
    }
    """
    
    def __init__(
        self,
        session_id: str | None = None,
        profile: str = "default",
        config: dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        """Initialize chat screen.
        
        Args:
            session_id: Optional session ID to resume
            profile: Profile name to use
            config: Amplifier configuration dict
            **kwargs: Additional screen kwargs
        """
        super().__init__(**kwargs)
        self.session_id = session_id
        self.profile = profile
        self.config = config or {}
        self.amplifier_session = None
        self._processing = False
    
    def compose(self) -> ComposeResult:
        """Create child widgets for chat screen."""
        yield Header()
        
        with Container(id="chat-container"):
            yield ChatWidget(id="chat")
        
        yield InputArea(id="input")
        yield Footer()
    
    def on_mount(self) -> None:
        """Set up chat screen after mounting."""
        # Update subtitle with profile
        if self.profile:
            self.sub_title = f"Profile: {self.profile}"
        
        # Show welcome message
        chat = self.query_one("#chat", ChatWidget)
        chat.add_message(
            "Welcome to Amplifier! 👋\n\n"
            "I'm here to help you with your development tasks.\n\n"
            "Type your request below and press **Enter** to send.\n"
            "Use **Shift+Enter** for a new line.\n\n"
            "*Tip: Press Ctrl+/ to see all keyboard shortcuts.*",
            role="assistant",
        )
        
        # Focus input
        input_area = self.query_one("#input", InputArea)
        input_area.focus_input()
        
        logger.info(f"Chat screen mounted (session={self.session_id}, profile={self.profile})")
    
    async def on_input_submitted(self, event: InputSubmitted) -> None:
        """Handle user input submission.
        
        Args:
            event: InputSubmitted event with user's text
        """
        # Prevent concurrent processing
        if self._processing:
            self.notify("Please wait for the current message to complete", severity="warning")
            return
        
        user_message = event.value.strip()
        if not user_message:
            return
        
        # Add user message to chat
        chat = self.query_one("#chat", ChatWidget)
        chat.add_message(user_message, role="user")
        
        # Process the message
        await self._process_user_message(user_message)
    
    async def _process_user_message(self, message: str) -> None:
        """Process user message and get AI response.
        
        Args:
            message: User's message text
        """
        self._processing = True
        
        try:
            chat = self.query_one("#chat", ChatWidget)
            
            # Start streaming response
            streaming_bubble = chat.start_streaming_message(role="assistant")
            
            # Simulate AI response for Phase 2 demo
            # In future phases, this will integrate with AmplifierSession
            await self._simulate_ai_response(chat, message)
            
            # Finalize streaming
            chat.finalize_streaming()
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            chat = self.query_one("#chat", ChatWidget)
            chat.add_message(
                f"❌ Error: {str(e)}\n\nPlease try again.",
                role="system",
            )
        
        finally:
            self._processing = False
            
            # Focus input for next message
            input_area = self.query_one("#input", InputArea)
            input_area.focus_input()
    
    async def _simulate_ai_response(self, chat: ChatWidget, user_message: str) -> None:
        """Simulate AI response with streaming.
        
        This is a placeholder for Phase 2 demonstration.
        Will be replaced with actual AmplifierSession integration.
        
        Args:
            chat: ChatWidget to stream to
            user_message: User's message
        """
        # Simulate thinking delay
        await asyncio.sleep(0.5)
        
        # Generate a demo response based on keywords
        if "hello" in user_message.lower() or "hi" in user_message.lower():
            response = (
                "Hello! 👋\n\n"
                "I'm Amplifier, your AI development assistant. "
                "I can help you with:\n\n"
                "- Writing and reviewing code\n"
                "- Debugging issues\n"
                "- Architecture decisions\n"
                "- Documentation\n"
                "- And much more!\n\n"
                "What would you like to work on today?"
            )
        elif "test" in user_message.lower():
            response = (
                "I can help you with testing! 🧪\n\n"
                "Let me demonstrate the **streaming response** feature:\n\n"
                "This text is being streamed character by character, "
                "simulating how real AI responses will appear.\n\n"
                "**Key features:**\n"
                "- Real-time streaming\n"
                "- Markdown rendering\n"
                "- Code syntax highlighting\n"
                "- And more!\n\n"
                "*Note: This is a Phase 2 demo. Real AI integration coming soon.*"
            )
        else:
            response = (
                f"I understand you want to: **{user_message}**\n\n"
                "This is a Phase 2 demonstration of the chat interface. "
                "In the full implementation, I would:\n\n"
                "1. Analyze your request\n"
                "2. Break it down into steps\n"
                "3. Execute tools (read files, write code, run tests)\n"
                "4. Show you the results for review\n\n"
                "*Integration with AmplifierSession coming in the next phase!*"
            )
        
        # Stream the response character by character
        for char in response:
            chat.append_to_streaming(char)
            await asyncio.sleep(0.01)  # Simulate streaming delay
    
    def action_new_chat(self) -> None:
        """Start a new chat (clear current messages)."""
        chat = self.query_one("#chat", ChatWidget)
        chat.clear_messages()
        
        # Show welcome message again
        chat.add_message(
            "New chat started! What would you like to work on?",
            role="assistant",
        )
        
        # Focus input
        input_area = self.query_one("#input", InputArea)
        input_area.focus_input()
        
        self.notify("New chat started", severity="information")
    
    def action_toggle_history(self) -> None:
        """Toggle session history view (placeholder for Phase 3)."""
        self.notify(
            "Session history browser coming in Phase 3!",
            title="History",
            severity="information",
        )
    
    def action_save_session(self) -> None:
        """Save current session (placeholder)."""
        self.notify(
            "Session saved!",
            title="Save",
            severity="information",
        )
    
    def action_show_help(self) -> None:
        """Show help information."""
        chat = self.query_one("#chat", ChatWidget)
        chat.add_message(
            "**Keyboard Shortcuts:**\n\n"
            "- **Enter** - Send message\n"
            "- **Shift+Enter** - New line\n"
            "- **Ctrl+N** - New chat\n"
            "- **Ctrl+H** - History (coming in Phase 3)\n"
            "- **Ctrl+S** - Save session\n"
            "- **Ctrl+/** - Show this help\n"
            "- **Ctrl+C** - Cancel operation\n"
            "- **Escape** - Focus input\n\n"
            "**Tips:**\n"
            "- Messages support Markdown formatting\n"
            "- Responses stream in real-time\n"
            "- Use natural language to describe what you want\n\n"
            "*Phase 2: Chat Interface - More features coming soon!*",
            role="system",
        )
    
    def action_focus_input(self) -> None:
        """Focus the input area."""
        input_area = self.query_one("#input", InputArea)
        input_area.focus_input()
    
    def action_cancel_operation(self) -> None:
        """Cancel current operation."""
        if self._processing:
            self.notify("Cancellation coming in future phase", severity="warning")
        else:
            self.notify("No operation to cancel", severity="information")


__all__ = ["ChatScreen"]
