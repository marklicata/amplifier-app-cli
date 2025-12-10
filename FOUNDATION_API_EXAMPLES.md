# Amplifier Foundation - API Examples

This document shows concrete examples of how the foundation library will be used.

---

## Example 1: Minimal App (50 lines)

**Goal:** Show simplest possible amplifier app

```python
"""minimal.py - A minimal Amplifier application"""
import asyncio
from amplifier_foundation import create_provider_manager, create_config_manager
from amplifier_core import AmplifierSession

async def main():
    # Setup provider if not configured
    providers = create_provider_manager()
    if not providers.get_current_provider():
        print("First time setup:")
        api_key = input("Anthropic API key: ")
        providers.use_provider(
            "provider-anthropic",
            scope="global",
            config={"api_key": api_key, "default_model": "claude-sonnet-4"}
        )
    
    # Resolve configuration
    from amplifier_foundation import resolve_app_config, create_profile_loader
    config_mgr = create_config_manager()
    profile_loader = create_profile_loader()
    
    config = resolve_app_config(
        config_manager=config_mgr,
        profile_loader=profile_loader,
        app_settings=None,  # Use defaults
    )
    
    # Create and run session
    session = AmplifierSession(config=config)
    await session.initialize()
    
    response = await session.execute("Explain quantum computing in simple terms")
    print(response)
    
    await session.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

**Result:** Working amplifier app in 40 lines.

---

## Example 2: Interactive REPL (100 lines)

**Goal:** Build a simple interactive app with session persistence

```python
"""repl.py - Interactive Amplifier REPL with session persistence"""
import asyncio
from amplifier_foundation import (
    create_config_manager,
    create_provider_manager,
    create_profile_loader,
    create_session_store,
    resolve_app_config,
)
from amplifier_core import AmplifierSession

class AmplifierREPL:
    def __init__(self):
        self.config_mgr = create_config_manager()
        self.provider_mgr = create_provider_manager(self.config_mgr)
        self.profile_loader = create_profile_loader()
        self.session_store = create_session_store()
        
    async def run(self):
        # Check provider
        if not self.provider_mgr.get_current_provider():
            print("No provider configured. Run setup first.")
            return
        
        # Resolve config
        config = resolve_app_config(
            config_manager=self.config_mgr,
            profile_loader=self.profile_loader,
            app_settings=None,
        )
        
        # Create session
        session = AmplifierSession(config=config, session_id="repl-session")
        await session.initialize()
        
        print("Amplifier REPL (type 'exit' to quit, 'save' to persist)\n")
        
        try:
            while True:
                prompt = input("You: ").strip()
                
                if not prompt:
                    continue
                if prompt.lower() == 'exit':
                    break
                if prompt.lower() == 'save':
                    await self.save_session(session)
                    print("Session saved!")
                    continue
                
                response = await session.execute(prompt)
                print(f"AI: {response}\n")
        
        finally:
            await session.cleanup()
    
    async def save_session(self, session: AmplifierSession):
        """Save session to storage"""
        context = session.coordinator.get("context")
        transcript = await context.get_messages() if context else []
        
        metadata = {
            "session_id": session.session_id,
            "config": session.config,
        }
        
        self.session_store.save(session.session_id, transcript, metadata)

if __name__ == "__main__":
    repl = AmplifierREPL()
    asyncio.run(repl.run())
```

**Result:** Full REPL with persistence in 80 lines.

---

## Example 3: CLI Command Using Foundation

**Goal:** Show how CLI commands become simpler

### Before (Current CLI Implementation)

```python
# amplifier-app-cli/amplifier_app_cli/commands/provider.py (simplified)
from pathlib import Path
from amplifier_config import ConfigManager, Scope
from ..paths import get_cli_config_paths, validate_scope_for_write
from ..provider_manager import ProviderManager
from ..provider_sources import get_effective_provider_sources
from ..lib.app_settings import AppSettings

