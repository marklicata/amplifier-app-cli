# CLI Cleanup Checklist

This document tracks files that should be removed from `amplifier-app-cli` once the foundation library extraction is complete.

## ✅ Already Extracted to Foundation

These components are now in `amplifier-foundation` and can be removed from the CLI:

### Core Path Management
- [x] `amplifier_app_cli/paths.py` → Replace with wrapper that re-exports from foundation
- [x] `amplifier_app_cli/lib/mention_loading/` → Replace with wrapper
- [x] `amplifier_app_cli/utils/mentions.py` → Replace with wrapper

### Provider Management  
- [ ] `amplifier_app_cli/provider_manager.py` → DELETE (use `amplifier_foundation.ProviderManager`)
- [ ] `amplifier_app_cli/provider_loader.py` → DELETE (use `amplifier_foundation.provider_loader`)
- [ ] `amplifier_app_cli/provider_sources.py` → DELETE (use `amplifier_foundation.provider_sources`)

### Module Management
- [ ] `amplifier_app_cli/module_manager.py` → DELETE (use `amplifier_foundation.ModuleManager`)

### Settings & Configuration
- [ ] `amplifier_app_cli/lib/app_settings/__init__.py` → DELETE (use `amplifier_foundation.AppSettings`)
- [ ] `amplifier_app_cli/effective_config.py` → DELETE (use `amplifier_foundation.effective_config`)

### Session & Storage
- [ ] `amplifier_app_cli/session_store.py` → DELETE (use `amplifier_foundation.SessionStore`)
- [ ] `amplifier_app_cli/key_manager.py` → DELETE (use `amplifier_foundation.KeyManager`)

### Utilities
- [ ] `amplifier_app_cli/project_utils.py` → DELETE (use `amplifier_foundation.project_utils`)

## 🔄 Import Updates Needed

After deleting the above files, update imports in these CLI files:

### Command Files
- [ ] `amplifier_app_cli/commands/config.py` - Update provider/module manager imports
- [ ] `amplifier_app_cli/commands/provider.py` - Update provider manager imports  
- [ ] `amplifier_app_cli/commands/session.py` - Update session store imports
- [ ] `amplifier_app_cli/commands/agent.py` - Update imports as needed
- [ ] `amplifier_app_cli/commands/__init__.py` - Check for any imports

### Runtime Configuration
- [ ] `amplifier_app_cli/runtime/config.py` - Update path/config imports
- [ ] `amplifier_app_cli/runtime/__init__.py` - Check for imports

### Main Entry Points
- [ ] `amplifier_app_cli/main.py` - Update all foundation imports
- [ ] `amplifier_app_cli/__init__.py` - Update exports
- [ ] `amplifier_app_cli/__main__.py` - Check for imports

### Agent & Spawning
- [ ] `amplifier_app_cli/session_spawner.py` - Update session store imports
- [ ] `amplifier_app_cli/agent_config.py` - Update as needed

### UI Components
- [ ] `amplifier_app_cli/console.py` - Update imports if needed
- [ ] `amplifier_app_cli/tui/` - Check for any foundation imports
- [ ] `amplifier_app_cli/ui/` - Check for any foundation imports

## 📝 Files to Keep in CLI

These are CLI-specific and should NOT be moved to foundation:

### CLI Commands (Keep All)
- `amplifier_app_cli/commands/` - All CLI command implementations
  - `config.py` - Config commands
  - `provider.py` - Provider commands
  - `session.py` - Session commands
  - `agent.py` - Agent delegation commands
  - `collection.py` - Collection commands
  - etc.

### UI/UX Components (Keep All)
- `amplifier_app_cli/console.py` - Rich console setup
- `amplifier_app_cli/tui/` - Textual UI components
- `amplifier_app_cli/ui/` - UI widgets and helpers
- `amplifier_app_cli/banners/` - CLI branding and banners

### CLI-Specific Features (Keep All)
- `amplifier_app_cli/main.py` - Interactive REPL loop
- `amplifier_app_cli/approval_provider.py` - CLI approval UX
- `amplifier_app_cli/trace_collector.py` - Trace collection UI
- `amplifier_app_cli/data/` - Bundled collections and profiles

### Runtime & Configuration (Keep, but update)
- `amplifier_app_cli/runtime/` - Runtime orchestration (update imports)
- `amplifier_app_cli/agent_config.py` - Agent configuration (update imports)
- `amplifier_app_cli/session_spawner.py` - Agent spawning (update imports)
- `amplifier_app_cli/provider_config_utils.py` - Provider config UI helpers (update imports)

## 🎯 Cleanup Process

### Phase 1: Update Imports (Safe)
1. Update all CLI files to import from `amplifier_foundation` instead of local modules
2. Test that CLI still works with foundation imports
3. Fix any breaking changes

### Phase 2: Remove Duplicates (Breaking)
1. Delete extracted files from CLI (listed above)
2. Remove now-unnecessary wrapper files
3. Update `pyproject.toml` to only depend on `amplifier-foundation`
4. Run full test suite

### Phase 3: Verify (Testing)
1. Test all CLI commands work correctly
2. Test all configuration scenarios
3. Test provider management
4. Test session management
5. Test agent delegation

## 📊 Expected Results

### Before Cleanup
- **CLI LOC**: ~4,500 lines
- **Dependencies**: 5 (core, config, module-resolution, collections, profiles)
- **Duplicate Code**: ~2,000 lines shared with foundation

### After Cleanup
- **CLI LOC**: ~2,500 lines (44% reduction)
- **Dependencies**: 1 (amplifier-foundation)
- **Duplicate Code**: 0 lines (foundation is source of truth)

## 🚧 Blockers

Before cleanup can begin:

1. [ ] Verify CLI still works with current foundation integration
2. [ ] Fix `ModuleValidationError` import in `main.py:18`
3. [ ] Complete all import updates
4. [ ] Run comprehensive CLI test suite
5. [ ] Get team approval for breaking changes

## 📅 Timeline

- **Week 1**: Update all imports (Phase 1)
- **Week 2**: Remove duplicates & test (Phase 2 & 3)
- **Week 3**: Fix any issues, final testing
- **Week 4**: Release v2.0 with foundation dependency

## 🔗 Related Documents

- `FOUNDATION_LIBRARY_PROPOSAL.md` - Original proposal
- `FOUNDATION_IMPLEMENTATION_GUIDE.md` - Implementation details
- `FOUNDATION_EXTRACTION_COMPLETE.md` - Phase 1 completion summary
- `README_FOUNDATION_EXTRACTION.md` - Documentation index

---

**Status**: 🟡 Ready to begin Phase 1 (import updates)  
**Last Updated**: 2024 (Current session)  
**Next Action**: Update imports in commands/ directory
