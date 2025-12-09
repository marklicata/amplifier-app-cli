#!/usr/bin/env python
"""Test script for Review Screen (Phase 2.5).

This demonstrates the review screen with mock data showing
the key features:
- Intent vs. result comparison
- Impact analysis (blast radius)
- Confidence indicators
- Accept/reject controls
"""

import sys
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent))

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button

from amplifier_app_cli.tui.screens.review import ReviewScreen


class ReviewTestApp(App):
    """Test app to demonstrate review screen."""
    
    CSS = """
    Screen {
        align: center middle;
    }
    
    Button {
        margin: 1;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create main screen."""
        yield Header()
        yield Button("Show High Confidence Review", id="btn-high")
        yield Button("Show Low Confidence Review", id="btn-low")
        yield Button("Show Breaking Changes Review", id="btn-breaking")
        yield Footer()
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press to show different review scenarios."""
        button_id = event.button.id
        
        if button_id == "btn-high":
            await self.show_high_confidence_review()
        elif button_id == "btn-low":
            await self.show_low_confidence_review()
        elif button_id == "btn-breaking":
            await self.show_breaking_changes_review()
    
    async def show_high_confidence_review(self) -> None:
        """Show review with high confidence."""
        screen = ReviewScreen(
            user_request="Add authentication to the API",
            ai_actions=[
                "Added JWT middleware",
                "Created /login endpoint",
                "Created /logout endpoint",
                "Added user model",
                "Protected all /api/* routes",
            ],
            notes=[
                "Using default 24h session timeout (you didn't specify)",
            ],
            impact_data={
                "files_changed": 8,
                "functions_modified": 12,
                "breaking_changes": 0,
                "dependencies_added": 2,
                "test_coverage": "87%",
            },
            confidence="high",
            confidence_reason="Seen this authentication pattern 1000+ times in production",
        )
        
        result = await self.push_screen(screen)
        self.notify(f"User decision: {result.get('decision')}", title="Review Result")
    
    async def show_low_confidence_review(self) -> None:
        """Show review with low confidence."""
        screen = ReviewScreen(
            user_request="Optimize database queries",
            ai_actions=[
                "Added database indexes on user_id columns",
                "Implemented query caching with Redis",
                "Converted N+1 queries to batch loading",
            ],
            notes=[
                "Not sure about your database load patterns",
                "Cache TTL of 5 minutes is a guess",
                "May need adjustment based on real usage",
            ],
            impact_data={
                "files_changed": 15,
                "functions_modified": 23,
                "breaking_changes": 0,
                "dependencies_added": 1,
                "test_coverage": "62%",
            },
            confidence="low",
            confidence_reason="Database optimization highly dependent on actual usage patterns",
        )
        
        result = await self.push_screen(screen)
        self.notify(f"User decision: {result.get('decision')}", title="Review Result")
    
    async def show_breaking_changes_review(self) -> None:
        """Show review with breaking changes."""
        screen = ReviewScreen(
            user_request="Update API to use camelCase",
            ai_actions=[
                "Converted all API responses to camelCase",
                "Updated serializers",
                "Updated frontend to match",
            ],
            notes=[
                "This is a BREAKING CHANGE for API consumers",
                "Existing clients will break until updated",
                "Consider versioning the API instead",
            ],
            impact_data={
                "files_changed": 45,
                "functions_modified": 78,
                "breaking_changes": 12,
                "dependencies_added": 0,
                "test_coverage": "91%",
            },
            confidence="medium",
            confidence_reason="Implementation is correct, but breaking changes are risky",
        )
        
        result = await self.push_screen(screen)
        self.notify(f"User decision: {result.get('decision')}", title="Review Result")


def main():
    """Run the review screen test app."""
    print("🚀 Starting Review Screen Test App")
    print("=" * 60)
    print("This demonstrates Phase 2.5: Review & Verification Screen")
    print()
    print("Features demonstrated:")
    print("  • Intent vs. Result comparison")
    print("  • Impact analysis (blast radius)")
    print("  • Confidence indicators")
    print("  • Accept/reject controls")
    print()
    print("Try these scenarios:")
    print("  1. High Confidence - Standard authentication implementation")
    print("  2. Low Confidence - Database optimization (AI unsure)")
    print("  3. Breaking Changes - API changes that break clients")
    print()
    print("Keyboard shortcuts:")
    print("  • a = Accept")
    print("  • r = Reject")
    print("  • e = Explain (placeholder)")
    print("  • Esc = Cancel")
    print("=" * 60)
    print()
    
    app = ReviewTestApp()
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Test app closed")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
