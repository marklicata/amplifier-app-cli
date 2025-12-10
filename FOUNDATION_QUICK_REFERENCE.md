# Amplifier Foundation - Quick Reference

## 🎯 Goal

Extract reusable foundation from `amplifier-app-cli` that all amplifier apps can build on.

## 📦 What Gets Extracted

### ⭐ Critical (Phase 1)
```
✅ paths.py                    → amplifier_foundation/paths.py
✅ runtime/config.py           → amplifier_foundation/config/resolver.py
✅ lib/app_settings/           → amplifier_foundation/config/app_settings.py
✅ provider_manager.py         → amplifier_foundation/providers/manager.py
✅ provider_sources.py         → amplifier_foundation/providers/sources.py
✅ session_store.py            → amplifier_foundation/session/store.py
✅ session_spawner.py          → amplifier_foundation/session/spawner.py
```

### 🔧 Important (Phase 2)
```
module_manager.py              → amplifier_foundation/modules/manager.py
key_manager.py                 → amplifier_foundation/security/keys.py
project_utils.py               → amplifier_foundation/project.py
effective_config.py            → amplifier_foundation/config/summary.py
agent_config.py                → amplifier_foundation/session/config.py
```

### 🤔 Maybe Later (Phase 3)
```
lib/mention_loading/           → TBD (separate lib or in profiles?)
provider_loader.py             → amplifier_foundation/providers/loader.py
trace_collector.py             → amplifier_foundation/observability/
```

## 🚫 What Stays in CLI

```
✋ commands/                   # CLI command implementations
✋ ui/, tui/, console.py       # Rich/Textual UI components
✋ main.py                     # Interactive REPL loop
✋ banners/                    # CLI branding
✋ data/                       # Bundled collections/profiles
✋ approval_provider.py        # CLI-specific UX
```

## 📊 Architecture Layers

```
┌─────────────────────────────────────────┐
│         End-User Applications            │ ← CLI, GUI, Web API
│  - Commands, UI/UX, display systems     │
├─────────────────────────────────────────┤
│      amplifier-foundation                │ ← New extraction
│  - Config resolution                     │
│  - Provider management                   │
│  - Session persistence                   │
│  - Module/profile/collection loading     │
├─────────────────────────────────────────┤
│      Core Dependencies                   │ ← Abstracted away
│  - amplifier-core                        │
│  - amplifier-config                      │
│  - amplifier-module-resolution           │
│  - amplifier-collections                 │
│  - amplifier-profiles                    │
└─────────────────────────────────────────┘
```

## 🔑 Key Interfaces

### Create & Use Pattern

```python
# Factory functions - simple, high-level
from amplifier_foundation import (
    create_config_manager,
    create_provider_manager,
    create_session_store,
)

config = create_config_manager()
providers = create_provider_manager(config)
store = create_session_store()
```

### Manager Pattern

```python
# Manager classes - explicit, powerful
from amplifier_foundation import ProviderManager

manager = ProviderManager(config)
result = manager.use_provider("provider-anthropic", scope="global", config={...})
current = manager.get_current_provider()
providers = manager.list_providers()
```

### Optional High-Level API

```python
# Application class - batteries included
from amplifier_foundation import Application

app = Application()
session = await app.create_session(profile="default")
response = await session.execute("Your prompt")
```

## 🔄 Migration Flow

```
1. Create foundation repo
   └─> Setup structure, pyproject.toml, tests/

2. Extract each component
   ├─> Copy file to foundation
   ├─> Update imports (absolute paths)
   ├─> Write tests
   ├─> Update CLI to import from foundation
   └─> Verify CLI still works

3. Iterate on API
   └─> Build example apps, gather feedback

4. Publish
   └─> PyPI, documentation, announcement
```

## 📏 Success Criteria

| Metric | Target |
|--------|--------|
| CLI LOC reduction | 40-60% |
| Foundation test coverage | >90% |
| Minimal app LOC | <100 |
| Breaking changes to CLI UX | 0 |
| Time to build new app | <1 day |

## 🎓 Example: Before & After

### Before (CLI does everything)

```python
# amplifier-app-cli/amplifier_app_cli/commands/provider.py
from amplifier_config import ConfigManager
from ..paths import get_cli_config_paths, create_module_resolver
from ..provider_manager import ProviderManager
from ..provider_sources import get_effective_provider_sources

@click.command()
def use(provider: str):
    paths = get_cli_config_paths()
    config = ConfigManager(paths=paths)
    manager = ProviderManager(config)
    sources = get_effective_provider_sources(config)
    # ... 20 more lines
```

