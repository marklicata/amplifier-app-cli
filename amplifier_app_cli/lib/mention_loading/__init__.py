"""Mention loading library for Amplifier (wraps foundation).

This module re-exports functionality from amplifier-foundation for backward compatibility.
"""

from amplifier_foundation.mention_loading import (
    ContentDeduplicator,
    ContextFile,
    MentionLoader,
    MentionResolver,
)

__all__ = ["MentionLoader", "MentionResolver", "ContentDeduplicator", "ContextFile"]
