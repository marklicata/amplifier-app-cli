# Amplifier Foundation Library - Implementation Guide

## Repository Structure

```
amplifier-foundation/
├── pyproject.toml
├── README.md
├── src/
│   └── amplifier_foundation/
│       ├── __init__.py              # Public API exports
│       ├── __version__.py
│       │
│       ├── paths.py                 # Path management
│       │
│       ├── config/
│       │   ├── __init__.py
│       │   ├── manager.py           # ConfigManager wrapper
│       │   ├── resolver.py          # Config resolution logic
│       │   ├── app_settings.py      # High-level settings helpers
│       │   └── summary.py           # Display summaries
│       │
│       ├── providers/
│       │   ├── __init__.py
│       │   ├── manager.py           # Provider lifecycle
│       │   ├── sources.py           # Canonical sources
│       │   ├── loader.py            # Provider discovery
│       │   └── config_utils.py      # Config wizards
│       │
│       ├── session/
│       │   ├── __init__.py
│       │   ├── store.py             # Persistence layer
│       │   ├── spawner.py           # Agent delegation
│       │   └── config.py            # Config merging
│       │
│       ├── modules/
│       │   ├── __init__.py
│       │   └── manager.py           # Module registration
│       │
│       ├── security/
│       │   ├── __init__.py
│       │   └── keys.py              # Key management
│       │
│       ├── project.py               # Project utilities
│       │
│       └── application.py           # High-level app API (optional)
│
├── tests/
│   ├── conftest.py
│   ├── test_paths.py
│   ├── test_config/
│   ├── test_providers/
│   ├── test_session/
│   └── ...
│
└── docs/
    ├── quickstart.md
    ├── configuration.md
    ├── providers.md
    ├── sessions.md
    └── api-reference.md
```

---

## Phase 1: Create Foundation Package

### Step 1.1: Repository Setup

```bash
# Create new repository
mkdir amplifier-foundation
cd amplifier-foundation
git init
uv init --lib

# Setup directory structure
mkdir -p src/amplifier_foundation/{config,providers,session,modules,security}
mkdir -p tests/{config,providers,session,modules,security}
mkdir -p docs
```

### Step 1.2: pyproject.toml

```toml
[project]
name = "amplifier-foundation"
version = "0.1.0"
description = "Common foundation for Amplifier AI applications"
readme = "README.md"
requires-python = ">=3.11"
license = "MIT"
authors = [
    { name = "Microsoft MADE:Explorations Team" }
]

dependencies = [
    "amplifier-core",
    "amplifier-config",
    "amplifier-module-resolution",
    "amplifier-collections",
    "amplifier-profiles",
    "pydantic>=2.0.0",
    "pyyaml>=6.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=4.0.0",
    "mypy>=1.8.0",
    "ruff>=0.1.0",
]

[tool.uv]
package = true

[tool.uv.sources]
amplifier-core = { git = "https://github.com/microsoft/amplifier-core", branch = "main" }
amplifier-config = { git = "https://github.com/microsoft/amplifier-config", branch = "main" }
amplifier-module-resolution = { git = "https://github.com/microsoft/amplifier-module-resolution", branch = "main" }
amplifier-collections = { git = "https://github.com/microsoft/amplifier-collections", branch = "main" }
amplifier-profiles = { git = "https://github.com/microsoft/amplifier-profiles", branch = "main" }

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "strict"
addopts = "--cov=amplifier_foundation --cov-report=html --cov-report=term"

[tool.ruff]
line-length = 120
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
```

### Step 1.3: Public API Design (`src/amplifier_foundation/__init__.py`)

