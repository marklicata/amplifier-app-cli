"""Path management - Re-export from amplifier_foundation.

This module is maintained for backward compatibility.
All new code should import from amplifier_foundation directly.
"""

from amplifier_foundation.paths import PathManager

# Maintain backward compatibility
__all__ = ["PathManager"]
