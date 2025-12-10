# Amplifier Foundation - Architecture Diagrams

Visual representations of the foundation library architecture and relationships.

---

## 1. Current Architecture (Before Extraction)

```
┌──────────────────────────────────────────────────────────────────┐
│                         Amplifier CLI                             │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   Commands   │  │   UI/UX      │  │   Runtime    │           │
│  │              │  │              │  │              │           │
│  │ - provider   │  │ - console    │  │ - config     │           │
│  │ - session    │  │ - tui        │  │ - paths      │           │
│  │ - profile    │  │ - banners    │  │ - managers   │           │
│  │ - module     │  │ - approval   │  │ - spawner    │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│                                                                    │
│  Everything mixed together - hard to reuse!                       │
└──────────────────────────────────┬───────────────────────────────┘
                                   │ directly depends on (messy)
                                   ▼
┌──────────────────────────────────────────────────────────────────┐
│                      Core Dependencies                            │
│  ┌─────────────┐ ┌─────────────┐ ┌──────────────┐               │
│  │ amplifier-  │ │ amplifier-  │ │  amplifier-  │               │
│  │    core     │ │   config    │ │   profiles   │               │
│  └─────────────┘ └─────────────┘ └──────────────┘               │
│  ┌─────────────┐ ┌─────────────┐                                 │
│  │ amplifier-  │ │ amplifier-  │                                 │
│  │ collections │ │   module-   │                                 │
│  │             │ │  resolution │                                 │
│  └─────────────┘ └─────────────┘                                 │
└──────────────────────────────────────────────────────────────────┘
```

**Problems:**
- CLI has too many responsibilities
- Hard to build other app types (GUI, API)
- Code duplication when building new apps
- Tight coupling to CLI-specific concerns

---

## 2. Target Architecture (After Extraction)

```
┌────────────────────────────────────────────────────────────────┐
│                    End-User Applications                        │
│                                                                  │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐      │
│  │      CLI      │  │      GUI      │  │   Web API     │      │
│  │               │  │               │  │               │      │
│  │ - Commands    │  │ - Tkinter UI  │  │ - FastAPI     │      │
│  │ - Rich UI     │  │ - Qt widgets  │  │ - Endpoints   │      │
│  │ - REPL loop   │  │ - Event loop  │  │ - Models      │      │
│  │ - Banners     │  │ - Buttons     │  │ - Auth        │      │
│  └───────────────┘  └───────────────┘  └───────────────┘      │
│                                                                  │
│  Apps focus on UX, not infrastructure                           │
└────────────────────────┬───────────────────────────────────────┘
                         │ depends on (clean interface)
                         ▼
┌────────────────────────────────────────────────────────────────┐
│                  Amplifier Foundation Library                   │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │  Configuration   │  │    Providers     │                    │
│  │                  │  │                  │                    │
│  │ - Path policy    │  │ - Manager        │                    │
│  │ - Scope system   │  │ - Sources        │                    │
│  │ - Resolution     │  │ - Discovery      │                    │
│  │ - App settings   │  │ - Configuration  │                    │
│  └──────────────────┘  └──────────────────┘                    │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │    Sessions      │  │     Modules      │                    │
│  │                  │  │                  │                    │
│  │ - Persistence    │  │ - Registration   │                    │
│  │ - Store/load     │  │ - Discovery      │                    │
│  │ - Agent spawning │  │ - Management     │                    │
│  │ - Multi-turn     │  │ - Sources        │                    │
│  └──────────────────┘  └──────────────────┘                    │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │    Security      │  │     Project      │                    │
│  │                  │  │                  │                    │
│  │ - Key storage    │  │ - Detection      │                    │
│  │ - Encryption     │  │ - Slug gen       │                    │
│  └──────────────────┘  └──────────────────┘                    │
│                                                                  │
│  Reusable infrastructure for all apps                           │
└────────────────────────┬───────────────────────────────────────┘
                         │ orchestrates (abstraction)
                         ▼
┌────────────────────────────────────────────────────────────────┐
│                      Core Dependencies                          │
│                   (abstracted away from apps)                   │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌──────────────┐             │
│  │ amplifier-  │ │ amplifier-  │ │  amplifier-  │             │
│  │    core     │ │   config    │ │   profiles   │             │
│  └─────────────┘ └─────────────┘ └──────────────┘             │
│  ┌─────────────┐ ┌─────────────┐                               │
│  │ amplifier-  │ │ amplifier-  │                               │
│  │ collections │ │   module-   │                               │
│  │             │ │  resolution │                               │
│  └─────────────┘ └─────────────┘                               │
└────────────────────────────────────────────────────────────────┘
```

