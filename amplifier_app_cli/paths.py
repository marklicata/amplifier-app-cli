"""CLI-specific path policy (now wraps amplifier-foundation).

This module maintains backward compatibility by wrapping the PathManager
from amplifier-foundation and providing CLI-specific factory functions.
"""

from pathlib import Path
from typing import TYPE_CHECKING
from typing import Literal

from amplifier_collections import CollectionResolver
from amplifier_config import ConfigManager
from amplifier_config import ConfigPaths
from amplifier_config import Scope
from amplifier_foundation import PathManager as FoundationPathManager
from amplifier_foundation import ScopeNotAvailableError
from amplifier_foundation import ScopeType
from amplifier_foundation import get_effective_scope
from amplifier_foundation import validate_scope_for_write
from amplifier_module_resolution import StandardModuleSourceResolver
from amplifier_profiles import ProfileLoader

if TYPE_CHECKING:
    from amplifier_profiles import AgentLoader

# Re-export foundation types
__all__ = [
    "ScopeType",
    "ScopeNotAvailableError",
    "validate_scope_for_write",
    "get_effective_scope",
    "get_cli_config_paths",
    "is_running_from_home",
    "get_collection_search_paths",
    "get_collection_lock_path",
    "get_profile_search_paths",
    "get_workspace_dir",
    "create_config_manager",
    "create_collection_resolver",
    "create_profile_loader",
    "get_agent_search_paths",
    "create_agent_loader",
    "create_module_resolver",
]

# Create CLI-specific path manager with bundled data
_cli_package_dir = Path(__file__).parent
_cli_path_manager = FoundationPathManager(
    bundled_dir=_cli_package_dir / "data",
    app_name="amplifier"
)


# ===== CONFIG PATHS =====


def get_cli_config_paths() -> ConfigPaths:
    """Get CLI-specific configuration paths.

    Returns:
        ConfigPaths with CLI conventions
    """
    return _cli_path_manager.get_config_paths()


def is_running_from_home() -> bool:
    """Check if running from the home directory.

    Returns:
        True if cwd is the user's home directory
    """
    return _cli_path_manager.is_running_from_home()


# ===== COLLECTION PATHS =====


def get_collection_search_paths() -> list[Path]:
    """Get CLI-specific collection search paths.

    Returns:
        List of paths to search for collections
    """
    return _cli_path_manager.get_collection_search_paths()


def get_collection_lock_path(local: bool = False) -> Path:
    """Get CLI-specific collection lock path.

    Args:
        local: If True, use project lock; if False, use user lock

    Returns:
        Path to collection lock file
    """
    return _cli_path_manager.get_collection_lock_path(local)


# ===== PROFILE PATHS =====


def get_profile_search_paths() -> list[Path]:
    """Get CLI-specific profile search paths.

    Returns:
        List of paths to search for profiles
    """
    return _cli_path_manager.get_profile_search_paths()


# ===== MODULE RESOLUTION PATHS =====


def get_workspace_dir() -> Path:
    """Get CLI-specific workspace directory for local modules.

    Returns:
        Path to workspace directory (.amplifier/modules/)
    """
    return _cli_path_manager.get_workspace_dir()


# ===== DEPENDENCY FACTORIES =====


def create_config_manager() -> ConfigManager:
    """Create CLI-configured config manager.

    Returns:
        ConfigManager with CLI path policy injected
    """
    return _cli_path_manager.create_config_manager()


def create_collection_resolver() -> CollectionResolver:
    """Create CLI-configured collection resolver.

    Returns:
        CollectionResolver with CLI search paths and source provider injected
    """
    return _cli_path_manager.create_collection_resolver()


def create_profile_loader(
    collection_resolver: CollectionResolver | None = None,
) -> ProfileLoader:
    """Create CLI-configured profile loader.

    Args:
        collection_resolver: Optional collection resolver

    Returns:
        ProfileLoader with CLI paths and protocols injected
    """
    return _cli_path_manager.create_profile_loader(collection_resolver)


def get_agent_search_paths() -> list[Path]:
    """Get CLI-specific agent search paths.

    Returns:
        List of paths to search for agents
    """
    return _cli_path_manager.get_agent_search_paths()


def create_agent_loader(
    collection_resolver: CollectionResolver | None = None,
) -> "AgentLoader":
    """Create CLI-configured agent loader.

    Args:
        collection_resolver: Optional collection resolver

    Returns:
        AgentLoader with CLI paths and protocols injected
    """
    return _cli_path_manager.create_agent_loader(collection_resolver)


def create_module_resolver() -> StandardModuleSourceResolver:
    """Create CLI-configured module resolver.

    Returns:
        StandardModuleSourceResolver with CLI providers injected
    """
    return _cli_path_manager.create_module_resolver()
