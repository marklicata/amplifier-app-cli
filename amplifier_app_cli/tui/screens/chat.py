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
from datetime import UTC
from datetime import datetime
from pathlib import Path
from typing import Any

from amplifier_core import AmplifierSession
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer
from textual.widgets import Header

from ...paths import create_module_resolver
from ...session_store import SessionStore
from ..tool_tracker import ToolTracker
from ..widgets.chat import ChatWidget
from ..widgets.input import InputArea
from ..widgets.input import InputSubmitted
from ..widgets.progress_tracker import ProgressTracker

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
    
    #main-content {
        height: 1fr;
        layout: vertical;
    }
    
    #chat-container {
        height: 1fr;
    }
    
    #progress-tracker {
        height: auto;
        max-height: 15;
        border-top: solid $primary;
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
        self._initial_transcript = None
        self._tool_tracker = None
        self._tool_tracker_unreg = None
        
        # Generate session ID if not provided
        if not self.session_id:
            import uuid
            self.session_id = str(uuid.uuid4())
    
    def compose(self) -> ComposeResult:
        """Create child widgets for chat screen."""
        yield Header()
        
        with Container(id="main-content"):
            with Container(id="chat-container"):
                yield ChatWidget(id="chat")
            
            # Progress tracker showing AI's thinking steps
            yield ProgressTracker(id="progress-tracker")
        
        yield InputArea(id="input")
        yield Footer()
    
    def on_mount(self) -> None:
        """Set up chat screen after mounting."""
        # Extract provider and model info for subtitle
        provider_name = "unknown"
        model_name = "unknown"
        if isinstance(self.config.get("providers"), list) and self.config["providers"]:
            first_provider = self.config["providers"][0]
            if isinstance(first_provider, dict):
                provider_name = first_provider.get("module", "unknown").replace("provider-", "")
                if "config" in first_provider:
                    provider_config = first_provider["config"]
                    model_name = provider_config.get("model") or provider_config.get("default_model", "unknown")
        
        # Update subtitle with profile, provider, model, and session
        self.sub_title = f"{self.profile} | {provider_name}/{model_name} | {self.session_id[:8]}..."
        
        # Try to load existing session
        chat = self.query_one("#chat", ChatWidget)
        store = SessionStore()
        
        if store.exists(self.session_id):
            try:
                transcript, metadata = store.load(self.session_id)
                self._initial_transcript = transcript
                
                # Show resumed session banner
                chat.add_message(
                    f"**Session Resumed** ({self.session_id[:8]}...)\n\n"
                    f"Previous messages: {len(transcript)}\n"
                    f"Profile: {self.profile}\n\n"
                    "Continue the conversation below.",
                    role="system",
                )
                
                # Display previous messages
                for msg in transcript:
                    role = msg.get("role", "assistant")
                    content = msg.get("content", "")
                    if role in ("user", "assistant"):
                        chat.add_message(content, role=role)
                
                logger.info(f"Loaded {len(transcript)} messages from session {self.session_id}")
                
            except Exception as e:
                logger.error(f"Failed to load session: {e}", exc_info=True)
                chat.add_message(
                    f"Could not load session history: {str(e)}\n\n"
                    "Starting fresh conversation.",
                    role="system",
                )
        else:
            # New session - show welcome message
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
        
        # Initialize session immediately (don't wait for first message)
        self.run_worker(self._initialize_session_on_mount(), exclusive=True)
    
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
        
        # Process the message (user message is added inside _process_user_message now)
        await self._process_user_message(user_message)
    
    async def _process_user_message(self, message: str) -> None:
        """Process user message and get AI response.
        
        Args:
            message: User's message text
        """
        self._processing = True
        
        try:
            chat = self.query_one("#chat", ChatWidget)
            
            # Add user message to chat FIRST (fix #3)
            chat.add_message(message, role="user")
            
            # Check if session is initialized
            if not self.amplifier_session:
                # This shouldn't happen now that we init on mount, but just in case
                chat.add_message(
                    "⚠️ Session not initialized. Please wait...",
                    role="system",
                )
                self._processing = False
                return
            
            # Start streaming response
            chat.start_streaming_message(role="assistant")
            
            # Execute prompt with real AmplifierSession
            try:
                response = await self.amplifier_session.execute(message)
                
                # Add the complete response to the streaming message
                chat.append_to_streaming(response)
                
                # Finalize streaming
                chat.finalize_streaming()
                
                # Save session after each interaction
                await self._save_session()
                
            except Exception as e:
                logger.error(f"Error executing prompt: {e}", exc_info=True)
                chat.finalize_streaming()
                chat.add_message(
                    f"Error: {str(e)}\n\nPlease try again.",
                    role="system",
                )
            
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            chat = self.query_one("#chat", ChatWidget)
            chat.add_message(
                f"Error: {str(e)}\n\nPlease try again.",
                role="system",
            )
        
        finally:
            self._processing = False
            
            # Focus input for next message
            input_area = self.query_one("#input", InputArea)
            input_area.focus_input()
    
    async def _initialize_session_on_mount(self) -> None:
        """Initialize session on mount (runs in background worker)."""
        try:
            chat = self.query_one("#chat", ChatWidget)
            
            # Show initialization message
            chat.add_message(
                "Initializing AI session...",
                role="system",
            )
            
            # Initialize the session
            await self._initialize_session()
            
            # Update message to show ready
            chat.add_message(
                "Session ready! Ask me anything.",
                role="system",
            )
            
            logger.info("Session initialized successfully on mount")
            
        except Exception as e:
            logger.error(f"Failed to initialize session on mount: {e}", exc_info=True)
            chat = self.query_one("#chat", ChatWidget)
            chat.add_message(
                f"Failed to initialize session: {str(e)}\n\n"
                "Please check your configuration and restart.",
                role="system",
            )
    
    async def _initialize_session(self) -> None:
        """Initialize AmplifierSession with proper configuration."""
        try:
            # Create UX systems for TUI
            from ...ui import CLIApprovalSystem, CLIDisplaySystem
            
            approval_system = CLIApprovalSystem()
            display_system = CLIDisplaySystem()
            
            # Create session
            self.amplifier_session = AmplifierSession(
                self.config,
                session_id=self.session_id,
                approval_system=approval_system,
                display_system=display_system,
            )
            
            # Mount module source resolver
            resolver = create_module_resolver()
            await self.amplifier_session.coordinator.mount("module-source-resolver", resolver)
            
            # Register capabilities
            from ...lib.mention_loading.deduplicator import ContentDeduplicator
            from ...lib.mention_loading.resolver import MentionResolver
            
            mention_resolver = MentionResolver()
            self.amplifier_session.coordinator.register_capability("mention_resolver", mention_resolver)
            
            mention_deduplicator = ContentDeduplicator()
            self.amplifier_session.coordinator.register_capability("mention_deduplicator", mention_deduplicator)
            
            # Initialize session (loads modules, etc.)
            await self.amplifier_session.initialize()
            
            # Restore transcript if resuming
            if self._initial_transcript:
                for message in self._initial_transcript:
                    await self.amplifier_session.add_message(
                        role=message.get("role"),
                        content=message.get("content", ""),
                    )
                logger.info(f"Restored {len(self._initial_transcript)} messages to session context")
            
            # Register CLI approval provider if needed
            from ...approval_provider import CLIApprovalProvider
            from ...console import console
            
            register_provider = self.amplifier_session.coordinator.get_capability("approval.register_provider")
            if register_provider:
                approval_provider = CLIApprovalProvider(console)
                register_provider(approval_provider)
            
            # Register tool tracker to show progress in tracker widget
            progress_tracker = self.query_one("#progress-tracker", ProgressTracker)
            self._tool_tracker = ToolTracker(progress_tracker)
            unreg_pre, unreg_post = self._tool_tracker.register_hooks(self.amplifier_session)
            self._tool_tracker_unreg = (unreg_pre, unreg_post)
            
            logger.info(f"AmplifierSession initialized (session_id={self.session_id})")
            
        except Exception as e:
            logger.error(f"Failed to initialize session: {e}", exc_info=True)
            raise
    
    async def _save_session(self) -> None:
        """Save current session state to SessionStore."""
        try:
            if not self.amplifier_session:
                return
            
            # Get transcript from context
            context = self.amplifier_session.coordinator.get("context")
            if not context or not hasattr(context, "get_messages"):
                return
            
            messages = await context.get_messages()
            
            # Extract model name from config
            model_name = "unknown"
            if isinstance(self.config.get("providers"), list) and self.config["providers"]:
                first_provider = self.config["providers"][0]
                if isinstance(first_provider, dict) and "config" in first_provider:
                    provider_config = first_provider["config"]
                    model_name = provider_config.get("model") or provider_config.get("default_model", "unknown")
            
            # Create metadata
            metadata = {
                "session_id": self.session_id,
                "created": datetime.now(UTC).isoformat(),
                "profile": self.profile,
                "model": model_name,
                "turn_count": len([m for m in messages if m.get("role") == "user"]),
            }
            
            # Save to store
            store = SessionStore()
            store.save(self.session_id, messages, metadata)
            
            logger.debug(f"Session saved: {self.session_id}")
            
        except Exception as e:
            logger.error(f"Failed to save session: {e}", exc_info=True)
            # Don't raise - saving is best-effort
    
    async def _show_review_screen_if_needed(self, user_request: str) -> None:
        """Show review screen if AI made file modifications.
        
        This is a placeholder for Phase 3 integration. In the future, this will:
        - Track tool executions via hooks
        - Detect file modifications
        - Extract impact metrics
        - Show ReviewScreen for user approval
        
        Args:
            user_request: The user's original request
        """
        # TODO: Implement file modification detection via hooks or tool tracking
        # For now, this is a placeholder that can be called after execute()
        # 
        # Future implementation:
        # 1. Register hook listener for tool:post events
        # 2. Track file write operations
        # 3. Calculate impact metrics (files changed, functions modified, etc.)
        # 4. Show ReviewScreen with collected data
        # 5. Handle user decision (accept/reject/defer)
        pass
    
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
    
    async def on_screen_suspend(self) -> None:
        """Called when screen is suspended (going to background)."""
        # Cleanup tool tracker hooks
        if self._tool_tracker and self._tool_tracker_unreg:
            unreg_pre, unreg_post = self._tool_tracker_unreg
            self._tool_tracker.unregister_hooks(unreg_pre, unreg_post)
            logger.info("Tool tracker hooks unregistered on suspend")


__all__ = ["ChatScreen"]