**Benefits:**
- Clean separation of concerns
- Apps depend only on foundation
- Foundation abstracts core complexity
- Easy to build new app types

---

## 3. Foundation Module Structure

```
amplifier-foundation/
│
├── paths.py                          # Central path policy
│   └── Exports: ConfigPaths, factories, search paths
│
├── config/
│   ├── __init__.py
│   ├── manager.py                    # ConfigManager wrapper
│   ├── resolver.py                   # resolve_app_config()
│   ├── app_settings.py               # High-level settings API
│   └── summary.py                    # Display summaries
│
├── providers/
│   ├── __init__.py
│   ├── manager.py                    # ProviderManager
│   ├── sources.py                    # Canonical sources
│   ├── loader.py                     # Discovery
│   └── utils.py                      # Config wizards
│
├── session/
│   ├── __init__.py
│   ├── store.py                      # SessionStore (persistence)
│   ├── spawner.py                    # Agent delegation
│   └── config.py                     # Config merging
│
├── modules/
│   ├── __init__.py
│   └── manager.py                    # ModuleManager
│
├── security/
│   ├── __init__.py
│   └── keys.py                       # KeyManager
│
└── project.py                        # Project utilities
```

---

## 4. Data Flow: Configuration Resolution

```
User Config Files              Foundation                     Output
                                                              
~/.amplifier/                                                 
  settings.yaml ────┐                                         
                    │                                         
.amplifier/         │         ┌──────────────┐               
  settings.yaml ────┼────────▶│ ConfigManager│               
                    │         └───────┬──────┘               
.amplifier/         │                 │                       
  settings.local ───┘                 ▼                       
       .yaml                  ┌──────────────┐               
                              │   Merger     │               
profiles/                     │  (3-scope)   │               
  dev.yaml ─────────────────▶ └──────┬───────┘               
                                     │                        
                                     ▼                        
CLI Overrides              ┌──────────────────┐              
  --provider ─────────────▶│ resolve_app_     │──────▶ Mount Plan
  --model ────────────────▶│    config()      │        (ready to use)
                           └──────────────────┘              
                                                              
  Priority: CLI > Local > Project > User > Profile            
```

---

## 5. Data Flow: Provider Selection

```
Settings                    Foundation                   Selected Provider
                                                         
User Settings              ┌──────────────────┐         
  config:                  │  AppSettings     │         
    providers: []  ───────▶│   .get_provider_ │         
                           │     overrides()  │         
Project Settings           └────────┬─────────┘         
  config:                           │                   
    providers:                      ▼                   
      - module: anthropic  ┌──────────────────┐         
        config:            │  Priority Sort   │         
          priority: 1 ────▶│  (lower wins)    │         
                           └────────┬─────────┘         
Profile                             │                   
  providers:                        ▼                   
    - module: openai       ┌──────────────────┐         
      config:              │   Select First   │──────▶ provider-anthropic
        priority: 100 ────▶│   (priority: 1)  │        (priority: 1 wins)
                           └──────────────────┘         
                                                         
  Lower priority number = higher precedence              
```

---

## 6. Data Flow: Session Persistence

