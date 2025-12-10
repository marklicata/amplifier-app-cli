"""Pure text processing for @mentions (wraps foundation).

This module re-exports functionality from amplifier-foundation for backward compatibility.
"""

from amplifier_foundation.mention_loading.utils import (
    HOME_PATTERN,
    MENTION_PATTERN,
    extract_mention_path,
    extract_mention_type,
    has_mentions,
    parse_mentions,
)

__all__ = [
    "MENTION_PATTERN",
    "HOME_PATTERN",
    "parse_mentions",
    "has_mentions",
    "extract_mention_path",
    "extract_mention_type",
]
