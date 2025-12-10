# Amplifier Foundation - Implementation TODO

## 📋 Phase 1: Repository Setup (Week 1-2)

### Repository Creation
- [ ] Create `amplifier-foundation` repository on GitHub
- [ ] Initialize with MIT license
- [ ] Setup basic README.md
- [ ] Configure branch protection (main)
- [ ] Setup GitHub Actions for CI/CD

### Project Structure
- [ ] Create directory structure (`src/amplifier_foundation/`, `tests/`, `docs/`)
- [ ] Setup `pyproject.toml` with dependencies
- [ ] Configure development tools (ruff, mypy, pytest)
- [ ] Setup pre-commit hooks
- [ ] Create initial `__init__.py` with version

### Documentation Setup
- [ ] Create docs/ folder structure
- [ ] Setup documentation generator (sphinx/mkdocs)
- [ ] Create CONTRIBUTING.md
- [ ] Create CODE_OF_CONDUCT.md
- [ ] Write initial architecture.md

---

## 📦 Phase 2: Core Infrastructure Extraction (Week 3-4)

### Path Management
- [ ] Copy `paths.py` → `amplifier_foundation/paths.py`
- [ ] Update imports to absolute paths
- [ ] Write unit tests for path functions
- [ ] Write tests for ConfigPaths
- [ ] Write tests for scope validation
- [ ] Update docstrings with examples
- [ ] Verify factory functions work

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

---

## 🔌 Phase 3: Provider Management (Week 5-6)

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

---

## 💾 Phase 4: Session Management (Week 7-8)

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

---

## 🧩 Phase 5: Module Management (Week 9)

### Module Manager
- [ ] Copy `module_manager.py` → `amplifier_foundation/modules/manager.py`
- [ ] Update imports
- [ ] Write tests for add_module
- [ ] Write tests for remove_module
- [ ] Write tests for get_current_modules
- [ ] Document module registration

---

## 📊 Phase 6: Configuration Summary (Week 9)

### Effective Config
- [ ] Copy `effective_config.py` → `amplifier_foundation/config/summary.py`
- [ ] Update imports
- [ ] Write tests for get_effective_config_summary
- [ ] Write tests for provider selection by priority
- [ ] Document summary API

---

## 🔗 Phase 7: CLI Integration (Week 10-11)

### Update CLI Dependencies
- [ ] Update `pyproject.toml` to depend on foundation
- [ ] Remove direct dependencies on core libs
- [ ] Setup local editable install for development
- [ ] Update uv.lock

### Update CLI Imports
- [ ] Update `commands/provider.py` imports
- [ ] Update `commands/module.py` imports
- [ ] Update `commands/session.py` imports
- [ ] Update `commands/profile.py` imports
- [ ] Update `main.py` imports
- [ ] Update `session_spawner.py` (if any remains in CLI)
- [ ] Update all other command files

### Remove Duplicate Code
- [ ] Remove `paths.py` from CLI
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
- [ ] Run full CLI test suite
- [ ] Manual testing: `amplifier init`
- [ ] Manual testing: `amplifier provider use`
- [ ] Manual testing: `amplifier run`
- [ ] Manual testing: `amplifier continue`
- [ ] Manual testing: `amplifier session list`
- [ ] Manual testing: `amplifier profile use`
- [ ] Manual testing: `amplifier module add`
- [ ] Verify no performance regressions

---

## ✅ Phase 8: Testing & Validation (Week 12)

### Foundation Tests
- [ ] Achieve >90% test coverage
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

---

## 📚 Phase 9: Documentation (Week 13-14)

### API Documentation
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
- [ ] Write foundation README.md
- [ ] Update CLI README.md to mention foundation
- [ ] Add badges (coverage, version, license)
- [ ] Add installation instructions
- [ ] Add quick start examples
- [ ] Add link to full documentation

### Code Documentation
- [ ] Review all docstrings
- [ ] Add type hints where missing
- [ ] Add usage examples in docstrings
- [ ] Document error conditions
- [ ] Document performance characteristics

---

