"""Reusable review widgets for TUI.

These widgets are used in the ReviewScreen but can also be used
elsewhere in the TUI for showing confidence, impact, etc.
"""

from __future__ import annotations

from typing import Any

from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from textual.widgets import Static


class ConfidenceBadge(Static):
    """Small confidence indicator badge.
    
    Can be used inline in chat or other places where you need
    a compact confidence indicator.
    """
    
    def __init__(self, confidence: str = "high", **kwargs: Any):
        """Initialize confidence badge.
        
        Args:
            confidence: 'high', 'medium', or 'low'
            **kwargs: Additional widget kwargs
        """
        super().__init__(**kwargs)
        self.confidence = confidence
    
    def render(self) -> RenderableType:
        """Render compact confidence badge."""
        icon_map = {
            "high": "🟢",
            "medium": "🟡",
            "low": "🔴",
        }
        
        icon = icon_map.get(self.confidence, "⚪")
        return Text(f"{icon} {self.confidence.capitalize()}")


class MiniImpactSummary(Static):
    """Compact impact summary for inline display.
    
    Shows just the key metrics in a single line or small box.
    """
    
    def __init__(self, impact_data: dict[str, Any] | None = None, **kwargs: Any):
        """Initialize mini impact summary.
        
        Args:
            impact_data: Impact metrics dict
            **kwargs: Additional widget kwargs
        """
        super().__init__(**kwargs)
        self.impact_data = impact_data or {}
    
    def render(self) -> RenderableType:
        """Render compact impact summary."""
        files = self.impact_data.get("files_changed", 0)
        breaking = self.impact_data.get("breaking_changes", 0)
        
        summary = Text()
        summary.append(f"{files} files", style="cyan")
        
        if breaking > 0:
            summary.append(" · ", style="dim")
            summary.append(f"{breaking} breaking", style="red bold")
        
        return summary


__all__ = ["ConfidenceBadge", "MiniImpactSummary"]
