"""Update CLI imports to use amplifier_foundation."""

import re
from pathlib import Path

# Mapping of old imports to new imports
IMPORT_REPLACEMENTS = {
    # Provider management
    r"from \.\.provider_manager import": "from amplifier_foundation import",
    r"from \.provider_manager import": "from amplifier_foundation import",
    r"from \.\.\.provider_manager import": "from amplifier_foundation import",
    
    # Session management
    r"from \.\.session_store import": "from amplifier_foundation import",
    r"from \.session_store import": "from amplifier_foundation import",
    r"from \.\.\.session_store import": "from amplifier_foundation import",
    
    # Key management
    r"from \.\.key_manager import": "from amplifier_foundation import",
    r"from \.key_manager import": "from amplifier_foundation import",
    r"from \.\.\.key_manager import": "from amplifier_foundation import",
    
    # Module management
    r"from \.\.module_manager import": "from amplifier_foundation import",
    r"from \.module_manager import": "from amplifier_foundation import",
    
    # Provider sources
    r"from \.\.provider_sources import": "from amplifier_foundation.provider_sources import",
    r"from \.provider_sources import": "from amplifier_foundation.provider_sources import",
    
    # Effective config
    r"from \.\.effective_config import": "from amplifier_foundation.effective_config import",
    r"from \.effective_config import": "from amplifier_foundation.effective_config import",
    
    # Project utils
    r"from \.\.project_utils import": "from amplifier_foundation.project_utils import",
    r"from \.project_utils import": "from amplifier_foundation.project_utils import",
    
    # Session spawner
    r"from \.\.session_spawner import": "from amplifier_foundation.session_spawner import",
    r"from \.session_spawner import": "from amplifier_foundation.session_spawner import",
}


def update_file(file_path: Path) -> bool:
    """Update imports in a single file. Returns True if modified."""
    try:
        content = file_path.read_text(encoding="utf-8")
        original_content = content
        
        # Apply all replacements
        for old_pattern, new_import in IMPORT_REPLACEMENTS.items():
            content = re.sub(old_pattern, new_import, content)
        
        # Write back if changed
        if content != original_content:
            file_path.write_text(content, encoding="utf-8")
            print(f"Updated: {file_path.name}")
            return True
        return False
    except Exception as e:
        print(f"Error updating {file_path.name}: {e}")
        return False


def main():
    """Update all Python files in the CLI."""
    cli_dir = Path("amplifier_app_cli")
    
    if not cli_dir.exists():
        print("Error: amplifier_app_cli directory not found")
        return
    
    # Find all Python files
    py_files = list(cli_dir.rglob("*.py"))
    
    print(f"Scanning {len(py_files)} Python files...")
    print()
    
    updated_count = 0
    for py_file in py_files:
        if update_file(py_file):
            updated_count += 1
    
    print()
    print(f"Updated {updated_count}/{len(py_files)} files")


if __name__ == "__main__":
    main()
