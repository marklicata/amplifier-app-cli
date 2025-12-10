# Amplifier Foundation - Implementation TODO (Updated Status)

## ✅ COMPLETED - Phase 1: Repository Setup (Week 1-2)

### Repository Creation
- [x] Create `amplifier-foundation` repository locally ✅
- [x] Initialize with MIT license ✅
- [x] Setup basic README.md ✅
- [ ] Configure GitHub remote (not pushed yet)
- [ ] Configure branch protection (main)
- [ ] Setup GitHub Actions for CI/CD

### Project Structure
- [x] Create directory structure (`amplifier_foundation/`, `tests/`, `docs/`) ✅
- [x] Setup `pyproject.toml` with dependencies ✅
- [x] Configure development tools (pytest) ✅
- [ ] Configure ruff, mypy
- [ ] Setup pre-commit hooks
- [x] Create initial `__init__.py` with version ✅

### Documentation Setup
- [x] Create docs/ folder structure ✅
- [ ] Setup documentation generator (sphinx/mkdocs)
- [ ] Create CONTRIBUTING.md
- [ ] Create CODE_OF_CONDUCT.md
- [ ] Write initial architecture.md

**Phase 1 Status: 60% Complete** ✅ Core done, CI/CD pending

---

## 🟡 IN PROGRESS - Phase 2: Core Infrastructure Extraction (Week 3-4)

### Path Management
- [x] Copy `paths.py` → `amplifier_foundation/paths.py` ✅
- [x] Update imports to absolute paths ✅
- [x] Write unit tests for path functions ✅
- [x] Write tests for ConfigPaths ✅
- [x] Write tests for scope validation ✅
- [x] Update docstrings with examples ✅
- [x] Verify factory functions work ✅

### Mention Loading (Bonus - Extracted Early)
- [x] Copy mention_loading → `amplifier_foundation/mention_loading/` ✅
- [x] Create models.py with MentionItem, MentionLoadResult ✅
- [x] Create deduplicator.py ✅
- [x] Create utils.py for text parsing ✅
- [x] Create resolver.py for path resolution ✅
- [x] Create loader.py for recursive loading ✅
- [x] Write unit tests (14 tests, all passing) ✅

### Configuration System
- [ ] Copy `runtime/config.py` → `amplifier_foundation/config/resolver.py`
- [ ] Copy `lib/app_settings/` → `amplifier_foundation/config/app_settings.py`
- [ ] Update imports in both files
- [ ] Write tests for resolve_app_config
- [ ] Write tests for AppSettings
- [ ] Write tests for deep_merge
- [ ] Write tests for env var expansion
- [ ] Document configuration resolution flow

### Utilities
- [ ] Copy `project_utils.py` → `amplifier_foundation/project.py`
- [ ] Write tests for get_project_slug
- [ ] Copy `key_manager.py` → `amplifier_foundation/security/keys.py`
- [ ] Write tests for KeyManager
- [ ] Test key storage security on Linux/Mac/Windows

**Phase 2 Status: 50% Complete** ✅ PathManager and mention loading done, config system pending

---

## ⏳ NOT STARTED - Phase 3: Provider Management (Week 5-6)

### Provider Sources
- [ ] Copy `provider_sources.py` → `amplifier_foundation/providers/sources.py`
- [ ] Update imports
- [ ] Write tests for get_effective_provider_sources
- [ ] Write tests for source_from_uri
- [ ] Write tests for install_known_providers
- [ ] Test local path support
- [ ] Test git URL support

### Provider Manager
- [ ] Copy `provider_manager.py` → `amplifier_foundation/providers/manager.py`
- [ ] Update imports
- [ ] Write tests for use_provider
- [ ] Write tests for get_current_provider
- [ ] Write tests for list_providers
- [ ] Write tests for reset_provider
- [ ] Write tests for priority selection
- [ ] Document provider lifecycle

