# Amplifier Foundation Library - Extraction Proposal

## Executive Summary

This document proposes extracting a common foundation library from `amplifier-app-cli` that manages the complexity of the core amplifier dependencies and provides a unified interface for building end-user applications.

**Target Dependencies to Abstract:**
- amplifier-core
- amplifier-config  
- amplifier-module-resolution
- amplifier-collections
- amplifier-profiles

**Proposed Library Name:** `amplifier-foundation` (or `amplifier-app-foundation`)

## Architecture Vision

```
┌─────────────────────────────────────────┐
│   End-User Applications (CLI, GUI, etc) │
│   - UI/UX specific code                 │
│   - Command implementations             │
│   - Display systems                     │
└──────────────┬──────────────────────────┘
               │ depends on
               ▼
┌─────────────────────────────────────────┐
│      amplifier-foundation               │
│   - Session management                  │
│   - Configuration resolution            │
│   - Provider management                 │
│   - Module/collection/profile loading   │
│   - Common utilities                    │
└──────────────┬──────────────────────────┘
               │ orchestrates
               ▼
┌─────────────────────────────────────────┐
│  Core Dependencies (abstracted away)    │
│  - amplifier-core                       │
│  - amplifier-config                     │
│  - amplifier-module-resolution          │
│  - amplifier-collections                │
│  - amplifier-profiles                   │
└─────────────────────────────────────────┘
```

## Components to Extract

### 1. **Path Management & Configuration Resolution** ⭐ HIGH PRIORITY
**Files:** `paths.py`, `runtime/config.py`, `lib/app_settings/`

**Why:** Every app needs consistent path conventions and configuration resolution.

**Extract As:**
- `amplifier_foundation.paths` - Path policy and factory functions
- `amplifier_foundation.config` - Configuration resolution and assembly
- `amplifier_foundation.app_settings` - High-level settings helpers

**Key Capabilities:**
- Standard directory structure (`~/.amplifier/`, `.amplifier/`)
- 3-scope configuration (local/project/global)
- Config path factories with proper precedence
- Environment variable expansion
- Scope validation and fallback handling

---

### 2. **Provider Management** ⭐ HIGH PRIORITY
**Files:** `provider_manager.py`, `provider_sources.py`, `provider_config_utils.py`, `provider_loader.py`

**Why:** Provider configuration is central to any amplifier app.

**Extract As:**
- `amplifier_foundation.providers.manager` - Provider lifecycle
- `amplifier_foundation.providers.sources` - Canonical provider sources
- `amplifier_foundation.providers.loader` - Provider discovery

**Key Capabilities:**
- Provider use/list/reset operations
- Priority-based provider selection
- Provider source resolution (git + local paths)
- Integration with config system
- Known provider installation

---

### 3. **Session Management** ⭐ HIGH PRIORITY
**Files:** `session_store.py`, `session_spawner.py`, `agent_config.py`

**Why:** Session persistence and agent delegation are common patterns.

**Extract As:**
- `amplifier_foundation.session.store` - Session persistence
- `amplifier_foundation.session.spawner` - Agent delegation
- `amplifier_foundation.session.config` - Config merging utilities

**Key Capabilities:**
- Atomic session save/load with backup
- Project-scoped session storage
- Sub-session spawning with W3C trace IDs
- Multi-turn resumption
- Session cleanup utilities

---

### 4. **Module Management** 
**Files:** `module_manager.py`

**Why:** Module registration across scopes is common.

**Extract As:**
- `amplifier_foundation.modules.manager` - Module lifecycle

**Key Capabilities:**
- Add/remove modules at scopes
- List current modules
- Module type handling (tools/hooks/agents/providers)

---

### 5. **Core Utilities**
**Files:** `key_manager.py`, `project_utils.py`, `effective_config.py`

**Why:** Shared infrastructure needed by all apps.

**Extract As:**
- `amplifier_foundation.security.keys` - API key management
- `amplifier_foundation.project` - Project detection
- `amplifier_foundation.config.summary` - Config display helpers

**Key Capabilities:**
- Secure key storage (`~/.amplifier/keys.env`)
- Project slug generation
- Effective config summarization

---

