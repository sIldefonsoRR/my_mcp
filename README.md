# my_mcp

MCP server exposing city/country lookup tools, resources, and a prompt, backed by local CSV datasets (`cities.csv`, `countries.csv`).

## Features

**Tools**
- `get_city_details(country_code, city_name)` — details for a city by 2-letter country code and city name.
- `get_cities_in_country(country_code)` — list of cities in a country.

**Resources**
- `cities://countries/` — raw CSV of all countries.
- `cities://country_name/{country_code}` — country name for a 2-letter code.

**Prompts**
- `city_details(city, country_code)` — asks the model to call `get_city_details` and render the result as an HTML table.

## Requirements

- Python 3.13
- [`uv`](https://docs.astral.sh/uv/)
- `mcp`, `pydantic` (see `.venv` / project deps)

## Setup

```bash
uv venv
uv pip install mcp pydantic
```

Place `cities.csv` and `countries.csv` in the project root (already included).

## Running the server

Two transport variants are available.

**stdio** (`mcp_server.py`) — spawned per-client, no separate process to manage:

```bash
uv run --with mcp mcp run mcp_server.py
```

Or directly:

```bash
python mcp_server.py
```

**SSE** (`mcp_server_http.py`) — long-running HTTP server, listens on `127.0.0.1:8000`; must be started separately before any client connects:

```bash
python mcp_server_http.py
# Running MCP server on http://127.0.0.1:8000/sse ...
```

### Registering with an MCP client

Three client config files are included:

- `.mcp_stdio.json` — stdio, launches `mcp_server.py` via `uv run --with mcp mcp run mcp_server.py`.
- `.mcp_sse.json` — SSE, connects to `http://127.0.0.1:8000/sse`. Start `mcp_server_http.py` first — this config only connects to it, it does not launch it.
- `.mcp.json` — legacy stdio config, same shape as `.mcp_stdio.json`. Its `cwd` (`/Users/sergioildefonso/my_mcp`) doesn't match this checkout's actual path — update it before using.

## Example clients

`mcp_client.py` — minimal stdio client, starts `mcp_server.py` as a subprocess, calls tools/resources/prompts, and prints results.

```bash
python mcp_client.py
```

`mcp_client_http.py` — same calls over SSE; requires `mcp_server_http.py` already running.

```bash
python mcp_client_http.py
```

## Project structure

```
mcp_server.py        # FastMCP app (stdio): registers tools, resources, prompt
mcp_server_http.py   # FastMCP app (SSE, 127.0.0.1:8000): same registrations
operations.py        # Implementation of tools/resources/prompt + CSV loading
mcp_client.py         # Example stdio client
mcp_client_http.py    # Example SSE client
cities.csv       # City dataset (Country, City, AccentCity, Region, Population, Latitude, Longitude, ...)
countries.csv    # Country dataset (Code, Name)
.mcp_stdio.json  # MCP client config, stdio launch via uv
.mcp_sse.json    # MCP client config, connects to running SSE server
.mcp.json        # Legacy stdio config (stale cwd)
```