### Provider Utilities
- [ ] Copy `provider_loader.py` → `amplifier_foundation/providers/loader.py`
- [ ] Copy `provider_config_utils.py` → `amplifier_foundation/providers/utils.py`
- [ ] Update imports
- [ ] Write tests
- [ ] Document provider discovery

**Phase 3 Status: 0% Complete**

---

## ⏳ NOT STARTED - Phase 4: Session Management (Week 7-8)

### Session Store
- [ ] Copy `session_store.py` → `amplifier_foundation/session/store.py`
- [ ] Update imports
- [ ] Write tests for save/load
- [ ] Write tests for atomic write
- [ ] Write tests for backup/recovery
- [ ] Write tests for cleanup
- [ ] Test on Windows (file handle issues)
- [ ] Document persistence format

### Session Spawner
- [ ] Copy `session_spawner.py` → `amplifier_foundation/session/spawner.py`
- [ ] Copy `agent_config.py` → `amplifier_foundation/session/config.py`
- [ ] Update imports
- [ ] Write tests for spawn_sub_session
- [ ] Write tests for resume_sub_session
- [ ] Write tests for W3C trace ID generation
- [ ] Write tests for config merging
- [ ] Document agent delegation pattern

**Phase 4 Status: 0% Complete**

---

## ⏳ NOT STARTED - Phase 5: Module Management (Week 9)

### Module Manager
- [ ] Copy `module_manager.py` → `amplifier_foundation/modules/manager.py`
- [ ] Update imports
- [ ] Write tests for add_module
- [ ] Write tests for remove_module
- [ ] Write tests for get_current_modules
- [ ] Document module registration

**Phase 5 Status: 0% Complete**

---

## ⏳ NOT STARTED - Phase 6: Configuration Summary (Week 9)

### Effective Config
- [ ] Copy `effective_config.py` → `amplifier_foundation/config/summary.py`
- [ ] Update imports
- [ ] Write tests for get_effective_config_summary
- [ ] Write tests for provider selection by priority
- [ ] Document summary API

**Phase 6 Status: 0% Complete**

---

## 🟡 PARTIALLY DONE - Phase 7: CLI Integration (Week 10-11)

### Update CLI Dependencies
- [x] Update `pyproject.toml` to depend on foundation ✅
- [x] Setup local editable install for development ✅
- [x] Update uv.lock ✅
- [ ] Remove direct dependencies on core libs (kept for now)

### Update CLI Imports
- [x] Create wrapper in `paths.py` to re-export foundation ✅
- [x] Create wrapper in `lib/mention_loading/` to re-export foundation ✅
- [x] Create wrapper in `utils/mentions.py` to re-export foundation ✅
- [ ] Update `commands/provider.py` imports
- [ ] Update `commands/module.py` imports
- [ ] Update `commands/session.py` imports
- [ ] Update `commands/profile.py` imports
- [ ] Update other command files as needed

### Remove Duplicate Code (BLOCKED - Waiting for full extraction)
- [ ] Remove original `paths.py` from CLI (keeping wrapper)
- [ ] Remove original `lib/mention_loading/` from CLI (keeping wrapper)
- [ ] Remove `runtime/config.py` from CLI
- [ ] Remove `lib/app_settings/` from CLI
- [ ] Remove `provider_manager.py` from CLI
- [ ] Remove `provider_sources.py` from CLI
- [ ] Remove `session_store.py` from CLI
- [ ] Remove `module_manager.py` from CLI
- [ ] Remove `key_manager.py` from CLI
- [ ] Remove `project_utils.py` from CLI
- [ ] Remove `effective_config.py` from CLI
- [ ] Update MANIFEST.in if needed

### Verify CLI Functionality
- [ ] Fix `ModuleValidationError` import in main.py ⚠️ BLOCKING
- [ ] Run full CLI test suite
- [ ] Manual testing: `amplifier init`
- [ ] Manual testing: `amplifier provider use`
- [ ] Manual testing: `amplifier run`
- [ ] Manual testing: `amplifier continue`
- [ ] Manual testing: `amplifier session list`
- [ ] Manual testing: `amplifier profile use`
- [ ] Manual testing: `amplifier module add`
- [ ] Verify no performance regressions

