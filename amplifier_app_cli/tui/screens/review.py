"""Review & Verification Screen for AI changes.

This is Phase 2.5 - the critical "co-primary" information need for AI-native developers.
Shows intent vs. result, impact analysis, and accept/reject controls.
"""

from __future__ import annotations

from typing import Any

from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container
from textual.containers import Horizontal
from textual.containers import Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Static


class ConfidenceIndicator(Static):
    """Visual indicator of AI confidence level.
    
    Shows green (high), yellow (medium), or red (low) confidence
    with explanatory text.
    """
    
    def __init__(
        self,
        confidence: str = "high",
        reason: str = "",
        **kwargs: Any,
    ):
        """Initialize confidence indicator.
        
        Args:
            confidence: 'high', 'medium', or 'low'
            reason: Explanation for confidence level
            **kwargs: Additional widget kwargs
        """
        super().__init__(**kwargs)
        self.confidence = confidence
        self.reason = reason
    
    def render(self) -> RenderableType:
        """Render confidence indicator with color and icon."""
        icon_map = {
            "high": ("🟢", "green"),
            "medium": ("🟡", "yellow"),
            "low": ("🔴", "red"),
        }
        
        icon, color = icon_map.get(self.confidence, ("⚪", "dim"))
        
        text = Text()
        text.append(f"{icon} ", style=color)
        text.append(f"{self.confidence.upper()} confidence", style=f"bold {color}")
        
        if self.reason:
            text.append(f"\n{self.reason}", style="dim")
        
        return text


class ImpactAnalysisWidget(Static):
    """Shows blast radius and impact of AI changes.
    
    Displays files changed, functions modified, breaking changes,
    dependency changes, and test coverage.
    """
    
    def __init__(
        self,
        impact_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        """Initialize impact analysis widget.
        
        Args:
            impact_data: Dict with keys like 'files_changed', 'breaking_changes', etc.
            **kwargs: Additional widget kwargs
        """
        super().__init__(**kwargs)
        self.impact_data = impact_data or {}
    
    def render(self) -> RenderableType:
        """Render impact analysis as a formatted table."""
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="bold")
        
        # Extract impact metrics
        files = self.impact_data.get("files_changed", 0)
        functions = self.impact_data.get("functions_modified", 0)
        breaking = self.impact_data.get("breaking_changes", 0)
        deps_added = self.impact_data.get("dependencies_added", 0)
        tests_coverage = self.impact_data.get("test_coverage", "N/A")
        
        # Build table
        table.add_row("Files changed:", str(files))
        table.add_row("Functions modified:", str(functions))
        
        if breaking > 0:
            table.add_row(
                "Breaking changes:",
                f"[red bold]{breaking} ⚠️[/red bold]"
            )
        
        if deps_added > 0:
            table.add_row(
                "Dependencies added:",
                f"[yellow]+{deps_added}[/yellow]"
            )
        
        table.add_row("Test coverage:", str(tests_coverage))
        
        return Panel(
            table,
            title="[bold]IMPACT ANALYSIS[/bold]",
            border_style="cyan",
        )


class ChangesSummaryWidget(Static):
    """Shows intent vs. result comparison.
    
    Displays what the user requested alongside what the AI
    actually implemented.
    """
    
    def __init__(
        self,
        user_request: str = "",
        ai_actions: list[str] | None = None,
        notes: list[str] | None = None,
        **kwargs: Any,
    ):
        """Initialize changes summary widget.
        
        Args:
            user_request: Original user request/prompt
            ai_actions: List of actions AI took
            notes: List of notes/warnings from AI
            **kwargs: Additional widget kwargs
        """
        super().__init__(**kwargs)
        self.user_request = user_request
        self.ai_actions = ai_actions or []
        self.notes = notes or []
    
    def render(self) -> RenderableType:
        """Render intent vs. result comparison."""
        # Build summary text
        summary = Text()
        
        # User request section
        summary.append("YOUR REQUEST:\n", style="bold cyan")
        summary.append(f'"{self.user_request}"\n\n', style="italic")
        
        # AI actions section
        summary.append("AI IMPLEMENTED:\n", style="bold green")
        for action in self.ai_actions:
            summary.append(f"  ✓ {action}\n", style="green")
        
        # Notes/warnings section
        if self.notes:
            summary.append("\nNOTES:\n", style="bold yellow")
            for note in self.notes:
                summary.append(f"  ⚠️ {note}\n", style="yellow")
        
        return Panel(
            summary,
            title="[bold]SUMMARY[/bold]",
            border_style="blue",
        )


