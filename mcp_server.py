from mcp.server.fastmcp import FastMCP
from operations import (
    get_city_details,
    get_cities_in_country,
    get_countries,
    country_name,
    get_city_details_prompt,
)


mcp = FastMCP("cities mcp")

# region TOOLS
mcp.tool(
    name="get_city_details",
    description="Gets the detais of a city from a country code and the city name.",
)(get_city_details)


mcp.tool(
    name="get_cities_in_country",
    description="Gets a list of the cities of a country.",
)(get_cities_in_country)
# endregion TOOLS

# region RESOURCES
mcp.resource("cities://countries/", mime_type="text/csv")(get_countries)

mcp.resource("cities://country_name/{country_code}", mime_type="text/plain")(
    country_name
)

# endregion RESOURCES

#region MCP Prompts
mcp.prompt(
    name="city_details",
    description="Gathers detailed information about a city and returns it formatted in an HTML table.",
)(get_city_details_prompt)
#endregion MCP Prompts

if __name__ == "__main__":
    print("Running MCP server...")
    mcp.run()
