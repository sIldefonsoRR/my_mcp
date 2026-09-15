# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A small MCP (Model Context Protocol) server exposing city/country lookup tools, resources, and a prompt, backed by two local CSV datasets (`cities.csv`, `countries.csv`). Built with `FastMCP` from the `mcp` Python package.

## Commands

Setup:
```bash
uv venv
uv pip install mcp pydantic
```

Run the server directly:
```bash
python mcp_server.py
```

Run via the MCP CLI (what `.mcp.json` uses for stdio clients):
```bash
uv run --with mcp mcp run mcp_server.py
```

Exercise it with the example client (spawns the server as a subprocess over stdio):
```bash
python mcp_client.py
```

There is no test suite, linter config, or build step in this repo — a `.ruff_cache/` exists but there is no `ruff.toml`/`pyproject.toml` configuring it.

## Architecture

Three-file split, all tools/resources/prompt are plain functions wired up declaratively:

- `operations.py` — all logic. Loads `cities.csv` into memory once at import time (module-level `_cities` list of dicts via `csv.DictReader`); `countries.csv` is read fresh on each call inside `get_countries`/`country_name`. Defines the tool/resource/prompt implementations as plain functions with `pydantic.Field(...)` default values used purely for MCP parameter descriptions (not runtime validation).
- `mcp_server.py` — the `FastMCP` app. Imports functions from `operations.py` and registers them via `mcp.tool(...)`, `mcp.resource(...)`, `mcp.prompt(...)`. This is the only place that wires names/descriptions/URIs to implementations — when adding a new capability, implement it in `operations.py` then register it here.
- `mcp_client.py` — minimal example stdio client (not used by the server itself); scratch file with commented-out alternative calls, useful as a reference for calling tools/resources/prompts programmatically.

Key data-shape details to know before touching `operations.py`:
- `cities.csv` rows use lowercase 2-letter country codes in the `Country` column and an ASCII `City` column plus an accented `AccentCity` column; `get_city_details` matches case-insensitively against `City` after stripping accents from the input via `_normalize_city_name` (NFD decompose + drop combining marks), but does **not** normalize `_cities`' own `AccentCity`/`City` values the same way beyond `.lower()` — matching is only case-insensitive, not accent-insensitive on both sides beyond what's already ASCII in `City`.
- `get_cities_in_country` compares `Country` case-sensitively (unlike `get_city_details`), so it expects a lowercase country code to match the CSV.
- `countries.csv` uses a capitalized 2-letter `Code` column; `country_name` matches case-insensitively.
- `.mcp.json`'s `cwd` is hardcoded to `/Users/sergioildefonso/my_mcp`, which does not match this repo's actual location (`/Users/sergioildefonso/Learning/Anthropic/my_mcp`) — update it if registering this server with an MCP client from this checkout.