## 🚀 Phase 10: Release (Week 15-16)

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

---

## 🎯 Success Criteria Tracking

### Quantitative Metrics
- [ ] CLI LOC reduced by 40-60%
- [ ] Foundation test coverage >90%
- [ ] Minimal app buildable in <100 LOC
- [ ] Zero breaking changes to CLI UX
- [ ] Config resolution <10ms
- [ ] Session load <20ms

### Qualitative Metrics
- [ ] Team can build new app without CLI code dive
- [ ] Second app (GUI) validates API
- [ ] New contributors understand foundation code
- [ ] Documentation enables independent development
- [ ] Community feedback is positive

---

## 🔮 Future Phases (Post-1.0)

### Optional Enhancements
- [ ] High-level Application API
- [ ] Context/mention loading system
- [ ] Observability/tracing module
- [ ] Plugin system for extensions
- [ ] Performance optimizations
- [ ] Async + sync API variants

### Additional Apps
- [ ] Build GUI reference app
- [ ] Build web API reference app
- [ ] Build VS Code extension example
- [ ] Build Slack bot example

### Ecosystem
- [ ] Create starter templates
- [ ] Build scaffolding CLI (`amplifier-create-app`)
- [ ] Write blog posts and tutorials
- [ ] Present at conferences
- [ ] Grow community

---

## 📝 Notes & Decisions

### Open Questions
- [ ] **Naming:** Decided on `amplifier-foundation`?
- [ ] **Mention system:** Keep in foundation, profiles, or separate?
- [ ] **Display protocols:** Should foundation define them?
- [ ] **Async API:** Async-only or provide sync wrappers?
- [ ] **Version strategy:** Pin dependencies or ranges?

### Decisions Made
- [ ] Document: Foundation will use semantic versioning
- [ ] Document: Foundation will support Python 3.11+
- [ ] Document: Foundation will use MIT license
- [ ] Document: Foundation will prioritize backward compatibility
- [ ] Document: Foundation will have comprehensive type hints

---

## 🐛 Known Issues / Risks

### Technical Risks
- [ ] Circular import issues during extraction
- [ ] Performance regression in hot paths
- [ ] Windows file handle issues in session store
- [ ] Type checking issues with dynamic imports

### Project Risks
- [ ] Timeline slippage
- [ ] Scope creep (too many features)
- [ ] Breaking changes during refactor
- [ ] Insufficient testing before release

### Mitigation Strategies
- [ ] Incremental extraction with tests
- [ ] Performance benchmarks at each phase
- [ ] Comprehensive test suite
- [ ] Code review before major changes
- [ ] Regular team check-ins

---

## 📞 Stakeholders & Communication

### Team Members
- [ ] Assign owner for each phase
- [ ] Schedule weekly sync meetings
- [ ] Create Slack channel for discussion
- [ ] Setup GitHub discussions for Q&A

### Communication Plan
- [ ] Week 1: Kickoff meeting, review proposal
- [ ] Week 4: Demo core extraction, gather feedback
- [ ] Week 8: Demo session management
- [ ] Week 12: Demo CLI integration
- [ ] Week 16: Release announcement

---

## ✨ Quick Win Targets

### Week 1 Goals (Minimal)
- [ ] Repository created
- [ ] Structure setup
- [ ] First test passing

### Week 4 Goals (Core Done)
- [ ] Path management extracted
- [ ] Config system extracted
- [ ] CLI commands use foundation imports

### Week 8 Goals (Providers Done)
- [ ] Provider management extracted
- [ ] Session management extracted
- [ ] Example app works

### Week 12 Goals (Integration Done)
- [ ] CLI fully migrated
- [ ] All duplicate code removed
- [ ] Tests passing

### Week 16 Goals (Release)
- [ ] Documentation complete
- [ ] Published to PyPI
- [ ] Announcement sent

---

*Track progress by checking off items as they're completed.*
*Update this document as priorities change or new tasks emerge.*

**Current Phase:** Planning / Proposal Review
**Next Milestone:** Team approval and repository creation
**Target Completion:** 16 weeks from start