```
Session Execution           Foundation                    Storage
                                                         
User prompt ───────────▶ AmplifierSession               
                             │                          
                             ▼                          
                        Execute & build                 
                         transcript                     
                             │                          
                             ▼                          
                        ┌──────────────┐                
                        │ SessionStore │                
                        │   .save()    │                
                        └──────┬───────┘                
                               │                        
                               ▼                        
                     ┌──────────────────┐               
                     │ Atomic Write     │               
                     │  1. Write temp   │               
                     │  2. Backup old   │               
                     │  3. Rename       │               
                     └────────┬─────────┘               
                              │                         
                              ▼                         
~/.amplifier/projects/<slug>/sessions/<id>/             
  ├── transcript.jsonl  ◀──── Message history           
  ├── metadata.json     ◀──── Session config            
  ├── *.backup          ◀──── Recovery files            
  └── profile.md        ◀──── Profile snapshot          
```

---

## 7. Component Dependencies

```
┌──────────────────────────────────────────────────┐
│              Application Layer                    │
│  (CLI commands, GUI widgets, API endpoints)      │
└────────────────────┬─────────────────────────────┘
                     │ uses
                     ▼
┌──────────────────────────────────────────────────┐
│           Foundation Public API                   │
│                                                   │
│  create_config_manager()                          │
│  create_provider_manager()                        │
│  create_session_store()                           │
│  resolve_app_config()                             │
└────────────────────┬─────────────────────────────┘
                     │ composed of
                     ▼
┌──────────────────────────────────────────────────┐
│          Foundation Components                    │
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  Paths   │─▶│  Config  │─▶│ Providers│       │
│  └──────────┘  └──────────┘  └──────────┘       │
│       │               │              │           │
│       │               ▼              ▼           │
│       │        ┌──────────┐   ┌──────────┐      │
│       └───────▶│ Sessions │   │ Modules  │      │
│                └──────────┘   └──────────┘      │
└────────────────────┬─────────────────────────────┘
                     │ uses
                     ▼
┌──────────────────────────────────────────────────┐
│         Core Library Dependencies                 │
│                                                   │
│  amplifier-core                                   │
│  amplifier-config                                 │
│  amplifier-profiles                               │
│  amplifier-collections                            │
│  amplifier-module-resolution                      │
└──────────────────────────────────────────────────┘

Dependencies flow one direction (no cycles)
```

---

## 8. Scope System Visualization

```
Settings Files                    Scope Priority           Effective Config
(explicit)                        (precedence)             (merged result)

                                                           
.amplifier/                       Highest Priority         
  settings.local.yaml ─────────▶  (LOCAL)          ─┐     
                                                     │     
                                                     ▼     
.amplifier/                       Medium Priority          
  settings.yaml ───────────────▶  (PROJECT)        ─┼────▶ Merged Settings
                                                     │      (LOCAL overrides
                                                     ▼       PROJECT overrides
~/.amplifier/                     Lower Priority            USER)
  settings.yaml ───────────────▶  (USER/GLOBAL)    ─┘     
                                                           
                                                           
Scope Availability:                                        
                                                           
When cwd = home dir:              When cwd ≠ home:        
  ✗ LOCAL (disabled)                ✓ LOCAL (enabled)     
  ✗ PROJECT (disabled)              ✓ PROJECT (enabled)   
  ✓ USER (always)                   ✓ USER (always)       
```

---

## 9. Provider Source Resolution

```
Provider Request              Resolution Strategy           Source
                                                           
provider-anthropic ───────▶  1. Check settings             
                                modules.providers[]        
                                for source override        
                                                           
                             2. Check DEFAULT_              
                                PROVIDER_SOURCES           
                                                           
                             3. Return canonical ─────────▶ git+https://github.com/
                                                             microsoft/amplifier-
                                                             module-provider-
                                                             anthropic@main
                                                           
provider-custom ──────────▶  1. Check settings             
                                modules.providers[]        
                                                           
                             2. User must have    ─────────▶ file://./my-provider
                                specified source             (local path)
                                (no default)                 or
                                                             git+https://...
                                                             (git URL)
```

