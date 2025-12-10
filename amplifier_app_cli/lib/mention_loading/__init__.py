"""Mention loading - Re-export from amplifier_foundation.

This module is maintained for backward compatibility.
All new code should import from amplifier_foundation directly.
"""

from amplifier_foundation.mention_loading import (
    ContentDeduplicator,
    MentionLoader,
    MentionMetadata,
    MentionResolver,
)

__all__ = [
    "MentionMetadata",
    "MentionResolver",
    "MentionLoader",
    "ContentDeduplicator",
]
