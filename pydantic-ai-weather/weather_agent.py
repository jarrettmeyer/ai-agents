import asyncio
import json
import os
import sys

from dataclasses import dataclass
from devtools import debug
from dotenv import load_dotenv
from httpx import AsyncClient as AsyncHttpxClient
from pydantic_ai import Agent, ModelRetry, RunContext
from typing import Any, Literal


load_dotenv()
# debug(os.getenv("LOGFIRE_IGNORE_NO_CONFIG"))

# Get the location.
try:
    location = sys.argv[1]
except IndexError:
    print("\nusage: python weather_agent.py <location>\n")
    sys.exit(1)


@dataclass
class WeatherDeps:
    httpx_client: AsyncHttpxClient
    geocode_api_key: str
    geocode_endpoint: str
    weather_api_key: str
    weather_endpoint: str
    weather_units: Literal["imperial", "metric"]


@dataclass
class LatLon:
    lat: float
    lon: float


# Read the system prompt.
with open("system_prompt.md") as f:
    system_prompt = f.read()

# Read weather codes from JSON source.
with open("weather_codes.json") as f:
    weather_codes = json.load(f)


weather_agent = Agent(
    model=os.getenv("LLM_MODEL", "openai:gpt-4o"),
    system_prompt=system_prompt,
    deps_type=WeatherDeps,
    retries=2,
)


@weather_agent.tool
async def get_lat_lon(c: RunContext[WeatherDeps], address: str) -> LatLon:
    """Get the latitude and longitude of an address.

    Args:
        c: Run context.
        address: The address or description of a location.
    """

    # TODO: Look for the lat/lon in a local cache before making API call.

    if c.deps.geocode_api_key is None:
        raise ValueError("Geocode API key is required.")

    query_params = {
        "q": address,
        "api_key": c.deps.geocode_api_key,
    }

    response = await c.deps.httpx_client.get(c.deps.geocode_endpoint, params=query_params)
    response.raise_for_status()
    data = response.json()
    # debug(data)

    # TODO: Cache this result locally.

    if data:
        return LatLon(lat=data[0]["lat"], lon=data[0]["lon"])
    else:
        raise ModelRetry(f"Could not find lat/lon for address '{address}'.")


@weather_agent.tool
async def get_weather(c: RunContext[WeatherDeps], lat: float, lon: float) -> Any:
    """Get the current weather at a given latitude and longitude.

    Args:
        c: Run context.
        lat: Location latitude.
        lon: Location longitude.
    """

    # TODO: Look for the weather data in a local cache before making API call.

    if c.deps.weather_api_key is None:
        raise ValueError("Weather API key is required.")

    params = {
        "apikey": c.deps.weather_api_key,
        "location": f"{lat}, {lon}",
        "units": c.deps.weather_units,
    }

    response = await c.deps.httpx_client.get(c.deps.weather_endpoint, params=params)
    response.raise_for_status()
    data = response.json()
    # debug(data)

    # TODO: Cache this result locally.

    return data["data"]["values"]


@weather_agent.tool
def lookup_weather_code(c: RunContext[WeatherDeps], weather_code: int) -> str:
    """Lookup the friendly text description for a weather code.

    Args:
        c: Run context.
        weather_code: Weather code to lookup.
    """
    return weather_codes.get(str(weather_code), "Unknown")


async def main():
    async with AsyncHttpxClient() as client:
        deps = WeatherDeps(
            httpx_client=client,
            geocode_api_key=os.getenv("GEOCODE_API_KEY"),
            geocode_endpoint=os.getenv("GEOCODE_API_ENDPOINT"),
            weather_api_key=os.getenv("WEATHER_API_KEY"),
            weather_endpoint=os.getenv("WEATHER_API_ENDPOINT"),
            weather_units="imperial",
        )

        response = await weather_agent.run(f"What is the weather in {location}?", deps=deps)
        # debug(response)

        print(f"\n\n{response.data}\n")


if __name__ == "__main__":
    asyncio.run(main())
