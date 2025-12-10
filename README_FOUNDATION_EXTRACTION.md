# 🏗️ Amplifier Foundation Library Extraction

## 📌 Overview

This directory contains the proposal and implementation plan for extracting a common foundation library from the Amplifier CLI. The foundation will abstract the complexity of core amplifier dependencies and provide a unified API for building end-user applications.

## 📄 Documentation Index

### 1. **[FOUNDATION_LIBRARY_PROPOSAL.md](./FOUNDATION_LIBRARY_PROPOSAL.md)** - START HERE
   - **Purpose:** High-level architectural proposal
   - **Audience:** Team leads, architects, decision makers
   - **Contents:**
     - Executive summary and vision
     - What gets extracted vs what stays in CLI
     - Dependency injection patterns
     - Migration strategy (4 phases)
     - API design principles
     - Success criteria
     - Open questions for discussion

### 2. **[FOUNDATION_QUICK_REFERENCE.md](./FOUNDATION_QUICK_REFERENCE.md)**
   - **Purpose:** At-a-glance reference for the project
   - **Audience:** Everyone on the team
   - **Contents:**
     - Visual architecture diagrams
     - Component extraction map
     - Before/after code examples
     - Success metrics
     - Timeline summary
     - Key interfaces

### 3. **[FOUNDATION_IMPLEMENTATION_GUIDE.md](./FOUNDATION_IMPLEMENTATION_GUIDE.md)**
   - **Purpose:** Detailed technical implementation guide
   - **Audience:** Engineers implementing the extraction
   - **Contents:**
     - Repository structure
     - pyproject.toml configuration
     - Public API design (`__init__.py`)
     - Step-by-step migration process
     - Testing strategy
     - Documentation requirements
     - Validation checklist
     - Minimal app example

### 4. **[FOUNDATION_API_EXAMPLES.md](./FOUNDATION_API_EXAMPLES.md)**
   - **Purpose:** Concrete code examples showing API usage
   - **Audience:** Developers building on foundation
   - **Contents:**
     - Minimal app (50 lines)
     - Interactive REPL (100 lines)
     - CLI command simplification
     - GUI application example
     - Web API server example
     - Testing patterns
     - Custom path policy example

### 5. **[FOUNDATION_TODO.md](./FOUNDATION_TODO.md)**
   - **Purpose:** Detailed task checklist for implementation
   - **Audience:** Project manager, implementation team
   - **Contents:**
     - Phase-by-phase task breakdown
     - Checkbox tracking for each task
     - Success criteria tracking
     - Risk mitigation strategies
     - Communication plan
     - Quick win targets

## 🎯 Quick Start for Team Members

### If you're a **Decision Maker:**
1. Read [FOUNDATION_LIBRARY_PROPOSAL.md](./FOUNDATION_LIBRARY_PROPOSAL.md)
2. Review the "Open Questions" section
3. Approve or provide feedback

### If you're an **Implementer:**
1. Skim [FOUNDATION_LIBRARY_PROPOSAL.md](./FOUNDATION_LIBRARY_PROPOSAL.md)
2. Deep dive [FOUNDATION_IMPLEMENTATION_GUIDE.md](./FOUNDATION_IMPLEMENTATION_GUIDE.md)
3. Reference [FOUNDATION_TODO.md](./FOUNDATION_TODO.md) for tasks
4. Use [FOUNDATION_API_EXAMPLES.md](./FOUNDATION_API_EXAMPLES.md) for guidance

### If you're building an **App on Foundation:**
1. Read [FOUNDATION_QUICK_REFERENCE.md](./FOUNDATION_QUICK_REFERENCE.md)
2. Study [FOUNDATION_API_EXAMPLES.md](./FOUNDATION_API_EXAMPLES.md)
3. Reference API docs (once foundation is published)

## 🎬 Current Status

**Stage:** 📋 Proposal / Planning
**Next Step:** Team review and approval
**Estimated Start Date:** TBD (after approval)
**Estimated Completion:** 16 weeks from start

## 💡 Key Insights

### The Problem
The CLI currently handles too much:
- Configuration resolution
- Provider management  
- Session persistence
- Module/profile/collection loading
- Path management
- All while also being a CLI application

This makes it hard to:
- Build other types of apps (GUI, web API)
- Maintain the codebase
- Onboard new developers

### The Solution
Extract a **foundation library** that:
- ✅ Abstracts complexity of core dependencies
- ✅ Provides high-level, ergonomic APIs
- ✅ Enables rapid app development
- ✅ Maintains backward compatibility with CLI

### The Benefits
- **40-60% reduction** in CLI codebase
- **<100 lines** to build a working app
- **Single source** for core functionality
- **Better docs** (one place to learn)
- **Faster innovation** (easier to experiment)

## 📊 Visual Overview

