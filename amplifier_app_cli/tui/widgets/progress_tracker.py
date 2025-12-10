"""Progress Tracker for TUI.

Shows AI's thinking steps and progress in a user-friendly way.
Replaces technical tool panel with step-by-step progress display.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from rich.panel import Panel
from rich.text import Text
from textual.reactive import reactive
from textual.widgets import Static

logger = logging.getLogger(__name__)


class ProgressTracker(Static):
    """Panel showing AI's thinking steps and progress.
    
    Displays:
    - Current step description
    - Completed steps with checkmarks
    - Active step with spinner
    - User-friendly language (no technical details)
    """
    
    # Reactive properties for dynamic updates
    current_step: reactive[str | None] = reactive(None)
    steps: reactive[list[dict[str, Any]]] = reactive([])
    
    CSS = """
    ProgressTracker {
        height: auto;
        max-height: 15;
        border: solid $primary;
        padding: 1;
    }
    
    ProgressTracker > Static {
        height: auto;
    }
    """
    
    # Map tool names to user-friendly step descriptions
    TOOL_TO_STEP = {
        "read_file": "Reading files",
        "grep_search": "Searching code",
        "semantic_search": "Analyzing codebase",
        "file_search": "Finding files",
        "list_dir": "Exploring directories",
        "replace_string_in_file": "Editing code",
        "multi_replace_string_in_file": "Making multiple edits",
        "create_file": "Creating new file",
        "run_in_terminal": "Running command",
        "get_terminal_output": "Checking command output",
        "runTests": "Running tests",
        "get_errors": "Checking for errors",
    }
    
    def __init__(self, **kwargs: Any):
        """Initialize progress tracker."""
        super().__init__(**kwargs)
        self._active_step: str | None = None
        self._completed_steps: list[str] = []
        self._step_count: int = 0
    
    def on_mount(self) -> None:
        """Set up panel after mounting."""
        self.update_display()
    
    def start_step(self, step_description: str) -> None:
        """Mark a step as started.
        
        Args:
            step_description: User-friendly description of the step
        """
        self._active_step = step_description
        self._step_count += 1
        self.current_step = step_description
        self.update_display()
        
        logger.debug(f"Step started: {step_description}")
    
    def complete_step(self, step_description: str | None = None) -> None:
        """Mark the current step as completed.
        
        Args:
            step_description: Optional description (uses current if not provided)
        """
        step = step_description or self._active_step
        
        if step and step not in self._completed_steps:
            self._completed_steps.append(step)
            
        self._active_step = None
        self.current_step = None
        self.update_display()
        
        logger.debug(f"Step completed: {step}")
    
    def on_tool_pre(self, tool_name: str, arguments: dict[str, Any], call_id: str) -> None:
        """Convert tool execution to user-friendly step.
        
        Args:
            tool_name: Name of the tool being called
            arguments: Tool input arguments
            call_id: Unique identifier for this call
        """
        # Convert tool name to friendly step description
        step_description = self.TOOL_TO_STEP.get(tool_name, f"Working on {tool_name}")
        
        # Add context from arguments for certain tools
        if tool_name == "read_file" and "filePath" in arguments:
            filename = arguments["filePath"].split("/")[-1].split("\\")[-1]
            step_description = f"Reading {filename}"
        elif tool_name == "create_file" and "filePath" in arguments:
            filename = arguments["filePath"].split("/")[-1].split("\\")[-1]
            step_description = f"Creating {filename}"
        elif tool_name == "replace_string_in_file" and "filePath" in arguments:
            filename = arguments["filePath"].split("/")[-1].split("\\")[-1]
            step_description = f"Editing {filename}"
        elif tool_name == "run_in_terminal" and "command" in arguments:
            # Show first part of command
            cmd = arguments["command"][:30] + ("..." if len(arguments["command"]) > 30 else "")
            step_description = f"Running: {cmd}"
        
        self.start_step(step_description)
    
    def on_tool_post(
        self,
        tool_name: str,
        result: Any,
        call_id: str,
        error: str | None = None,
    ) -> None:
        """Mark tool completion as step completion.
        
        Args:
            tool_name: Name of the tool that completed
            result: Tool output/result
            call_id: Unique identifier for this call
            error: Error message if tool failed
        """
        if error:
            # Don't mark as completed if there was an error
            self._active_step = None
            self.current_step = None
        else:
            self.complete_step()
        
        self.update_display()
    
    def reset(self) -> None:
        """Clear all steps and reset tracker."""
        self._active_step = None
        self._completed_steps = []
        self._step_count = 0
        self.current_step = None
        self.update_display()
    
    def update_display(self) -> None:
        """Update the display with current progress."""
        # Build progress text
        lines: list[str] = []
        
        # Show completed steps (last 5 to avoid clutter)
        recent_completed = self._completed_steps[-5:]
        for step in recent_completed:
            lines.append(f"✓ {step}")
        
        # Show active step with spinner
        if self._active_step:
            lines.append(f"⟳ {self._active_step}...")
        
        # If nothing to show
        if not lines:
            lines.append("Ready to assist")
        
        # Create rich text
        text = Text("\n".join(lines))
        
        # Create panel
        panel = Panel(
            text,
            title=f"[bold]Progress[/bold] ({self._step_count} steps)",
            border_style="blue",
        )
        
        self.update(panel)