---

## 10. Session Spawning (Agent Delegation)

```
Parent Session                 Foundation                Child Session
                                                        
┌──────────────┐                                      ┌──────────────┐
│  Session A   │                                      │  Session B   │
│  (main)      │                                      │  (agent)     │
│              │                                      │              │
│ prompt: "..."│─────▶ spawn_sub_session()           │              │
│              │         │                            │              │
│ config: {...}│         ├──▶ Merge configs           │              │
│              │         │    (parent + agent)        │              │
│              │         │                            │              │
│              │         ├──▶ Generate child ID       │ id: <parent>-│
│              │         │    (W3C trace pattern)     │     <child>_ │
│              │         │                            │     agent-name
│              │         │                            │              │
│              │         ├──▶ Create child session    │              │
│              │         │                            │              │
│              │         ├──▶ Initialize & mount      │              │
│              │         │                            │              │
│              │         └──▶ Execute instruction ───▶│ execute()    │
│              │                                      │              │
│              │◀────── return response + session_id ─┤              │
│              │                                      │              │
│              │         (can resume later with ID)  │              │
└──────────────┘                                      └──────────────┘
                                                      
Trace ID propagation:                                 
  Parent: root-session-id (becomes trace_id)          
  Child:  <parent-span>-<child-span>_agent-name       
          ^^^^^^^^^^^^^─inherited─^^^^^               
```

---

## 11. API Usage Patterns

### Pattern 1: Factory Functions (High-Level)
```
Application Code              Foundation                 Core Libs
                                                        
create_config_                                         
  _manager() ─────────────▶ ConfigManager ──────────▶ amplifier-config
                            (wraps complexity)         
                                                        
create_provider_                                       
  _manager(config) ──────▶ ProviderManager ─────────▶ amplifier-module-
                            (abstracts discovery)       resolution
```

### Pattern 2: Manager Classes (Explicit)
```
Application Code              Foundation                 Core Libs
                                                        
ConfigPaths(...)                                       
     ↓                                                 
ConfigManager(paths) ────▶ Direct control  ──────────▶ amplifier-config
     ↓                                                 
ProviderManager(config) ─▶ Explicit config ──────────▶ amplifier-module-
                                                         resolution
```

### Pattern 3: Application API (Future)
```
Application Code              Foundation                 Everything
                                                        
Application() ───────────────▶ All-in-one   ──────────▶ Manages all
     ↓                         wrapper                   dependencies
app.create_session()                                    
```

---

## 12. Testing Strategy Layers

```
┌──────────────────────────────────────────────────┐
│            Integration Tests                      │
│  Test entire workflows (CLI commands, etc)       │
└────────────────────┬─────────────────────────────┘
                     │ validates
                     ▼
┌──────────────────────────────────────────────────┐
│          Foundation Component Tests               │
│  Test each manager/module in isolation           │
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  Paths   │  │  Config  │  │ Providers│       │
│  │  Tests   │  │  Tests   │  │  Tests   │       │
│  └──────────┘  └──────────┘  └──────────┘       │
│  ┌──────────┐  ┌──────────┐                      │
│  │ Sessions │  │ Modules  │                      │
│  │  Tests   │  │  Tests   │                      │
│  └──────────┘  └──────────┘                      │
└────────────────────┬─────────────────────────────┘
                     │ mocks
                     ▼
┌──────────────────────────────────────────────────┐
│          Core Library Mocks                       │
│  Mock amplifier-core, config, profiles, etc      │
└──────────────────────────────────────────────────┘
```

---

## Summary

The foundation library provides a clean abstraction layer that:

1. **Simplifies** app development
2. **Abstracts** core dependency complexity
3. **Enables** rapid prototyping
4. **Maintains** backward compatibility
5. **Standardizes** patterns across apps

Apps depend on foundation → Foundation orchestrates core libs → Everyone wins!

---

*These diagrams illustrate the architectural vision for the foundation library.*
