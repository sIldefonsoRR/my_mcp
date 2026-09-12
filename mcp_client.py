import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

params = StdioServerParameters(command="python", args=["mcp_server.py"])

async def main() -> None:
    # connection
    async with stdio_client(params) as (read, write):
        # session
        async with ClientSession(read, write) as session:
            await session.initialize()

            # # command
            # country_code = "pt"
            # city_name = "Faro"
            # result = await session.call_tool(
            #     "get_city_details",
            #     {"country_code": country_code, "city_name": city_name, }
            # )            
            # result = result.content[0].text
            # print(result)

            # command
            # result = await session.read_resource(
            #     "cities://countries/",
            # )            
            # result = result.contents[0].text
            # print(result)

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


