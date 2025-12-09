"""Main Textual TUI application for Amplifier CLI.

This is the Phase 1 minimal implementation that proves the architecture.
It provides a basic interface that displays output in a scrollable log.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from rich.console import RenderableType
from textual.app import App
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import RichLog

logger = logging.getLogger(__name__)


class AmplifierApp(App):
    """Amplifier TUI Application.
    
    Phase 1 minimal implementation:
    - Header with title and session info
    - Scrollable log for output
    - Footer with keybindings
    - Basic async integration proof-of-concept
    
    Future phases will add:
    - Chat interface with input area
    - Session browser
    - Settings screens
    - Tool execution panels
    """
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    Header {
        background: $primary;
        color: $text;
    }
    
    #log-container {
        height: 1fr;
        border: solid $primary;
    }
    
    RichLog {
        background: $surface;
        color: $text;
        padding: 1;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("ctrl+c", "quit", "Quit", show=False),
        ("ctrl+l", "clear_log", "Clear"),
        ("?", "help", "Help"),
    ]
    
    TITLE = "Amplifier"
    SUB_TITLE = "AI-Powered Development CLI"
    
    def __init__(
        self,
        config: dict | None = None,
        session_id: str | None = None,
        profile: str = "default",
        **kwargs: Any,
    ):
        """Initialize TUI application.
        
        Args:
            config: Amplifier configuration dict
            session_id: Optional session ID to resume
            profile: Profile name to use
            **kwargs: Additional Textual app kwargs
        """
        super().__init__(**kwargs)
        self.amplifier_config = config or {}
        self.amplifier_session_id = session_id
        self.amplifier_profile = profile
        self.amplifier_session = None
        
        # Update subtitle with profile info
        if profile:
            self.sub_title = f"Profile: {profile}"
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app.
        
        Phase 1 layout:
        - Header (title + session info)
        - Container with RichLog (scrollable output)
        - Footer (keybindings)
        """
        yield Header(show_clock=True)
        
        with Container(id="log-container"):
            yield RichLog(id="output-log", highlight=True, markup=True)
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when app is mounted.
        
        Phase 1: Display welcome message and basic info.
        Phase 2: Launch chat screen directly.
        """
        # Phase 2: Launch chat screen directly
        from .screens.chat import ChatScreen
        
        chat_screen = ChatScreen(
            session_id=self.amplifier_session_id,
            profile=self.amplifier_profile,
            config=self.amplifier_config,
        )
        
        self.push_screen(chat_screen)
        
        logger.info("TUI mounted - launching chat screen")
    
    def action_clear_log(self) -> None:
        """Clear the output log."""
        log = self.query_one("#output-log", RichLog)
        log.clear()
        log.write("[dim]Log cleared[/dim]")
    
    def action_help(self) -> None:
        """Show help information."""
        log = self.query_one("#output-log", RichLog)
        log.write("")
        log.write("[bold]Amplifier TUI - Phase 1[/bold]")
        log.write("")
        log.write("[bold cyan]Keyboard Shortcuts:[/bold cyan]")
        log.write("  [bold]q[/bold] or [bold]Ctrl+C[/bold] - Quit")
        log.write("  [bold]Ctrl+L[/bold] - Clear log")
        log.write("  [bold]?[/bold] - Show this help")
        log.write("")
        log.write("[bold cyan]Coming Soon (Phase 2+):[/bold cyan]")
        log.write("  • Interactive chat interface")
        log.write("  • Message streaming")
        log.write("  • Session browser")
        log.write("  • Visual configuration")
        log.write("  • Tool execution panels")
        log.write("")
    
    def write_log(self, content: RenderableType) -> None:
        """Write content to the log.
        
        Helper method for easy log access from other components.
        
        Args:
            content: Rich renderable content to write
        """
        log = self.query_one("#output-log", RichLog)
        log.write(content)
    
    async def on_exit(self) -> None:
        """Called when app is exiting.
        
        Future: Clean up AmplifierSession and connections.
        """
        if self.amplifier_session:
            try:
                await self.amplifier_session.cleanup()
            except Exception as e:
                logger.error(f"Error cleaning up session: {e}")


def run_tui(
    config: dict | None = None,
    session_id: str | None = None,
    profile: str = "default",
) -> None:
    """Run the Amplifier TUI application.
    
    Entry point for TUI mode from main CLI.
    
    Args:
        config: Amplifier configuration dict
        session_id: Optional session ID to resume
        profile: Profile name to use
    """
    app = AmplifierApp(
        config=config,
        session_id=session_id,
        profile=profile,
    )
    
    try:
        app.run()
    except Exception as e:
        logger.error(f"TUI error: {e}")
        raise
