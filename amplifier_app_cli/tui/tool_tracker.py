"""Tool execution tracker for TUI.

Hooks into AmplifierSession tool events and forwards them to the UI.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .widgets.tool_panel import ToolExecutionPanel

logger = logging.getLogger(__name__)


class ToolTracker:
    """Tracks tool execution and updates the TUI panel.
    
    Registers hooks with AmplifierSession to capture tool:pre and tool:post
    events, then forwards them to the ToolExecutionPanel for display.
    """
    
    def __init__(self, tool_panel: ToolExecutionPanel):
        """Initialize tool tracker.
        
        Args:
            tool_panel: The UI panel to update with tool activity
        """
        self.tool_panel = tool_panel
        self._call_ids: dict[str, str] = {}  # Maps tool sequence to call_id
        self._sequence = 0
    
    async def on_tool_pre(self, event: str, data: dict[str, Any]):
        """Hook callback for tool:pre event.
        
        Called when a tool is about to execute.
        
        Args:
            event: Event name (should be "tool:pre")
            data: Event data containing tool_name and tool_input
        """
        from amplifier_app_utils.models import HookResult
        
        tool_name = data.get("tool_name", "unknown")
        tool_input = data.get("tool_input", {})
        
        # Generate unique call ID
        call_id = f"{tool_name}_{self._sequence}_{uuid.uuid4().hex[:8]}"
        self._sequence += 1
        
        # Store call ID for matching in post hook
        self._call_ids[f"{tool_name}_{self._sequence}"] = call_id
        
        # Notify panel (safe to call from async hook)
        try:
            self.tool_panel.on_tool_pre(tool_name, tool_input, call_id)
        except Exception as e:
            logger.error(f"Error updating tool panel (pre): {e}", exc_info=True)
        
        # Always continue (don't block tool execution)
        return HookResult(action="continue")
    
    async def on_tool_post(self, event: str, data: dict[str, Any]):
        """Hook callback for tool:post event.
        
        Called when a tool completes execution.
        
        Args:
            event: Event name (should be "tool:post")
            data: Event data containing tool_name and result
        """
        from amplifier_app_utils.models import HookResult
        
        tool_name = data.get("tool_name", "unknown")
        result = data.get("result")
        error = data.get("error")
        
        # Find matching call ID
        call_key = f"{tool_name}_{self._sequence}"
        call_id = self._call_ids.get(call_key, f"{tool_name}_unknown")
        
        # Notify panel (safe to call from async hook)
        try:
            self.tool_panel.on_tool_post(tool_name, result, call_id, error)
        except Exception as e:
            logger.error(f"Error updating tool panel (post): {e}", exc_info=True)
        
        # Clean up call ID
        if call_key in self._call_ids:
            del self._call_ids[call_key]
        
        # Always continue
        return HookResult(action="continue")
    
    def register_hooks(self, session) -> tuple[callable, callable]:
        """Register tool tracking hooks with the session.
        
        Args:
            session: AmplifierSession instance
            
        Returns:
            Tuple of (unregister_pre, unregister_post) functions
        """
        hooks = session.coordinator.get("hooks")
        if not hooks:
            logger.warning("No hooks system found in session")
            return (lambda: None, lambda: None)
        
        # Register with high priority to catch all tool calls
        unregister_pre = hooks.register(
            "tool:pre",
            self.on_tool_pre,
            priority=900,  # Higher than trace collector (1000)
            name="tui_tool_tracker_pre"
        )
        
        unregister_post = hooks.register(
            "tool:post",
            self.on_tool_post,
            priority=900,
            name="tui_tool_tracker_post"
        )
        
        logger.info("Tool tracker hooks registered")
        
        return (unregister_pre, unregister_post)
    
    def unregister_hooks(self, unregister_pre: callable, unregister_post: callable) -> None:
        """Unregister tool tracking hooks.
        
        Args:
            unregister_pre: Function to unregister pre hook
            unregister_post: Function to unregister post hook
        """
        try:
            unregister_pre()
            unregister_post()
            logger.info("Tool tracker hooks unregistered")
        except Exception as e:
            logger.error(f"Error unregistering tool hooks: {e}", exc_info=True)


__all__ = ["ToolTracker"]