```python
"""Amplifier Foundation - Common infrastructure for Amplifier applications.

This library provides the essential building blocks for building applications
on top of the Amplifier AI platform, abstracting the complexity of core
dependencies and providing a unified, ergonomic API.

Quick Start:
    >>> from amplifier_foundation import Application
    >>> 
    >>> app = Application()
    >>> session = await app.create_session(profile="default")
    >>> response = await session.execute("Your prompt here")

Advanced Usage:
    >>> from amplifier_foundation import (
    ...     create_config_manager,
    ...     create_provider_manager,
    ...     create_session_store,
    ... )
    >>> 
    >>> config = create_config_manager()
    >>> providers = create_provider_manager(config)
    >>> store = create_session_store()
"""

from __future__ import annotations

# Version
from .__version__ import __version__

# Core factories (most common use case)
from .paths import (
    create_agent_loader,
    create_collection_resolver,
    create_config_manager,
    create_module_resolver,
    create_profile_loader,
)

# Path management
from .paths import (
    ConfigPaths,
    get_agent_search_paths,
    get_cli_config_paths,
    get_collection_search_paths,
    get_profile_search_paths,
    get_workspace_dir,
    is_running_from_home,
    ScopeNotAvailableError,
)

# Configuration
from .config import (
    AppSettings,
    EffectiveConfigSummary,
    get_effective_config_summary,
    resolve_app_config,
)

# Providers
from .providers import (
    ProviderManager,
    ProviderInfo,
    ConfigureResult,
    install_known_providers,
    get_effective_provider_sources,
)

# Session management
from .session import (
    SessionStore,
    spawn_sub_session,
    resume_sub_session,
)

# Modules
from .modules import (
    ModuleManager,
    ModuleInfo,
)

# Security
from .security import KeyManager

# Project utilities
from .project import get_project_slug

# Optional: High-level application API
# from .application import Application

__all__ = [
    # Version
    "__version__",
    
    # Factories (primary API)
    "create_config_manager",
    "create_provider_manager",
    "create_profile_loader",
    "create_agent_loader",
    "create_collection_resolver",
    "create_module_resolver",
    
    # Path management
    "ConfigPaths",
    "get_cli_config_paths",
    "get_profile_search_paths",
    "get_agent_search_paths",
    "get_collection_search_paths",
    "get_workspace_dir",
    "is_running_from_home",
    "ScopeNotAvailableError",
    
    # Configuration
    "AppSettings",
    "resolve_app_config",
    "EffectiveConfigSummary",
    "get_effective_config_summary",
    
    # Providers
    "ProviderManager",
    "ProviderInfo",
    "ConfigureResult",
    "install_known_providers",
    "get_effective_provider_sources",
    
    # Sessions
    "SessionStore",
    "spawn_sub_session",
    "resume_sub_session",
    
    # Modules
    "ModuleManager",
    "ModuleInfo",
    
    # Security
    "KeyManager",
    
    # Project
    "get_project_slug",
    
    # High-level API
    # "Application",
]
```

---

## Phase 2: Migration Process

### Step 2.1: Extract Core Files

For each component, follow this pattern:

1. **Copy file from CLI to foundation**
2. **Update imports** to use absolute imports
3. **Add tests** for the component
4. **Update CLI** to import from foundation
5. **Remove original** from CLI
6. **Verify** CLI still works

#### Example: Extracting `paths.py`

```bash
# 1. Copy file
cp amplifier-app-cli/amplifier_app_cli/paths.py \
   amplifier-foundation/src/amplifier_foundation/paths.py

# 2. Update imports in foundation file
# Before:
from amplifier_collections import CollectionResolver
from .lib.mention_loading import MentionLoader

# After:
from amplifier_collections import CollectionResolver
# Note: MentionLoader might need extraction decision

# 3. Write tests
cat > amplifier-foundation/tests/test_paths.py << 'EOF'
import pytest
from pathlib import Path
from amplifier_foundation.paths import (
    get_cli_config_paths,
    create_config_manager,
    is_running_from_home,
)

def test_config_paths_structure():
    paths = get_cli_config_paths()
    assert paths.user is not None
    assert paths.user.name == "settings.yaml"

def test_running_from_home(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert not is_running_from_home()
    
    monkeypatch.chdir(Path.home())
    assert is_running_from_home()

def test_config_manager_factory():
    config = create_config_manager()
    assert config is not None
    assert hasattr(config, 'get_merged_settings')
EOF

# 4. Update CLI imports
# In amplifier-app-cli/amplifier_app_cli/commands/provider.py:
# Before:
from ..paths import create_config_manager

# After:
from amplifier_foundation import create_config_manager

# 5. Remove original (after verification)
# git rm amplifier-app-cli/amplifier_app_cli/paths.py
```

### Step 2.2: Handling Dependencies Between Files

Some files depend on each other. Extract in this order:

1. **Independent utilities first:**
   - `project_utils.py` (no deps)
   - `key_manager.py` (no deps)

2. **Core infrastructure:**
   - `paths.py` (depends on nothing in CLI)
   - `lib/app_settings/` (depends on paths)