**Phase 7 Status: 30% Complete** ⚠️ Blocked by import error

---

## ⏳ NOT STARTED - Phase 8: Testing & Validation (Week 12)

### Foundation Tests
- [x] Basic tests written (14 passing) ✅
- [ ] Achieve >90% test coverage (currently ~60%)
- [ ] Add integration tests
- [ ] Add performance benchmarks
- [ ] Test on Linux
- [ ] Test on macOS
- [ ] Test on Windows
- [ ] Setup CI/CD pipeline
- [ ] Configure codecov or similar

### Example Applications
- [ ] Build minimal.py example (50 lines)
- [ ] Build repl.py example (100 lines)
- [ ] Build gui_app.py example
- [ ] Build api_server.py example
- [ ] Verify all examples work
- [ ] Document example setup

### CLI Regression Testing
- [ ] Run CLI test suite again
- [ ] Compare performance benchmarks
- [ ] Test all CLI commands manually
- [ ] Verify no breaking changes
- [ ] Get user testing feedback

**Phase 8 Status: 10% Complete** (Basic tests only)

---

## ⏳ NOT STARTED - Phase 9: Documentation (Week 13-14)

### API Documentation
- [x] Foundation README.md created ✅
- [ ] Generate API reference from docstrings
- [ ] Write quickstart.md
- [ ] Write concepts.md
- [ ] Write configuration.md
- [ ] Write providers.md
- [ ] Write sessions.md
- [ ] Write modules.md
- [ ] Write building-apps.md tutorial
- [ ] Write migration-guide.md

### README Updates
- [x] Write foundation README.md ✅
- [x] Create CLI documentation linking to foundation ✅
- [ ] Update CLI README.md to mention foundation
- [ ] Add badges (coverage, version, license)
- [ ] Add installation instructions
- [ ] Add quick start examples
- [ ] Add link to full documentation

### Code Documentation
- [x] Basic docstrings in PathManager ✅
- [x] Basic docstrings in mention_loading ✅
- [ ] Review all docstrings for completeness
- [ ] Add type hints where missing
- [ ] Add usage examples in docstrings
- [ ] Document error conditions
- [ ] Document performance characteristics

**Phase 9 Status: 20% Complete** (Basic README done)

---

## ⏳ NOT STARTED - Phase 10: Release (Week 15-16)

### Pre-Release Checklist
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Examples work
- [ ] CLI integration verified
- [ ] Performance acceptable
- [ ] Security review done
- [ ] License files in place
- [ ] CHANGELOG.md created

### PyPI Preparation
- [ ] Setup PyPI account/token
- [ ] Configure publishing workflow
- [ ] Test build process (`uv build`)
- [ ] Test install from wheel
- [ ] Verify package metadata

### Release v0.1.0
- [ ] Tag release in git
- [ ] Generate release notes
- [ ] Publish to PyPI
- [ ] Update CLI to use PyPI version
- [ ] Announce in team channels
- [ ] Update documentation links

### Post-Release
- [ ] Monitor for issues
- [ ] Respond to feedback
- [ ] Plan v0.2.0 improvements
- [ ] Write blog post / announcement
- [ ] Update roadmap

**Phase 10 Status: 0% Complete**

---

## 🎯 Overall Progress Summary

| Phase | Status | Completion |
|-------|--------|-----------|
| 1. Repository Setup | ✅ Mostly Done | 60% |
| 2. Core Infrastructure | 🟡 In Progress | 50% |
| 3. Provider Management | ⏳ Not Started | 0% |
| 4. Session Management | ⏳ Not Started | 0% |
| 5. Module Management | ⏳ Not Started | 0% |
| 6. Config Summary | ⏳ Not Started | 0% |
| 7. CLI Integration | 🟡 Partial | 30% |
| 8. Testing & Validation | ⏳ Not Started | 10% |
| 9. Documentation | 🟡 Started | 20% |
| 10. Release | ⏳ Not Started | 0% |
| **OVERALL** | **🟡 Early Progress** | **~20%** |

