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

```bash
uv run --with mcp mcp run mcp_server.py
```

Or directly:

```bash
python mcp_server.py
```

### Registering with an MCP client

`.mcp.json` already configures this server for stdio clients:

```json
{
  "mcpServers": {
    "my_mcp_server": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "--with", "mcp", "mcp", "run", "mcp_server.py"],
      "cwd": "/Users/sergioildefonso/my_mcp"
    }
  }
}
```

## Example client

`mcp_client.py` shows a minimal stdio client that starts the server as a subprocess, calls tools/resources/prompts, and prints results.

```bash
python mcp_client.py
```

## Project structure

```
mcp_server.py    # FastMCP app: registers tools, resources, prompt
operations.py    # Implementation of tools/resources/prompt + CSV loading
mcp_client.py    # Example stdio client
cities.csv       # City dataset (Country, City, AccentCity, Region, Population, Latitude, Longitude, ...)
countries.csv    # Country dataset (Code, Name)
.mcp.json        # MCP client config for stdio launch via uv
```