3. **Managers (depend on infrastructure):**
   - `provider_sources.py` (depends on config)
   - `provider_manager.py` (depends on sources, app_settings)
   - `module_manager.py` (depends on config)
   - `session_store.py` (depends on project_utils)

4. **High-level features:**
   - `runtime/config.py` (depends on app_settings, profiles)
   - `effective_config.py` (depends on provider_loader)
   - `session_spawner.py` (depends on session_store, agent_config)

### Step 2.3: CLI Integration

Update CLI's `pyproject.toml`:

```toml
[project]
name = "amplifier-app-cli"
dependencies = [
    "click>=8.1.0",
    "rich>=13.0.0",
    "amplifier-foundation",  # New dependency
    "prompt-toolkit>=3.0.52",
    "textual>=0.50.0",
    # Remove: amplifier-core, amplifier-config, etc. (now via foundation)
]

[tool.uv.sources]
amplifier-foundation = { git = "https://github.com/microsoft/amplifier-foundation", branch = "main" }
# Or during development:
# amplifier-foundation = { path = "../amplifier-foundation", editable = true }
```

Update CLI imports globally:

```python
# Before:
from amplifier_config import ConfigManager
from .paths import create_config_manager, create_provider_manager
from .provider_manager import ProviderManager
from .session_store import SessionStore

# After:
from amplifier_foundation import (
    create_config_manager,
    create_provider_manager,
    ProviderManager,
    SessionStore,
)
```

---

## Phase 3: Testing Strategy

### Unit Tests (Foundation)

Each component should have comprehensive unit tests:

```python
# tests/test_providers/test_manager.py
import pytest
from amplifier_foundation.providers import ProviderManager
from amplifier_foundation import create_config_manager

@pytest.fixture
def provider_manager(tmp_path, monkeypatch):
    # Mock home directory
    monkeypatch.setenv("HOME", str(tmp_path))
    config = create_config_manager()
    return ProviderManager(config)

def test_use_provider(provider_manager):
    result = provider_manager.use_provider(
        provider_id="provider-anthropic",
        scope="global",
        config={"default_model": "claude-sonnet-4"},
    )
    assert result.provider == "provider-anthropic"
    assert result.scope == "global"

def test_get_current_provider(provider_manager):
    provider_manager.use_provider(
        provider_id="provider-openai",
        scope="global",
        config={"default_model": "gpt-4"},
    )
    current = provider_manager.get_current_provider()
    assert current is not None
    assert current.module_id == "provider-openai"
```

### Integration Tests (CLI with Foundation)

Ensure CLI still works with foundation:

```python
# amplifier-app-cli/tests/test_integration/test_foundation.py
import pytest
from click.testing import CliRunner
from amplifier_app_cli.main import cli

def test_provider_use_via_foundation():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            'provider', 'use', 'anthropic',
            '--api-key', 'test-key',
            '--model', 'claude-sonnet-4'
        ])
        assert result.exit_code == 0
        assert "Configured provider-anthropic" in result.output

def test_session_persistence():
    # Verify session store from foundation works
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create session
        result = runner.invoke(cli, ['run', 'test prompt'])
        assert result.exit_code == 0
        
        # List sessions
        result = runner.invoke(cli, ['session', 'list'])
        assert result.exit_code == 0
        assert 'test prompt' in result.output or 'messages' in result.output
```

### Regression Tests

Create a test suite that runs both old and new implementations:

```bash
# Run old CLI tests
cd amplifier-app-cli
uv run pytest

# Run new foundation tests
cd ../amplifier-foundation
uv run pytest

# Run integration tests
cd ../amplifier-app-cli
uv run pytest tests/test_integration/
```

---

## Phase 4: Documentation

### Foundation README.md

```markdown
# Amplifier Foundation

Common infrastructure for building applications on the Amplifier AI platform.

## Installation

```bash
pip install amplifier-foundation
# or
uv pip install amplifier-foundation
```

## Quick Start

```python
from amplifier_foundation import Application

app = Application()
session = await app.create_session(profile="default")
response = await session.execute("Write a Python function to calculate fibonacci")
print(response)
```

## Core Concepts

### Configuration Management
- 3-scope system (local, project, global)
- YAML-based settings
- Environment variable expansion

### Provider Management
- Use/list/reset providers
- Priority-based selection
- Local and git-based sources

### Session Management
- Persistent sessions
- Agent delegation
- Multi-turn conversations

See [documentation](./docs/) for detailed guides.
```

### API Documentation

Generate from docstrings:

