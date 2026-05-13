# PromptForge

Lightweight Terminal AI Prompt Manager & Optimizer

## Installation

```bash
pip install -e .
```

## Usage

```bash
promptforge add --title "My Prompt" --content "..." --tags "tag1,tag2"
promptforge list --category coding --sort score
promptforge search "Python"
promptforge show <id>
promptforge score <id>
promptforge export <id> --format md
promptforge stats
promptforge tui
```

## Features

- Zero external dependencies (Python standard library only)
- SQLite storage
- TF-IDF search engine
- Multi-dimensional quality scoring
- Multi-format export (JSON/YAML/Markdown)
- TUI interactive dashboard
- Version management