@click.command()
@click.argument("provider")
@click.option("--scope", type=click.Choice(["local", "project", "global"]))
@click.option("--api-key")
@click.option("--model")
def use(provider: str, scope: str, api_key: str, model: str):
    """Configure a provider"""
    # Setup paths
    paths = get_cli_config_paths()
    config = ConfigManager(paths=paths)
    
    # Validate scope
    scope = validate_scope_for_write(scope or "local", config)
    
    # Build config
    provider_config = {}
    if api_key:
        provider_config["api_key"] = api_key
    if model:
        provider_config["default_model"] = model
    
    # Get sources
    sources = get_effective_provider_sources(config)
    
    # Configure
    manager = ProviderManager(config)
    result = manager.use_provider(
        provider_id=f"provider-{provider}",
        scope=scope,
        config=provider_config,
        source=sources.get(f"provider-{provider}")
    )
    
    console.print(f"✓ Configured {result.provider} at {result.scope}")
```

### After (Using Foundation)

```python
# amplifier-app-cli/amplifier_app_cli/commands/provider.py (simplified)
from amplifier_foundation import create_provider_manager

@click.command()
@click.argument("provider")
@click.option("--scope", type=click.Choice(["local", "project", "global"]))
@click.option("--api-key")
@click.option("--model")
def use(provider: str, scope: str, api_key: str, model: str):
    """Configure a provider"""
    # Build config
    provider_config = {}
    if api_key:
        provider_config["api_key"] = api_key
    if model:
        provider_config["default_model"] = model
    
    # Configure via foundation
    manager = create_provider_manager()
    result = manager.use_provider(
        provider_id=f"provider-{provider}",
        scope=scope or "local",
        config=provider_config,
    )
    
    console.print(f"✓ Configured {result.provider} at {result.scope}")
```

**Reduction:** ~40 lines → ~20 lines (50% reduction)

---

## Example 4: Building a GUI App

**Goal:** Show foundation enables non-CLI apps easily

```python
"""gui_app.py - Simple Tkinter GUI using foundation"""
import asyncio
import tkinter as tk
from tkinter import scrolledtext, messagebox
from amplifier_foundation import (
    create_config_manager,
    create_provider_manager,
    create_profile_loader,
    resolve_app_config,
)
from amplifier_core import AmplifierSession

class AmplifierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Amplifier GUI")
        
        # Foundation components
        self.config_mgr = create_config_manager()
        self.provider_mgr = create_provider_manager(self.config_mgr)
        self.profile_loader = create_profile_loader()
        
        # Check provider
        if not self.provider_mgr.get_current_provider():
            messagebox.showerror("Error", "No provider configured. Run CLI setup first.")
            self.root.destroy()
            return
        
        # UI setup
        self.setup_ui()
        
        # Session setup
        self.session = None
        asyncio.create_task(self.initialize_session())
    
    def setup_ui(self):
        # Input area
        tk.Label(self.root, text="Prompt:").pack(pady=5)
        self.input_text = scrolledtext.ScrolledText(self.root, height=5)
        self.input_text.pack(padx=10, pady=5, fill=tk.BOTH)
        
        # Send button
        self.send_btn = tk.Button(self.root, text="Send", command=self.on_send)
        self.send_btn.pack(pady=5)
        
        # Output area
        tk.Label(self.root, text="Response:").pack(pady=5)
        self.output_text = scrolledtext.ScrolledText(self.root, height=15)
        self.output_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    
    async def initialize_session(self):
        """Initialize amplifier session using foundation"""
        config = resolve_app_config(
            config_manager=self.config_mgr,
            profile_loader=self.profile_loader,
            app_settings=None,
        )
        
        self.session = AmplifierSession(config=config)
        await self.session.initialize()
        self.send_btn.config(state=tk.NORMAL)
    
    def on_send(self):
        """Handle send button click"""
        prompt = self.input_text.get("1.0", tk.END).strip()
        if not prompt:
            return
        
        self.send_btn.config(state=tk.DISABLED)
        asyncio.create_task(self.execute_prompt(prompt))
    
    async def execute_prompt(self, prompt: str):
        """Execute prompt and display response"""
        try:
            response = await self.session.execute(prompt)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", response)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.send_btn.config(state=tk.NORMAL)