```bash
# Use sphinx, mkdocs, or similar
cd amplifier-foundation
pip install sphinx sphinx-rtd-theme
sphinx-quickstart docs
sphinx-apidoc -o docs/api src/amplifier_foundation
```

---

## Phase 5: Validation Checklist

Before calling migration complete:

### Functionality Checklist

- [ ] All CLI commands work identically
- [ ] Configuration resolution unchanged
- [ ] Provider management works (use/list/reset)
- [ ] Session persistence works
- [ ] Agent delegation works
- [ ] Module management works
- [ ] Profile/collection loading works
- [ ] API keys stored securely
- [ ] Scope validation works
- [ ] Path factories work in all scenarios

### Code Quality Checklist

- [ ] All files have type hints
- [ ] All functions have docstrings
- [ ] Tests cover >90% of foundation code
- [ ] No circular imports
- [ ] Ruff/mypy pass with no errors
- [ ] Performance is equivalent or better

### Documentation Checklist

- [ ] README with quick start
- [ ] API reference generated
- [ ] Migration guide for CLI developers
- [ ] Tutorial for building new apps
- [ ] Troubleshooting guide

### Integration Checklist

- [ ] CLI uses only public foundation APIs
- [ ] No direct imports of amplifier-core in CLI
- [ ] Foundation tests pass in isolation
- [ ] CLI tests pass with foundation
- [ ] Can build a minimal app in <100 LOC

---

## Example: Minimal App Using Foundation

Goal: Validate foundation API is ergonomic

```python
# minimal_app.py - A 50-line Amplifier app
import asyncio
from amplifier_foundation import (
    Application,
    create_provider_manager,
    ProviderManager,
)

async def main():
    # Setup provider if needed
    providers = create_provider_manager()
    if not providers.get_current_provider():
        print("No provider configured. Let's set one up:")
        api_key = input("Anthropic API key: ")
        providers.use_provider(
            provider_id="provider-anthropic",
            scope="global",
            config={
                "api_key": api_key,
                "default_model": "claude-sonnet-4",
            }
        )
        print("✓ Provider configured\n")
    
    # Create application
    app = Application()
    
    # Interactive loop
    print("Minimal Amplifier App (type 'exit' to quit)\n")
    while True:
        prompt = input("You: ").strip()
        if not prompt or prompt.lower() == 'exit':
            break
        
        session = await app.create_session(profile="default")
        response = await session.execute(prompt)
        print(f"AI: {response}\n")
        await session.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

**Success criteria:** This should work out of the box with `uv run minimal_app.py`

---

## Rollout Plan

### Week 1-2: Setup & Core Extraction
- Create repository
- Extract paths, config, app_settings
- Write tests for extracted code
- Document core APIs

### Week 3-4: Provider & Module Management
- Extract provider management
- Extract module management
- Integrate key management
- Write tests and docs

### Week 5-6: Session Management
- Extract session store
- Extract session spawner
- Write tests for persistence
- Document session APIs

### Week 7-8: CLI Integration
- Update CLI to use foundation
- Remove duplicate code
- Run full test suite
- Update CLI documentation

### Week 9-10: Validation & Polish
- Build example applications
- Write tutorials
- API refinement based on feedback
- Performance testing

### Week 11-12: Release
- Final documentation pass
- Publish to PyPI
- Announce to community
- Monitor for issues

---

## Success Metrics

**Quantitative:**
- CLI codebase reduced by 40-60%
- Foundation test coverage >90%
- Can build working app in <100 LOC
- Zero breaking changes to CLI UX
- Foundation package <500KB

**Qualitative:**
- Foundation docs enable app building without reading CLI code
- Second app (GUI) built with foundation validates API
- Community feedback is positive
- Code is maintainable (new contributors can understand it)

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking CLI during migration | High | Comprehensive test suite, incremental migration |
| Foundation API too complex | Medium | User testing with minimal app example |
| Performance regression | Medium | Benchmark before/after, optimize hot paths |
| Import cycles | Low | Careful dependency ordering, use factories |
| Documentation gap | Medium | Write docs alongside code, not after |

---

## Next Actions

1. **Get approval** on overall approach
2. **Create foundation repo** with basic structure
3. **Start with paths.py** extraction (smallest, most isolated)
4. **Write first integration test** before extracting more
5. **Iterate rapidly** with feedback loops

---

*This is a living document. Update as implementation progresses.*