class ReviewScreen(Screen):
    """Review & Verification Screen for AI changes.
    
    This screen appears after AI completes work, allowing the developer
    to review changes before accepting them. This is the critical
    "co-primary" information need identified in user needs analysis.
    
    Features:
    - Intent vs. result comparison
    - Impact analysis (blast radius)
    - Confidence indicators
    - Accept/reject controls
    - Ability to request clarification or modifications
    """
    
    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("a", "accept", "Accept"),
        ("r", "reject", "Reject"),
        ("e", "explain", "Explain"),
    ]
    
    CSS = """
    ReviewScreen {
        background: $surface;
    }
    
    #review-content {
        height: 1fr;
        overflow-y: auto;
        padding: 1;
    }
    
    #controls {
        height: auto;
        dock: bottom;
        background: $panel;
        padding: 1;
    }
    
    .review-section {
        margin: 1 0;
    }
    
    Button {
        margin: 0 1;
    }
    
    Button.accept {
        background: $success;
    }
    
    Button.reject {
        background: $error;
    }
    
    Button.explain {
        background: $primary;
    }
    """
    
    def __init__(
        self,
        user_request: str = "",
        ai_actions: list[str] | None = None,
        notes: list[str] | None = None,
        impact_data: dict[str, Any] | None = None,
        confidence: str = "high",
        confidence_reason: str = "",
        **kwargs: Any,
    ):
        """Initialize review screen.
        
        Args:
            user_request: Original user request
            ai_actions: List of actions AI took
            notes: List of notes/warnings
            impact_data: Impact analysis data
            confidence: AI confidence level ('high', 'medium', 'low')
            confidence_reason: Explanation for confidence level
            **kwargs: Additional screen kwargs
        """
        super().__init__(**kwargs)
        self.user_request = user_request
        self.ai_actions = ai_actions or []
        self.notes = notes or []
        self.impact_data = impact_data or {}
        self.confidence = confidence
        self.confidence_reason = confidence_reason
        self.decision = None  # Will be set to 'accept', 'reject', or 'explain'
    
    def compose(self) -> ComposeResult:
        """Create child widgets for review screen."""
        yield Header()
        
        with Container(id="review-content"):
            # Confidence indicator at top
            yield ConfidenceIndicator(
                confidence=self.confidence,
                reason=self.confidence_reason,
                classes="review-section",
            )
            
            # Changes summary (intent vs. result)
            yield ChangesSummaryWidget(
                user_request=self.user_request,
                ai_actions=self.ai_actions,
                notes=self.notes,
                classes="review-section",
            )
            
            # Impact analysis (blast radius)
            yield ImpactAnalysisWidget(
                impact_data=self.impact_data,
                classes="review-section",
            )
            
            # Additional info text
            yield Static(
                "[dim]Press 'e' to see detailed explanations, "
                "'a' to accept, 'r' to reject, or 'Esc' to cancel.[/dim]",
                classes="review-section",
            )
        
        # Control buttons at bottom
        with Horizontal(id="controls"):
            yield Button("✓ Accept", variant="success", id="btn-accept", classes="accept")
            yield Button("⚠️ Accept with Notes", variant="primary", id="btn-accept-notes")
            yield Button("✗ Reject", variant="error", id="btn-reject", classes="reject")
            yield Button("💡 Explain", variant="primary", id="btn-explain", classes="explain")
            yield Button("⏸️ Defer", variant="default", id="btn-defer")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id
        
        if button_id == "btn-accept":
            self.decision = "accept"
            self.dismiss({"decision": "accept"})
        
        elif button_id == "btn-accept-notes":
            self.decision = "accept_notes"
            self.dismiss({"decision": "accept_notes"})
        
        elif button_id == "btn-reject":
            self.decision = "reject"
            self.dismiss({"decision": "reject"})
        
        elif button_id == "btn-explain":
            self.decision = "explain"
            self.action_explain()
        
        elif button_id == "btn-defer":
            self.decision = "defer"
            self.dismiss({"decision": "defer"})
    
    def action_accept(self) -> None:
        """Accept changes (keyboard shortcut)."""
        self.decision = "accept"
        self.dismiss({"decision": "accept"})
    
    def action_reject(self) -> None:
        """Reject changes (keyboard shortcut)."""
        self.decision = "reject"
        self.dismiss({"decision": "reject"})
    
    def action_explain(self) -> None:
        """Request detailed explanation (keyboard shortcut).
        
        Future: Open modal with detailed explanations for each change.
        For now, just show a notification.
        """
        self.app.notify(
            "💡 Detailed explanations coming in future phase",
            title="Explain",
            severity="information",
        )
    
    def action_cancel(self) -> None:
        """Cancel review (keyboard shortcut)."""
        self.decision = "cancel"
        self.dismiss({"decision": "cancel"})


# Convenience function for showing review screen
def show_review_screen(
    app,
    user_request: str,
    ai_actions: list[str],
    notes: list[str] | None = None,
    impact_data: dict[str, Any] | None = None,
    confidence: str = "high",
    confidence_reason: str = "",
) -> None:
    """Show review screen and wait for user decision.
    
    Args:
        app: Textual app instance
        user_request: Original user request
        ai_actions: List of actions AI took
        notes: Optional list of notes/warnings
        impact_data: Optional impact analysis data
        confidence: AI confidence level
        confidence_reason: Explanation for confidence
        
    Returns:
        Dict with 'decision' key containing user's choice
    """
    screen = ReviewScreen(
        user_request=user_request,
        ai_actions=ai_actions,
        notes=notes,
        impact_data=impact_data,
        confidence=confidence,
        confidence_reason=confidence_reason,
    )
    
    return app.push_screen(screen)
