#!/usr/bin/env python
"""Test script for Chat Screen (Phase 2).

This demonstrates the interactive chat interface with:
- Message bubbles for user and assistant
- Streaming responses
- Multi-line input
- Keyboard shortcuts
- Markdown rendering
"""

import sys
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from textual.app import App

from amplifier_app_cli.tui.screens.chat import ChatScreen


class ChatTestApp(App):
    """Test app to demonstrate chat screen."""
    
    TITLE = "Amplifier Chat - Phase 2 Demo"
    
    def on_mount(self) -> None:
        """Show chat screen on mount."""
        chat_screen = ChatScreen(
            session_id="demo-session",
            profile="test-profile",
        )
        self.push_screen(chat_screen)


def main():
    """Run the chat screen test app."""
    print("🚀 Starting Chat Screen Test App (Phase 2)")
    print("=" * 60)
    print("This demonstrates Phase 2: Enhanced Chat Interface")
    print()
    print("Features demonstrated:")
    print("  • Message bubbles with role-based styling")
    print("  • Streaming assistant responses (simulated)")
    print("  • Multi-line input (Shift+Enter for new line)")
    print("  • Markdown rendering in messages")
    print("  • Keyboard shortcuts")
    print()
    print("Try these:")
    print("  • Type 'hello' to see a welcome message")
    print("  • Type 'test' to see streaming demonstration")
    print("  • Type anything else to see general response")
    print()
    print("Keyboard shortcuts:")
    print("  • Enter - Send message")
    print("  • Shift+Enter - New line in input")
    print("  • Ctrl+N - New chat (clear messages)")
    print("  • Ctrl+/ - Show help in chat")
    print("  • Ctrl+S - Save session (placeholder)")
    print("  • Ctrl+C - Cancel (placeholder)")
    print("  • Esc - Focus input")
    print()
    print("Note: This is a demo with simulated AI responses.")
    print("Real AmplifierSession integration coming soon!")
    print("=" * 60)
    print()
    
    app = ChatTestApp()
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Chat test app closed")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