```
Current State:                    Future State:
                                  
┌─────────────────┐              ┌──────────────┐
│  Amplifier CLI  │              │ CLI/GUI/API  │ ← Apps
│  - Everything!  │              │ - UI/UX only │
│  - UI/UX        │              └──────┬───────┘
│  - Config       │                     │ depends on
│  - Providers    │                     ▼
│  - Sessions     │              ┌──────────────┐
│  - Modules      │              │  Foundation  │ ← New!
│  - ...          │              │  - Config    │
└────────┬────────┘              │  - Providers │
         │                       │  - Sessions  │
         │ depends on            │  - Modules   │
         ▼                       └──────┬───────┘
┌─────────────────┐                     │ orchestrates
│   Core Deps     │                     ▼
│  - core         │              ┌──────────────┐
│  - config       │              │  Core Deps   │ ← Abstracted
│  - profiles     │              │  (5 libs)    │
│  - ...          │              └──────────────┘
└─────────────────┘              
```

## 🔑 Key Files to Extract

**High Priority:**
- `paths.py` - Path management (⭐ Critical)
- `runtime/config.py` - Config resolution (⭐ Critical)
- `provider_manager.py` - Provider lifecycle (⭐ Critical)
- `session_store.py` - Session persistence (⭐ Critical)

**Medium Priority:**
- `module_manager.py` - Module registration
- `key_manager.py` - Secure key storage
- `project_utils.py` - Project detection

See [FOUNDATION_LIBRARY_PROPOSAL.md](./FOUNDATION_LIBRARY_PROPOSAL.md#appendix-file-mapping) for complete mapping.

## 🎯 Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| CLI LOC reduction | 40-60% | 0% |
| Foundation test coverage | >90% | N/A |
| Minimal app size | <100 LOC | Impossible |
| Breaking CLI changes | 0 | N/A |
| Time to build app | <1 day | Several days |

## 🚀 Rollout Timeline

| Weeks | Phase | Deliverable |
|-------|-------|-------------|
| 1-2   | Setup | Foundation repo created |
| 3-4   | Core  | Path & config extracted |
| 5-6   | Providers | Provider management extracted |
| 7-8   | Sessions | Session management extracted |
| 9-10  | Integration | CLI uses foundation |
| 11-12 | Validation | Example apps work |
| 13-14 | Documentation | Full docs complete |
| 15-16 | Release | Published to PyPI |

## 📞 Questions & Discussion

### Open Questions
1. **Naming:** `amplifier-foundation` or `amplifier-app-foundation`?
2. **@mention system:** Foundation, profiles, or separate lib?
3. **Display protocols:** Should foundation define them?
4. **Async API:** Async-only or provide sync wrappers?

### How to Provide Feedback
- **GitHub Issues:** Open issue with "foundation" label
- **Team Meeting:** Discuss in weekly sync
- **Slack:** Post in #amplifier-foundation channel (TBD)
- **Email:** Send to architecture team

## 🛠️ Getting Involved

### As a Reviewer
1. Read the proposal documents
2. Test the examples mentally
3. Identify potential issues
4. Provide constructive feedback

### As an Implementer
1. Claim a phase from TODO.md
2. Follow implementation guide
3. Write tests for your code
4. Submit PRs with documentation

### As a User (Future)
1. Try building an app with foundation
2. Report bugs or API issues
3. Suggest improvements
4. Share your app with community

## 📚 Additional Resources

- **Current CLI Documentation:** [README.md](./README.md)
- **Amplifier Core:** https://github.com/microsoft/amplifier-core
- **Amplifier Config:** https://github.com/microsoft/amplifier-config
- **Amplifier Profiles:** https://github.com/microsoft/amplifier-profiles

## ⚠️ Important Notes

1. **Backward Compatibility:** The CLI must work identically after extraction
2. **No Breaking Changes:** User-facing CLI behavior cannot change
3. **Test Coverage:** All extracted code must have >90% coverage
4. **Documentation:** Write docs alongside code, not after
5. **Incremental:** Extract and test one component at a time

## 🎉 Expected Impact

### For End Users
- ✅ **Consistency** across all amplifier apps
- ✅ **Better documentation** in one place
- ✅ **More features** developed faster

### For Developers  
- ✅ **Lower barrier** to building apps
- ✅ **Focus on UX** instead of infrastructure
- ✅ **Reusable code** = less duplication

### For Ecosystem
- ✅ **Standards** across implementations
- ✅ **Innovation** through easier experimentation
- ✅ **Quality** through shared testing

## 📋 Checklist for Approval

Before proceeding with implementation, ensure:

- [ ] Team has reviewed proposal
- [ ] Open questions have been answered
- [ ] Success criteria are agreed upon
- [ ] Timeline is realistic
- [ ] Resources are allocated
- [ ] Risks are understood
- [ ] Communication plan is in place

## 🎓 Learning Path

**Week 1:** Understand the problem
- Read proposal
- Review current CLI codebase
- Understand core dependencies

**Week 2:** Understand the solution
- Study API examples
- Review implementation guide
- Ask clarifying questions

**Week 3:** Start contributing
- Pick a task from TODO.md
- Setup development environment
- Submit first PR

---

## 📝 Document History

| Date | Version | Changes |
|------|---------|---------|
| 2024-01 | 1.0 | Initial proposal created |

---

## 🤝 Contributors

This proposal was created through analysis of the `amplifier-app-cli` codebase to identify opportunities for extracting reusable infrastructure.

---

**Status:** 📋 PROPOSAL - Awaiting Team Review  
**Owner:** TBD  
**Last Updated:** 2024

---

*For questions or feedback, open a GitHub issue or contact the architecture team.*
