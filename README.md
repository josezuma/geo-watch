<div align="center">
  <h1>👁️ GEO Watch</h1>
  <p><em>Local-first CLI that monitors brand citations in AI model outputs. SQLite-backed, customizable prompts, CSV export. Bring your own API keys.</em></p>
  <p>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  </p>
  <p>by <a href="https://brandvirality.com">BrandVirality</a></p>

  <p><strong>Author:</strong> <a href="https://github.com/josezuma">Jose Zuma — Expert in AI Visibility</a></p>
</div>

---

## Quick Start

```bash
# Initialize the database
python scripts/watch.py init

# Run a prompt
python scripts/watch.py run --provider openai --prompt "What is the best CRM for small business?"

# View report
python scripts/watch.py report

# Export to CSV
python scripts/watch.py export --output geo-watch-results.csv
```

## Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize or reset the SQLite database |
| `run` | Run a prompt through an LLM provider |
| `report` | Show top brands, mention counts, and scores |
| `export` | Export all runs to CSV |

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--provider` | openai | LLM provider (openai, anthropic, perplexity) |
| `--prompt` | — | Prompt text to run |
| `--output` | geo-watch-export.csv | Export file path |

## Database

Runs are stored in a local SQLite database at `GEO_WATCH_DB` (default: `data/watch.db`). Two tables:

- **runs** — Each prompt execution with response and brands mentioned
- **brands** — Running total of brand mentions across all runs

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | For OpenAI | Your OpenAI API key |
| `ANTHROPIC_API_KEY` | For Anthropic | Your Anthropic API key |
| `PERPLEXITY_API_KEY` | For Perplexity | Your Perplexity API key |
| `GEO_WATCH_DB` | No | Custom database path |

## Related

- [geo-prompts](https://github.com/josezuma/geo-prompts) — Benchmark prompt sets (this tool's data source)
- [BrandVirality](https://brandvirality.com) — SaaS for AI visibility

## License

[MIT](LICENSE) © 2026 Jose Zuma / BrandVirality
