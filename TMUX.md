# 🪟 Tmux Cheatsheet & Command Reference

> **Custom configuration optimized for AI Coding Agents, Multi-Pane Workflows & Homelab Orchestration.**  
> Managed via [Chezmoi](https://www.chezmoi.io/) (`dot_tmux.conf` → `~/.tmux.conf`).

---

## ⚡ The Basics & Dual Prefix

This configuration supports **two prefix keys** interchangeably:
* **`Ctrl + a`** *(Recommended — ergonomic and fast)*
* **`Ctrl + b`** *(Default tmux fallback)*

In this guide, **`Prefix`** refers to pressing either `Ctrl + a` or `Ctrl + b`.

---

## 🤖 AI Agent Workflow Superpowers

These shortcuts are specifically configured for running and managing multiple AI agents (Claude Code, Antigravity, Aider, OpenHands, etc.):

| Shortcut | Action | Agent Use Case |
| :--- | :--- | :--- |
| **`Prefix` + `S`** | **Toggle Synchronized Panes** | Broadcast your prompt or terminal command simultaneously to **all active panes** (e.g. testing the same prompt across models or running multi-agent tasks). |
| **`Prefix` + `P`** | **Toggle Continuous Audit Logging** | Pipes the entire stdout/stderr stream of the pane into `~/.tmux/logs/%Y%m%d-%H%M%S-#S-#W-#P.log`. Perfect for compliance, audit trails, and reviewing agent actions. |
| **`Prefix` + `z`** | **Maximize / Zoom Pane** | Expands the agent's pane to full screen to inspect large code diffs or thinking traces without distraction. Press again to restore. |
| **`Alt` + `Arrows`** | **Instant Pane Switch** | Jump between agent panes immediately without typing any prefix. |
| **`Alt` + `h` `j` `k` `l` | **Vim Pane Switch** | Navigate panes using standard Vim keys without typing any prefix. |
| **`Prefix` + `\|`** | **Vertical Split (Right)** | Open a new pane side-by-side **preserving the current working directory**. |
| **`Prefix` + `-`** | **Horizontal Split (Bottom)** | Open a new pane underneath **preserving the current working directory**. |
| **`Prefix` + `x`** | **Close Pane** | Immediately closes the current pane without the annoying `kill-pane? (y/n)` confirmation prompt. |

---

## 📋 Session Management (From Normal Terminal)

Use these commands in your shell before entering or when managing tmux sessions:

```bash
# Start a new named session
tmux new -s agent-workspace

# List all running sessions
tmux ls

# Attach to an existing session
tmux attach -t agent-workspace
# or shorthand:
tmux a -t agent-workspace

# Attach to the last active session
tmux a

# Detach from inside tmux (keeps everything running in background)
# Press: Prefix + d

# Kill / Terminate a session
tmux kill-session -t agent-workspace

# Kill all tmux sessions
tmux kill-server
```

---

## 🪟 Windows (Tabs) Management

Windows behave like browser tabs inside your tmux session:

| Shortcut | Action |
| :--- | :--- |
| **`Prefix` + `c`** | Create a new window (opens in current working directory) |
| **`Prefix` + `1` .. `9`** | Switch directly to window number `1` through `9` (1-indexed) |
| **`Prefix` + `,`** | Rename current window (e.g. `claude-code`, `backend`, `monitor`) |
| **`Prefix` + `w`** | Interactive window & session picker tree |
| **`Prefix` + `n`** | Next window |
| **`Prefix` + `p`** | Previous window |
| **`Prefix` + `&`** | Kill current window |

---

## 📐 Pane Sizing & Layouts

| Shortcut | Action |
| :--- | :--- |
| **`Prefix` + `H`** | Resize pane 5 cells to the **Left** (repeatable) |
| **`Prefix` + `J`** | Resize pane 5 cells **Down** (repeatable) |
| **`Prefix` + `K`** | Resize pane 5 cells **Up** (repeatable) |
| **`Prefix` + `L`** | Resize pane 5 cells to the **Right** (repeatable) |
| **`Prefix` + `Space`** | Cycle through automated layouts (even-horizontal, even-vertical, main-horizontal, etc.) |

---

## 📜 Copy Mode, Scrolling & Universal Clipboard (OSC 52)

This configuration features a massive **100,000-line history buffer** so agent outputs are never truncated, combined with **OSC 52 clipboard synchronization** that works seamlessly over SSH, JetBrains Gateway, and Windows Terminal without X11.

### Using the Mouse
* **Scroll wheel**: Instantly enters copy mode and scrolls up through the agent's history.
* **Click & Drag**: Select text with the mouse; releasing the mouse button automatically copies the selection to your system clipboard!

### Using the Keyboard (Vi Mode)
| Shortcut | Action |
| :--- | :--- |
| **`Prefix` + `[`** | Enter scrollback / copy mode |
| **`k` / `j`** or **`↑` / `↓`** | Move cursor up / down |
| **`Ctrl` + `u` / `Ctrl` + `d`** | Scroll half page up / down |
| **`/`** | Search forward |
| **`?`** | Search backward |
| **`n` / `N`** | Next / previous search match |
| **`v`** | Begin text selection (visual mode) |
| **`Ctrl` + `v`** | Toggle rectangle / block selection |
| **`y`** | Yank (copy) selected text to system clipboard and exit copy mode |
| **`q`** or **`Escape`** | Exit copy mode |
| **`Prefix` + `]`** | Paste the internal tmux buffer |

---

## 🔄 Configuration Reload & Status Indicators

### Reload Configuration
Whenever you tweak `~/.tmux.conf`:
* Press **`Prefix` + `r`** to hot-reload the configuration. A confirmation message `✓ tmux.conf reloaded!` will briefly appear.

### Status Bar Indicators
The status bar at the bottom gives live visual feedback:
* **`󰖯 #S`** : Current Session Name (highlighted in cyan).
* **`#I: #W`** : Window index and window title.
* **`󰊓`** : Appears next to the window title when the current pane is **Zoomed** (`Prefix + z`).
* **`󰓦`** : Appears next to the window title when **Panes Synchronization** is active (`Prefix + S`).
* **`󰉋 <dir>`** : Current working directory basename.
* **`󱑍 HH:MM`** : Host system time.
* **` #H`** : Hostname of the machine (`uruk`, `jenko`, or workstation).
