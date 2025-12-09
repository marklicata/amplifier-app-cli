#!/usr/bin/env python
"""Move test files to test/TUI/ directory."""
import os
import shutil

# Create directory
os.makedirs('test/TUI', exist_ok=True)
print("✓ Created test/TUI directory")

# Move files
files = ['test_chat_screen.py', 'test_review_screen.py', 'test_tui.py']
for filename in files:
    if os.path.exists(filename):
        shutil.move(filename, f'test/TUI/{filename}')
        print(f"✓ Moved {filename} to test/TUI/")
    else:
        print(f"✗ {filename} not found")

# Verify
print("\nFiles in test/TUI/:")
for f in os.listdir('test/TUI'):
    print(f"  - {f}")

print("\nTest files remaining in root:")
remaining = [f for f in os.listdir('.') if f.startswith('test_') and f.endswith('.py')]
if remaining:
    for f in remaining:
        print(f"  - {f}")
else:
    print("  None (all moved successfully)")
