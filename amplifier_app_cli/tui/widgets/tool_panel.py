"""Tool Execution Panel for TUI.

Phase 5: Tool Feedback & Visibility
Shows real-time tool calls, inputs, outputs, and progress.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from textual.reactive import reactive
from textual.widgets import Static

logger = logging.getLogger(__name__)


class ToolExecutionPanel(Static):
    """Panel showing real-time tool execution activity.
    
    Displays:
    - Current tool being executed
    - Tool call history
    - Inputs and outputs
    - Execution time
    - Success/error status
    """
    
    # Reactive properties for dynamic updates
    current_tool: reactive[str | None] = reactive(None)
    tool_history: reactive[list[dict[str, Any]]] = reactive([])
    
    CSS = """
    ToolExecutionPanel {
        height: auto;
        max-height: 20;
        border: solid $primary;
        padding: 1;
    }
    
    ToolExecutionPanel > Static {
        height: auto;
    }
    """
    
    def __init__(self, **kwargs: Any):
        """Initialize tool execution panel."""
        super().__init__(**kwargs)
        self._active_calls: dict[str, dict[str, Any]] = {}
        self._completed_calls: list[dict[str, Any]] = []
        self._max_history = 10  # Show last 10 tool calls
    
    def on_mount(self) -> None:
        """Set up panel after mounting."""
        self.update_display()
    
    def on_tool_pre(self, tool_name: str, arguments: dict[str, Any], call_id: str) -> None:
        """Called when a tool execution starts.
        
        Args:
            tool_name: Name of the tool being called
            arguments: Tool input arguments
            call_id: Unique identifier for this call
        """
        self._active_calls[call_id] = {
            "tool": tool_name,
            "arguments": arguments,
            "start_time": datetime.now(UTC),
            "status": "running",
        }
        
        self.current_tool = tool_name
        self.update_display()
        
        logger.debug(f"Tool started: {tool_name} (id={call_id})")
    
    def on_tool_post(
        self,
        tool_name: str,
        result: Any,
        call_id: str,
        error: str | None = None,
    ) -> None:
        """Called when a tool execution completes.
        
        Args:
            tool_name: Name of the tool that completed
            result: Tool output/result
            call_id: Unique identifier for this call
            error: Error message if tool failed
        """
        if call_id in self._active_calls:
            call_info = self._active_calls.pop(call_id)
            
            # Calculate duration
            end_time = datetime.now(UTC)
            duration_ms = (end_time - call_info["start_time"]).total_seconds() * 1000
            
            # Store completed call
            completed = {
                "tool": tool_name,
                "arguments": call_info["arguments"],
                "result": result,
                "duration_ms": round(duration_ms, 2),
                "timestamp": end_time.isoformat(),
                "status": "error" if error else "success",
                "error": error,
            }
            
            self._completed_calls.append(completed)
            
            # Keep only last N calls
            if len(self._completed_calls) > self._max_history:
                self._completed_calls = self._completed_calls[-self._max_history:]
            
            # Update reactive property to trigger re-render
            self.tool_history = list(self._completed_calls)
            
            # Clear current tool if no active calls
            if not self._active_calls:
                self.current_tool = None
            
            self.update_display()
            
            logger.debug(f"Tool completed: {tool_name} in {duration_ms:.2f}ms (id={call_id})")
    
    def update_display(self) -> None:
        """Update the panel display."""
        self.update(self.render())
    
    def render(self) -> RenderableType:
        """Render the tool execution panel."""
        # If no activity, show empty state
        if not self._active_calls and not self._completed_calls:
            return Panel(
                Text("No tool activity yet", style="dim"),
                title="🔧 Tool Execution",
                border_style="dim",
            )
        
        content = Text()
        
        # Show active tool calls
        if self._active_calls:
            content.append("⏳ Active:\n", style="bold cyan")
            for call_id, call_info in self._active_calls.items():
                tool = call_info["tool"]
                content.append(f"  • {tool}", style="yellow")
                
                # Show key arguments (abbreviated)
                args = call_info["arguments"]
                if args:
                    arg_str = ", ".join(f"{k}={str(v)[:30]}..." if len(str(v)) > 30 else f"{k}={v}" 
                                       for k, v in list(args.items())[:2])
                    content.append(f" ({arg_str})", style="dim")
                
                content.append("\n")
            content.append("\n")
        
        # Show recent completed calls
        if self._completed_calls:
            content.append("📋 Recent:\n", style="bold")
            
            # Show last 5 calls
            recent = self._completed_calls[-5:]
            for call in recent:
                tool = call["tool"]
                status = call["status"]
                duration = call["duration_ms"]
                
                # Status indicator
                if status == "success":
                    content.append("  ✓ ", style="green")
                else:
                    content.append("  ✗ ", style="red")
                
                # Tool name
                content.append(f"{tool}", style="yellow" if status == "success" else "red")
                
                # Duration
                content.append(f" ({duration:.0f}ms)", style="dim")
                
                # Error if present
                if call.get("error"):
                    content.append(f"\n    Error: {call['error']}", style="red dim")
                
                content.append("\n")
        
        return Panel(
            content,
            title="🔧 Tool Execution",
            border_style="cyan" if self._active_calls else "dim",
        )
    
    def clear_history(self) -> None:
        """Clear tool execution history."""
        self._completed_calls.clear()
        self.tool_history = []
        self.update_display()


class MiniToolIndicator(Static):
    """Compact tool activity indicator for chat bubbles.
    
    Shows a small badge when tools are being executed.
    Can be embedded in chat messages.
    """
    
    def __init__(self, tool_name: str, status: str = "running", **kwargs: Any):
        """Initialize mini tool indicator.
        
        Args:
            tool_name: Name of the tool
            status: 'running', 'success', or 'error'
            **kwargs: Additional widget kwargs
        """
        super().__init__(**kwargs)
        self.tool_name = tool_name
        self.status = status
    
    def render(self) -> RenderableType:
        """Render the mini indicator."""
        if self.status == "running":
            icon = "⏳"
            style = "yellow"
        elif self.status == "success":
            icon = "✓"
            style = "green"
        else:
            icon = "✗"
            style = "red"
        
        return Text(f"{icon} {self.tool_name}", style=style)


__all__ = ["ToolExecutionPanel", "MiniToolIndicator"]
