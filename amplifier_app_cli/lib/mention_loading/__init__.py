"""Mention loading - Re-export from amplifier_app_utils.

This module is maintained for backward compatibility.
All new code should import from amplifier_app_utils directly.
"""

from amplifier_app_utils.mention_loading import (
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