# Async Tkinter integration
def run_async_tkinter(root):
    """Run Tkinter with asyncio event loop"""
    async def tk_loop():
        while True:
            root.update()
            await asyncio.sleep(0.01)
    
    asyncio.run(tk_loop())

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x500")
    app = AmplifierGUI(root)
    run_async_tkinter(root)
```

**Result:** GUI app in ~100 lines using foundation.

---

## Example 5: Web API Server

**Goal:** RESTful API using foundation

```python
"""api_server.py - FastAPI server using foundation"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from amplifier_foundation import (
    create_config_manager,
    create_provider_manager,
    create_profile_loader,
    create_session_store,
    resolve_app_config,
)
from amplifier_core import AmplifierSession
import asyncio

app = FastAPI(title="Amplifier API")

# Foundation setup
config_mgr = create_config_manager()
provider_mgr = create_provider_manager(config_mgr)
profile_loader = create_profile_loader()
session_store = create_session_store()

# Cache for active sessions
active_sessions: dict[str, AmplifierSession] = {}

class PromptRequest(BaseModel):
    prompt: str
    profile: str = "default"
    session_id: str | None = None

class PromptResponse(BaseModel):
    response: str
    session_id: str

@app.post("/execute", response_model=PromptResponse)
async def execute_prompt(request: PromptRequest):
    """Execute a prompt with optional session persistence"""
    
    # Check provider
    if not provider_mgr.get_current_provider():
        raise HTTPException(status_code=400, detail="No provider configured")
    
    # Get or create session
    session_id = request.session_id or f"api-{asyncio.current_task().get_name()}"
    
    if session_id in active_sessions:
        session = active_sessions[session_id]
    else:
        # Resolve config
        config = resolve_app_config(
            config_manager=config_mgr,
            profile_loader=profile_loader,
            app_settings=None,
            profile_override=request.profile,
        )
        
        # Create new session
        session = AmplifierSession(config=config, session_id=session_id)
        await session.initialize()
        active_sessions[session_id] = session
    
    # Execute
    response = await session.execute(request.prompt)
    
    # Persist if session_id was provided
    if request.session_id:
        context = session.coordinator.get("context")
        transcript = await context.get_messages() if context else []
        session_store.save(session_id, transcript, {"config": session.config})
    
    return PromptResponse(response=response, session_id=session_id)

@app.get("/providers")
async def list_providers():
    """List available providers"""
    providers = provider_mgr.list_providers()
    return {"providers": [{"id": p[0], "name": p[1]} for p in providers]}

@app.get("/sessions")
async def list_sessions():
    """List stored sessions"""
    sessions = session_store.list_sessions()
    return {"sessions": sessions}

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    # Clean up active session
    if session_id in active_sessions:
        await active_sessions[session_id].cleanup()
        del active_sessions[session_id]
    
    # No filesystem deletion in this example, but you could add it
    return {"status": "deleted", "session_id": session_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Result:** REST API in ~120 lines using foundation.

---

## Example 6: Testing Apps Built with Foundation

**Goal:** Show how foundation enables easy testing

```python
"""test_my_app.py - Testing an app built with foundation"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from amplifier_foundation import (
    create_config_manager,
    create_provider_manager,
    SessionStore,
)

@pytest.fixture
def mock_config(tmp_path):
    """Mock configuration for testing"""
    with patch('amplifier_foundation.paths.Path.home') as mock_home:
        mock_home.return_value = tmp_path
        config = create_config_manager()
        yield config

