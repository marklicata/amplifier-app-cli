# Amplifier CLI

Command-line interface for the Amplifier AI-powered modular development platform.

> **Note**: This is a **reference implementation** of an Amplifier CLI. It works with [amplifier-core](https://github.com/microsoft/amplifier-core) and demonstrates how to build a CLI around the kernel. You can use this as-is, fork it, or build your own CLI using [amplifier-foundation](https://github.com/microsoft/amplifier-foundation).

## Installation

### For Users

```bash
# Try without installing
uvx --from git+https://github.com/microsoft/amplifier amplifier

# Install globally
uv tool install git+https://github.com/microsoft/amplifier
```

## Quick Start

```bash
# First-time setup (auto-runs if no config)
amplifier init

# Tip: Set environment variables for faster setup
# export ANTHROPIC_API_KEY="your-key"
# The wizard detects env vars and shows them as defaults

# Install shell completion (optional, one-time setup)
amplifier --install-completion

# Single command
amplifier run "Create a Python function to calculate fibonacci numbers"

# Single command via stdin (useful for scripts/pipelines)
echo "Summarize this spec" | amplifier run

# Interactive chat mode
amplifier

# Use specific profile
amplifier run --profile dev "Your prompt"
```

**Environment variables**: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `AZURE_OPENAI_API_KEY` detected automatically during `amplifier init`.

## Commands

### Configuration Commands

```bash
# Provider management
amplifier provider use <name> [--local|--project|--global]
amplifier provider current
amplifier provider list
amplifier provider reset [--scope]

# Profile management
amplifier profile use <name> [--local|--project|--global]
amplifier profile current
amplifier profile list
amplifier profile show <name>
amplifier profile default [--set <name>|--clear]
amplifier profile reset

# Collection management
amplifier collection add <git-url> [--local]
amplifier collection list
amplifier collection show <name>
amplifier collection remove <name> [--local]
amplifier collection refresh [<name>] [--mutable-only]

# Module management
amplifier module add <name> [--local|--project|--global]
amplifier module remove <name> [--scope]
amplifier module current
amplifier module list
amplifier module show <name>
amplifier module refresh [<name>] [--mutable-only]
amplifier module check-updates

# Source management
amplifier source add <id> <uri> [--local|--project|--global]
amplifier source remove <id> [--scope]
amplifier source list
amplifier source show <id>
```

### Session Commands

```bash
# New sessions
amplifier run "prompt"                    # Single-shot (auto-persists, shows ID)
amplifier                                 # Interactive (auto-generates ID)

# Runtime overrides (highest priority, override all config levels)
amplifier run -p anthropic "prompt"              # Use specific provider
amplifier run -m claude-sonnet-4-5 "prompt"      # Use specific model
amplifier run --max-tokens 500 "prompt"          # Limit output tokens
amplifier run -p openai -m gpt-4o --max-tokens 1000 "prompt"  # Combine flags

# Resume workflows
amplifier continue                        # Resume most recent (interactive)
amplifier continue "new prompt"           # Resume most recent (single-shot)
amplifier run --resume <id> "prompt"      # Resume specific session
echo "prompt" | amplifier continue        # Resume via Unix pipe

# Session management
amplifier session list                    # Recent sessions
amplifier session show <id>               # Session details
amplifier session resume <id>             # Resume specific (interactive)
amplifier session delete <id>             # Delete session
amplifier session cleanup [--days N]      # Clean up old sessions
```

### Conversational Single-Shot Workflows

**Build context across multiple commands:**

```bash
# Question 1: Start conversation
$ amplifier run "What's the weather in Seattle?"
Session ID: a1b2c3d4
[Response about Seattle weather]

# Question 2: Follow-up with context
$ amplifier continue "And what about tomorrow?"
✓ Resuming most recent session: a1b2c3d4
  Messages: 2
[Response with context from previous question]

# Question 3: Continue the thread
$ amplifier continue "Should I bring an umbrella?"
✓ Resuming most recent session: a1b2c3d4
  Messages: 4
[Response informed by entire weather conversation]
```

**Unix piping with context:**

```bash
# Initial question
$ amplifier run "Analyze this log file structure"
Session ID: e5f6g7h8
[Analysis]

# Follow-up via pipe
$ cat errors.log | amplifier continue
✓ Resuming most recent session: e5f6g7h8
  Messages: 2
[Analysis of errors with context from previous conversation]
```

**Resume specific conversation:**

```bash
# List your sessions
$ amplifier session list
Recent Sessions:
  a1b2c3d4  2024-11-10 14:30  6 messages  # Weather conversation
  e5f6g7h8  2024-11-10 12:15  4 messages  # Log analysis

# Resume the weather conversation specifically
$ amplifier run --resume a1b2c3d4 "What about next week?"
✓ Resuming session: a1b2c3d4
  Messages: 6
[Response with full weather conversation context]
```

### Tool Commands

```bash
# List tools available in the active profile (shows actual tool names)
amplifier tool list                               # Table format (mounts tools)
amplifier tool list --modules                     # Show module names (fast, no mount)
amplifier tool list --profile dev                 # Specify profile
amplifier tool list --output json                 # JSON format

# Show details about a specific tool
amplifier tool info <tool-name>                   # Show tool info
amplifier tool info read_file --profile dev       # With specific profile
amplifier tool info --module tool-filesystem      # Show module info (fast)

# Invoke a tool directly with arguments
amplifier tool invoke read_file file_path=/tmp/test.txt
amplifier tool invoke bash command="ls -la"
amplifier tool invoke web_fetch url="https://example.com"
```

**Note**: Tool modules (e.g., `tool-filesystem`) expose multiple actual tools (e.g., `read_file`, `write_file`, `edit_file`). Use `amplifier tool list` to see actual tool names, or `--modules` for a fast module-level view.

### Utility Commands

```bash
amplifier init                                     # First-time setup
amplifier update [--check-only] [--force] [-y]    # Update Amplifier, modules, and collections
amplifier --install-completion                     # Set up tab completion
amplifier --version                                # Show version
amplifier --help                                   # Show help
```

**Update command options**:
- `--check-only`: Check for updates without installing
- `--force`: Force update all sources (skip update detection)
- `-y, --yes`: Skip confirmation prompts
- `--verbose`: Show detailed multi-line output per source (default: concise one-line format)

## Shell Completion

Enable tab completion with one command. Amplifier automatically installs completion for standard shell setups.

### One-Command Installation

```bash
amplifier --install-completion
```

**What happens**:
1. Detects your shell (bash, zsh, or fish) from `$SHELL`
2. **Automatically appends** the completion line to your shell config:
   - Bash: `~/.bashrc`
   - Zsh: `~/.zshrc`
   - Fish: `~/.config/fish/completions/amplifier.fish`
3. Checks if already installed (safe to run multiple times)
4. Falls back to manual instructions if custom configuration detected

**Output (standard setup)**:
```
Detected shell: bash
✓ Added completion to /home/user/.bashrc

To activate:
  source ~/.bashrc

Or start a new terminal.
```

**Output (already installed)**:
```
Detected shell: bash
✓ Completion already configured in /home/user/.bashrc
```

### Tab Completion Works Everywhere

Once active, tab completion works throughout the CLI:

```bash
amplifier pro<TAB>         # Completes to "profile"
amplifier profile u<TAB>   # Completes to "use"
amplifier profile use <TAB> # Shows available profiles
amplifier run --<TAB>      # Shows all options
```

## Architecture

This CLI is built using **[amplifier-foundation](https://github.com/microsoft/amplifier-foundation)**, a common library that abstracts the complexity of working with amplifier-core and its dependencies. The foundation provides:

- **Path Management** - Unified access to configuration, collections, and profiles
- **Provider Management** - Provider lifecycle, configuration, and discovery
- **Session Management** - Session persistence, spawning, and resumption
- **Module Management** - Module installation and configuration
- **Key Management** - Secure API key storage
- **Mention Loading** - @mention expansion system

The CLI layer adds:

- **Command Interface** - Rich command-line commands with Typer
- **Interactive REPL** - Multi-line chat interface with prompt_toolkit
- **TUI** - Optional text-based UI with Textual
- **Rich Output** - Beautiful console output with Rich
- **Bundled Collections** - Pre-installed expertise bundles

## Supported Providers

- **Anthropic Claude** - Recommended, most tested (Sonnet, Opus models)
- **OpenAI** - Good alternative (GPT-4o, GPT-4o-mini, o1 models)
- **Azure OpenAI** - Enterprise users with Azure subscriptions
- **Ollama** - Local, free, no API key needed

### Provider sources

`amplifier provider use …` pins the canonical module source for each
first-party provider (for example, the OpenAI provider resolves to
`git+https://github.com/microsoft/amplifier-module-provider-openai@main`).
Existing installations inherit these canonical URIs at runtime as well, so
fresh environments download the provider code via **uv** automatically. No
manual source overrides are required for the built-in providers.

## Development

### Prerequisites

- Python 3.11+
- [UV](https://github.com/astral-sh/uv) package manager

### Setup

```bash
cd amplifier-app-cli
uv pip install -e .
uv run pytest
```

### Project Structure

```
amplifier_app_cli/
├── commands/          # CLI command implementations
│   ├── provider.py    # Provider management commands
│   ├── collection.py  # Collection management commands
│   ├── init.py        # Setup wizard
│   ├── logs.py        # Log viewing
│   └── setup.py       # Additional setup commands
├── data/
│   ├── collections/   # Bundled collections (foundation, developer-expertise)
│   │   └── developer-expertise/agents/  # Default agents
│   ├── profiles/      # Profile defaults and metadata
│   └── context/       # Bundled context files
├── ui/                # Rich console components
├── tui/               # Textual UI components
├── banners/           # Banner art
├── lib/               # Wrapper modules (re-export foundation)
│   └── mention_loading/ # @mention wrappers
├── utils/             # CLI-specific utilities
│   └── mentions.py    # Mention utility wrappers
├── paths.py           # Path configuration wrapper
├── approval_provider.py # CLI-specific approval UX
└── main.py            # CLI entry point and REPL

tests/
├── TUI/               # TUI component tests
├── test_mentions.py   # Mention system tests
├── test_mention_resolver_collections.py # Collection resolution tests
├── test_repl_prompt.py # REPL tests
└── test_save_command_sanitization.py # Command tests
```

**Dependencies**:
- `amplifier-foundation` - Core functionality and abstraction layer
- `amplifier-core` - Amplifier kernel
- `typer` - CLI framework
- `rich` - Beautiful console output
- `prompt_toolkit` - REPL interface
- `textual` - TUI framework

## Documentation

**CLI-Specific Docs** (in this repo):
- [Agent Delegation](docs/AGENT_DELEGATION_IMPLEMENTATION.md) - Sub-session spawning and resumption
- [Context Loading](docs/CONTEXT_LOADING.md) - @mention system implementation
- [Interactive Mode](docs/INTERACTIVE_MODE.md) - REPL and slash commands
- [Architectural Decisions](docs/decisions/) - ADRs for major design choices

**Foundation Library** (external):
- **→ [Amplifier Foundation](https://github.com/microsoft/amplifier-foundation)** - Core library documentation

**Authoritative Guides** (external, maintained in library repos):
- **→ [Profile Authoring](https://github.com/microsoft/amplifier-profiles/blob/main/docs/PROFILE_AUTHORING.md)** - Creating and managing profiles
- **→ [Agent Authoring](https://github.com/microsoft/amplifier-profiles/blob/main/docs/AGENT_AUTHORING.md)** - Creating specialized agents
- **→ [User Onboarding](https://github.com/microsoft/amplifier/blob/next/docs/USER_ONBOARDING.md)** - Complete user guide and reference

**Toolkit** (for building sophisticated tools):
- **→ [Toolkit Guide](https://github.com/microsoft/amplifier-collection-toolkit/blob/main/docs/TOOLKIT_GUIDE.md)** - Multi-config metacognitive recipes

## Contributing

> [!NOTE]
> This project is not currently accepting external contributions, but we're actively working toward opening this up. We value community input and look forward to collaborating in the future. For now, feel free to fork and experiment!

Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit [Contributor License Agreements](https://cla.opensource.microsoft.com).

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
