#!/usr/bin/env python
"""Quick test script for TUI implementation."""

import sys
from pathlib import Path

# Add the package to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    # Test imports
    print("Testing TUI imports...")
    from amplifier_app_cli.tui import AmplifierApp
    print("✓ TUI imports successful")
    
    # Test Textual is available
    from textual.app import App
    print("✓ Textual library available")
    
    # Test app initialization
    print("\nTesting TUI initialization...")
    app = AmplifierApp(
        config={"test": True},
        session_id="test-session",
        profile="test-profile"
    )
    print("✓ TUI app initialized successfully")
    
    print("\n✓ All Phase 1 tests passed!")
    print("\nTo launch the TUI, run:")
    print("  amplifier run --tui")
    print("  amplifier --tui")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("\nPlease run: uv sync")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
