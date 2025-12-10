"""Mention utilities - Re-export from amplifier_foundation.

This module is maintained for backward compatibility.
All new code should import from amplifier_foundation directly.
"""

from amplifier_foundation.mention_loading.utils import (
    extract_mention_path,
    has_mentions,
    parse_home_directory_mentions,
    parse_mentions,
)

__all__ = [
    "parse_mentions",
    "has_mentions",
    "extract_mention_path",
    "parse_home_directory_mentions",
]