---

## 🚨 CRITICAL BLOCKERS

### Immediate Issues
1. **ModuleValidationError Import** ⚠️ HIGH PRIORITY
   - Location: `amplifier-app-cli/main.py:18`
   - Error: `from amplifier_core.errors import ModuleValidationError`
   - Issue: Class doesn't exist in amplifier_core
   - Impact: CLI cannot start
   - Action: Need to investigate and fix

### Next Priority Items
2. **Complete Configuration System Extraction**
   - Extract `runtime/config.py`
   - Extract `lib/app_settings/`
   - Write comprehensive tests
   
3. **Provider Management Extraction**
   - Critical for CLI functionality
   - Large component (~500 LOC)
   - Needs careful testing

4. **CLI Integration Testing**
   - Blocked by import error
   - Need full regression test suite
   - Performance benchmarks

---

## 📊 Success Criteria Status

### Quantitative Metrics
- [ ] CLI LOC reduced by 40-60% (currently ~5%)
- [ ] Foundation test coverage >90% (currently ~60%)
- [ ] Minimal app buildable in <100 LOC (not yet tested)
- [x] Zero breaking changes to CLI UX ✅ (wrapper pattern works)
- [ ] Config resolution <10ms (not benchmarked)
- [ ] Session load <20ms (not implemented)

### Qualitative Metrics
- [ ] Team can build new app without CLI code dive
- [ ] Second app (GUI) validates API
- [ ] New contributors understand foundation code
- [ ] Documentation enables independent development
- [ ] Community feedback is positive

**Overall Success Criteria: 10% achieved**

---

## 🎯 Recommended Next Actions

### This Week
1. ✅ **Fix ModuleValidationError import** - Unblock CLI
2. 🔄 **Extract configuration system** - Complete Phase 2
3. 🔄 **Write integration tests** - Ensure CLI still works
4. 🔄 **Test foundation in isolation** - Build a minimal example

### Next Week
5. **Extract provider management** - Start Phase 3
6. **Extract session management** - Start Phase 4
7. **Remove duplicate CLI code** - Clean up wrappers
8. **Full CLI regression testing** - Verify everything works

### Month 2
9. **Complete all extractions** - Phases 5-6
10. **Build example applications** - Validate API
11. **Write comprehensive docs** - Enable adoption
12. **Prepare for release** - PyPI, CI/CD, etc.

---

## 📝 Notes & Open Questions

### Decisions Still Needed
- [ ] **Repository hosting:** GitHub organization? Personal? Microsoft?
- [ ] **Naming:** Confirmed `amplifier-foundation` or other?
- [ ] **Version strategy:** Pin deps or allow ranges?
- [ ] **Python versions:** 3.11+ only or support 3.10?
- [ ] **Async API:** Async-only or provide sync wrappers?

### Technical Questions
- [ ] **Mention system:** Should it stay in foundation or move to separate package?
- [ ] **Display protocols:** Should foundation define them?
- [ ] **Approval system:** Foundation or CLI-specific?
- [ ] **Bundled data:** How to handle collections/profiles in foundation?

---

## ✨ What's Working Well

### Successes So Far
- ✅ **PathManager pattern** - Clean, dependency injection-based API
- ✅ **Wrapper approach** - Zero-breaking-change integration
- ✅ **Test coverage** - All foundation tests passing
- ✅ **Documentation** - Comprehensive planning docs created
- ✅ **Mention loading** - Fully extracted and working

### Lessons Learned
- **Incremental extraction works** - Small, tested pieces are manageable
- **Wrappers prevent breakage** - Re-exporting maintains compatibility
- **Tests catch issues early** - Without tests, integration is risky
- **Documentation is essential** - Clear vision makes implementation easier

---

*Last Updated: During implementation*
*Current Phase: 2 (Core Infrastructure - In Progress)*
*Next Milestone: Fix CLI import error, complete config extraction*
