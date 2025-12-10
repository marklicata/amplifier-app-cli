"""Path management - Re-export from amplifier_app_utils.

This module is maintained for backward compatibility.
All new code should import from amplifier_app_utils directly.
"""

from amplifier_app_utils.paths import PathManager

# Maintain backward compatibility
__all__ = ["PathManager"]
