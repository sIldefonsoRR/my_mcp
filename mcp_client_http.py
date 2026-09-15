import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

SERVER_URL = "http://127.0.0.1:8000/sse"

async def main() -> None:
    # connection (server must already be running: python mcp_server_http.py)
    async with sse_client(SERVER_URL) as (read, write):
        # session
        async with ClientSession(read, write) as session:
            await session.initialize()

            # command
            country_code = "pt"
            city_name = "Faro"
            result = await session.call_tool(
                "get_city_details",
                {"country_code": country_code, "city_name": city_name, }
            )
            result = result.content[0].text
            print(result)

            # command
            result = await session.read_resource(
                "cities://countries/",
            )
            result = result.contents[0].text
            print(result)

            # command
            country_code = "pt"
            city_name = "Faro"
            result = await session.get_prompt(
                "city_details",
                {"city": city_name, "country_code": country_code, },
            )
            result = result.messages
            for message in result:
                print(message.content.text)

asyncio.run(main())
