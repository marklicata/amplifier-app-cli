#!/usr/bin/env python
"""Test script for Tool Execution Panel (Phase 5).

This demonstrates the tool execution panel showing real-time tool calls.
Run with: python test_tool_panel.py
"""

import sys
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent))

from amplifier_app_cli.tui.app import run_tui
from amplifier_app_cli.runtime.config import resolve_app_config
from amplifier_app_cli.paths import create_config_manager, create_profile_loader, create_agent_loader
from amplifier_app_cli.lib.app_settings import AppSettings
from amplifier_app_cli.data.profiles import get_system_default_profile
from amplifier_app_cli.console import console


def main():
    """Run the TUI with tool execution panel."""
    print("🔧 Starting Amplifier TUI - Tool Execution Panel Test")
    print("=" * 60)
    print("Phase 5: Tool Feedback & Visibility")
    print()
    print("Features:")
    print("  ✓ Real-time tool execution display")
    print("  ✓ Tool inputs and outputs shown")
    print("  ✓ Execution timing tracked")
    print("  ✓ Success/error status indicators")
    print()
    print("Try asking the AI to:")
    print("  • Read a file")
    print("  • Search for code")
    print("  • Run a command")
    print("  • Create a todo list")
    print()
    print("Watch the tool panel at the bottom to see tools in action!")
    print("=" * 60)
    print()
    
    # Load configuration
    config_manager = create_config_manager()
    profile_loader = create_profile_loader()
    agent_loader = create_agent_loader()
    app_settings = AppSettings(config_manager)
    
    active_profile_name = config_manager.get_active_profile() or get_system_default_profile()
    
    try:
        config_data = resolve_app_config(
            config_manager=config_manager,
            profile_loader=profile_loader,
            agent_loader=agent_loader,
            app_settings=app_settings,
            cli_config={},
            profile_override=active_profile_name,
            console=console,
        )
        
        print(f"✓ Loaded profile: {active_profile_name}")
        print(f"✓ Tool tracking enabled")
        print()
        
        # Launch TUI
        run_tui(
            config=config_data,
            session_id=None,  # New session
            profile=active_profile_name,
        )
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ TUI closed")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