### 6. **Context Loading System** (Optional - discuss timing)
**Files:** `lib/mention_loading/`

**Why:** @mention system is powerful and reusable.

**Extract As:**
- `amplifier_foundation.context.mentions` (or keep in separate lib)

**Key Capabilities:**
- @mention path resolution
- Content deduplication
- Profile/agent mention loading

**Note:** This may deserve its own library (`amplifier-mentions` or stay in profiles).

---

## What Stays in CLI

The CLI should become a thin application layer that provides:

1. **CLI-Specific Concerns:**
   - Click command definitions (`commands/`)
   - Rich/Textual UI components (`ui/`, `tui/`, `console.py`)
   - Interactive mode REPL (`main.py` interactive loop)
   - Banner art and CLI branding (`banners/`)
   - Approval provider implementation (CLI-specific UX)

2. **CLI Entry Points:**
   - `main.py` - Command dispatcher
   - `__main__.py` - Entry point
   - Command implementations that call foundation APIs

3. **Bundled Data:**
   - `data/collections/` - Default collections
   - `data/profiles/` - Default profiles
   - `data/context/` - Bundled context files

---

## Dependency Injection Pattern

The foundation library should provide factory functions that apps can customize:

```python
# Foundation provides factories with sensible defaults
from amplifier_foundation import (
    create_config_manager,
    create_profile_loader,
    create_session_store,
    create_provider_manager,
)

# Apps can use as-is or customize
config = create_config_manager()
profiles = create_profile_loader(config)
sessions = create_session_store()
providers = create_provider_manager(config)
```

Apps can override path policies if needed:

```python
# Custom path policy for specialized app
from amplifier_foundation.paths import ConfigPaths

custom_paths = ConfigPaths(
    user=Path("/custom/location/settings.yaml"),
    project=Path(".myapp/config.yaml"),
    local=None  # Disable local scope
)

config = create_config_manager(paths=custom_paths)
```

---

## Migration Strategy

### Phase 1: Create Foundation Package
1. Create new repo: `amplifier-foundation`
2. Copy identified files maintaining structure
3. Update imports to `amplifier_foundation.*`
4. Add proper `pyproject.toml` with dependencies
5. Write comprehensive tests

### Phase 2: Update CLI to Use Foundation
1. Add `amplifier-foundation` as dependency
2. Replace copied code with imports
3. Test thoroughly (should be drop-in replacement)
4. Remove duplicate code from CLI
5. Update documentation

### Phase 3: Dogfood & Iterate
1. Use in CLI (reference implementation)
2. Build 1-2 other apps (GUI, web API) to validate API
3. Gather feedback and refine
4. Stabilize API for 1.0 release

### Phase 4: Publish
1. Document foundation library thoroughly
2. Publish to PyPI
3. Update other apps to use published version
4. Announce to community

---

## API Design Principles

Following your preferences (Python, TypeScript, readable, performant):

1. **High-Level, Batteries-Included API**
   ```python
   # Simple case: sensible defaults
   from amplifier_foundation import Application
   
   app = Application()
   session = await app.create_session(profile="dev")
   response = await session.execute("Your prompt")
   ```

2. **Composable, Explicit When Needed**
   ```python
   # Advanced case: explicit control
   from amplifier_foundation import (
       create_config_manager,
       create_provider_manager,
       SessionStore,
   )
   
   config = create_config_manager()
   providers = create_provider_manager(config)
   providers.use_provider("provider-anthropic", scope="global", ...)
   
   store = SessionStore(base_dir=custom_path)
   ```

3. **Readable, Performant Code**
   - Type hints everywhere
   - Concise, focused docstrings
   - Performance-critical paths optimized
   - Lazy loading where appropriate
   - Async-first for I/O operations

---

## Example Usage (CLI Commands)

**Before (CLI does everything):**
```python
# commands/provider.py (simplified)
@click.command()
def provider_use(name: str):
    config = ConfigManager(paths=get_cli_config_paths())
    provider_info = get_provider_info(name)
    # ... 50 more lines of logic
```

**After (Foundation does heavy lifting):**
```python
# commands/provider.py (simplified)
from amplifier_foundation import create_provider_manager

@click.command()
def provider_use(name: str):
    manager = create_provider_manager()
    result = manager.use_provider(name, scope="global")
    console.print(f"✓ Configured {result.provider}")
```