@pytest.fixture
def mock_provider_manager(mock_config):
    """Mock provider manager"""
    manager = create_provider_manager(mock_config)
    return manager

def test_provider_configuration(mock_provider_manager):
    """Test provider can be configured"""
    result = mock_provider_manager.use_provider(
        provider_id="provider-anthropic",
        scope="global",
        config={"api_key": "test-key", "default_model": "claude-sonnet-4"}
    )
    
    assert result.provider == "provider-anthropic"
    assert result.scope == "global"
    
    current = mock_provider_manager.get_current_provider()
    assert current is not None
    assert current.module_id == "provider-anthropic"

def test_session_persistence(tmp_path):
    """Test session can be saved and loaded"""
    store = SessionStore(base_dir=tmp_path / "sessions")
    
    # Save session
    transcript = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    metadata = {"session_id": "test-123", "config": {}}
    
    store.save("test-123", transcript, metadata)
    
    # Load session
    loaded_transcript, loaded_metadata = store.load("test-123")
    
    assert len(loaded_transcript) == 2
    assert loaded_transcript[0]["content"] == "Hello"
    assert loaded_metadata["session_id"] == "test-123"

@pytest.mark.asyncio
async def test_session_execution(mock_config):
    """Test session execution with mocked provider"""
    from amplifier_foundation import resolve_app_config, create_profile_loader
    from amplifier_core import AmplifierSession
    
    profile_loader = create_profile_loader()
    
    # Mock the provider to return test response
    with patch('amplifier_core.providers.anthropic.AnthropicProvider.generate') as mock_generate:
        mock_generate.return_value = "Test response"
        
        config = resolve_app_config(
            config_manager=mock_config,
            profile_loader=profile_loader,
            app_settings=None,
        )
        
        session = AmplifierSession(config=config)
        await session.initialize()
        
        response = await session.execute("Test prompt")
        
        assert response == "Test response"
        await session.cleanup()
```

**Result:** Clean, testable code with foundation abstractions.

---

## Example 7: Advanced - Custom Path Policy

**Goal:** Show how to customize foundation for specialized needs

```python
"""custom_app.py - App with custom directory structure"""
from pathlib import Path
from amplifier_foundation import ConfigPaths, create_config_manager

# Define custom path policy
custom_paths = ConfigPaths(
    user=Path("/opt/myapp/config/settings.yaml"),
    project=Path(".myapp/config.yaml"),
    local=None,  # Disable local scope
)

# Create config manager with custom paths
config = create_config_manager(paths=custom_paths)

# Use foundation components normally
from amplifier_foundation import create_provider_manager

provider_mgr = create_provider_manager(config)
current = provider_mgr.get_current_provider()
print(f"Current provider: {current.module_id if current else 'None'}")
```

**Result:** Foundation is flexible enough for custom requirements.

---

## Summary: API Patterns

### Pattern 1: Factory Functions (Recommended)
```python
from amplifier_foundation import create_config_manager, create_provider_manager

config = create_config_manager()  # Sensible defaults
providers = create_provider_manager(config)
```

### Pattern 2: Manager Classes (Explicit)
```python
from amplifier_foundation import ConfigManager, ProviderManager
from amplifier_foundation.paths import get_cli_config_paths

paths = get_cli_config_paths()
config = ConfigManager(paths=paths)  # Explicit configuration
providers = ProviderManager(config)
```

### Pattern 3: High-Level Application (Coming)
```python
from amplifier_foundation import Application

app = Application()  # Everything configured
session = await app.create_session()
```

---

## Key Takeaways

1. **Simple by Default:** Most apps can use factories with defaults
2. **Explicit When Needed:** Custom paths/config available when required
3. **Testable:** Easy to mock and test with standard patterns
4. **Reusable:** Same code works for CLI, GUI, API, etc.
5. **Type-Safe:** Full type hints enable IDE autocomplete and type checking

---

*These examples demonstrate the ergonomics and flexibility of the proposed foundation API.*