### After (Foundation abstracts complexity)

```python
# amplifier-app-cli/amplifier_app_cli/commands/provider.py
from amplifier_foundation import create_provider_manager

@click.command()
def use(provider: str):
    manager = create_provider_manager()
    result = manager.use_provider(provider, scope="global", ...)
    console.print(f"✓ Configured {result.provider}")
```

## 🎯 API Design Goals

1. **High-level by default** - Simple things should be simple
2. **Explicit when needed** - Complex things should be possible
3. **Type-safe** - Type hints everywhere
4. **Async-first** - For I/O operations
5. **Testable** - Easy to mock and test
6. **Documented** - Every public API has docstring

## 📚 Documentation Structure

```
amplifier-foundation/
└── docs/
    ├── quickstart.md              # 5-minute tutorial
    ├── concepts.md                # Core concepts
    ├── configuration.md           # Config system deep dive
    ├── providers.md               # Provider management
    ├── sessions.md                # Session persistence
    ├── building-apps.md           # Tutorial: build an app
    ├── api-reference/             # Auto-generated
    └── migration-guide.md         # For existing CLI devs
```

## ⚡ Performance Targets

| Operation | Target |
|-----------|--------|
| Config load | <10ms |
| Provider list | <50ms |
| Session load | <20ms |
| Session save | <30ms |
| Module resolve | <100ms (first), <5ms (cached) |

## 🧪 Testing Strategy

```
Unit Tests (Foundation)
├─> Test each component in isolation
├─> Mock external dependencies
└─> Cover edge cases

Integration Tests (CLI + Foundation)
├─> End-to-end command tests
├─> Verify no breaking changes
└─> Test real-world scenarios

Regression Tests
├─> Compare old vs new behavior
└─> Performance benchmarks
```

## 🚀 Rollout Timeline

| Week | Milestone |
|------|-----------|
| 1-2  | Setup, extract core (paths, config) |
| 3-4  | Extract providers, modules |
| 5-6  | Extract session management |
| 7-8  | CLI integration, remove duplicates |
| 9-10 | Validation, example apps |
| 11-12| Documentation, release |

## ✅ Pre-Merge Checklist

- [ ] All CLI tests pass
- [ ] Foundation tests pass (>90% coverage)
- [ ] Minimal app example works
- [ ] API documentation complete
- [ ] Migration guide written
- [ ] Performance benchmarks pass
- [ ] No regressions in CLI behavior
- [ ] Code review approved

## 🎉 Expected Benefits

### For End Users
- Consistent experience across amplifier apps
- Better documentation (single source of truth)
- Faster development of new features

### For Developers
- Lower barrier to building amplifier apps
- Focus on UX, not infrastructure
- Reusable, battle-tested code

### For Ecosystem
- Common patterns and standards
- Easier experimentation
- Higher quality through shared maintenance

## 📞 Questions to Resolve

1. **Naming:** `amplifier-foundation` or `amplifier-app-foundation`?
2. **@mention system:** Keep in foundation, move to profiles, or separate lib?
3. **Display protocols:** Should foundation define interfaces for UI systems?
4. **Async API:** Provide both sync and async, or async-only?
5. **Version strategy:** Pin dependencies or use ranges?

## 🔗 Related Documents

- [FOUNDATION_LIBRARY_PROPOSAL.md](./FOUNDATION_LIBRARY_PROPOSAL.md) - Detailed proposal
- [FOUNDATION_IMPLEMENTATION_GUIDE.md](./FOUNDATION_IMPLEMENTATION_GUIDE.md) - Technical guide
- [CLI README.md](./README.md) - Current CLI documentation

---

## 🎬 Getting Started

1. **Read** the full proposal: [FOUNDATION_LIBRARY_PROPOSAL.md](./FOUNDATION_LIBRARY_PROPOSAL.md)
2. **Review** implementation guide: [FOUNDATION_IMPLEMENTATION_GUIDE.md](./FOUNDATION_IMPLEMENTATION_GUIDE.md)
3. **Discuss** with team and refine scope
4. **Create** foundation repository
5. **Start** with smallest extraction (paths.py)
6. **Iterate** with fast feedback loops

---

*Last Updated: 2024*
*Status: PROPOSAL - Awaiting Team Review*