---

## Open Questions for Discussion

1. **Naming:** `amplifier-foundation` vs `amplifier-app-foundation` vs other?

2. **Context Loading:** Keep @mention system in foundation, profiles, or separate lib?

3. **Display System Protocol:** Should foundation define display/approval system protocols, or leave entirely to apps?

4. **Async vs Sync:** Should we provide both sync and async APIs, or async-only?

5. **Configuration Format:** Standardize on current YAML format or allow flexibility?

6. **Module Discovery:** How much entry point discovery logic should be in foundation vs apps?

---

## Benefits

### For End Users
- **Consistency:** All amplifier apps feel familiar
- **Better Docs:** Single place to learn core concepts
- **Faster Apps:** Reusable code = more time for features

### For Developers
- **Lower Barrier:** Build amplifier apps without mastering all dependencies
- **Focus on UX:** Spend time on what makes your app unique
- **Battle-Tested:** Foundation handles edge cases (scope validation, atomic writes, etc.)

### For Ecosystem
- **Standards:** Common patterns across implementations
- **Innovation:** Easier to experiment with new app types
- **Quality:** Shared code gets more testing and refinement

---

## Next Steps

1. **Review & Discuss:** Team reviews this proposal
2. **Refine Scope:** Decide what goes in v1.0
3. **Create Repo:** Set up `amplifier-foundation` repository
4. **Extract Code:** Begin migration following Phase 1
5. **Test Integration:** Update CLI to use foundation
6. **Build Second App:** Validate API with different use case (GUI or API)

---

## Appendix: File Mapping

### High Priority Extractions
| Current Location | Foundation Location | Priority |
|-----------------|---------------------|----------|
| `paths.py` | `amplifier_foundation/paths.py` | ⭐ Critical |
| `runtime/config.py` | `amplifier_foundation/config/resolver.py` | ⭐ Critical |
| `lib/app_settings/` | `amplifier_foundation/config/app_settings.py` | ⭐ Critical |
| `provider_manager.py` | `amplifier_foundation/providers/manager.py` | ⭐ Critical |
| `provider_sources.py` | `amplifier_foundation/providers/sources.py` | ⭐ Critical |
| `session_store.py` | `amplifier_foundation/session/store.py` | ⭐ Critical |
| `session_spawner.py` | `amplifier_foundation/session/spawner.py` | ⭐ Critical |

### Medium Priority Extractions
| Current Location | Foundation Location | Priority |
|-----------------|---------------------|----------|
| `module_manager.py` | `amplifier_foundation/modules/manager.py` | Medium |
| `key_manager.py` | `amplifier_foundation/security/keys.py` | Medium |
| `project_utils.py` | `amplifier_foundation/project.py` | Medium |
| `effective_config.py` | `amplifier_foundation/config/summary.py` | Medium |
| `agent_config.py` | `amplifier_foundation/session/config.py` | Medium |

### Lower Priority / TBD
| Current Location | Foundation Location | Priority |
|-----------------|---------------------|----------|
| `lib/mention_loading/` | `amplifier_foundation/context/mentions/` or separate | TBD |
| `provider_loader.py` | `amplifier_foundation/providers/loader.py` | Low |
| `provider_config_utils.py` | `amplifier_foundation/providers/utils.py` | Low |
| `trace_collector.py` | `amplifier_foundation/observability/` | Low |

---

## Success Criteria

Foundation library is successful when:

1. ✅ CLI codebase shrinks by ~40-60% (UI/commands only)
2. ✅ Can build a GUI app in < 500 lines using foundation
3. ✅ New apps don't need to import amplifier-core directly
4. ✅ Configuration system "just works" with sensible defaults
5. ✅ Session management is < 20 lines for basic use case
6. ✅ Zero breaking changes to CLI user experience
7. ✅ Foundation has comprehensive test coverage (>90%)
8. ✅ Foundation docs enable building apps without reading CLI code

---

*Prepared by: Amplifier Architecture Analysis*
*Date: 2024*
*Status: PROPOSAL - Awaiting Review*
