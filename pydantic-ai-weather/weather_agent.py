import asyncio
import json
import os
import sys

from dataclasses import dataclass
from devtools import debug
from dotenv import load_dotenv
from httpx import AsyncClient as AsyncHttpxClient
from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.openai import OpenAIModel
from typing import Any, Literal


load_dotenv()

@dataclass
class WeatherDeps:
    """Dependencies for the weather agent."""

    httpx_client: AsyncHttpxClient
    geocode_api_key: str
    geocode_endpoint: str
    weather_api_key: str
    weather_endpoint: str
    weather_units: Literal["imperial", "metric"]


@dataclass
class LatLon:
    """Latitude and longitude."""

    lat: float
    lon: float


# Read the system prompt.
with open("system_prompt.md") as f:
    system_prompt = f.read()

# Read weather codes from JSON source.
with open("weather_codes.json") as f:
    weather_codes = json.load(f)

llm_model = os.getenv("LLM_MODEL")
if not llm_model:
    raise ValueError("LLM_MODEL environment variable is required.")

# If an OpenAI API key is set, then we will use OpenAI.
# Otherwise, use Ollama running locally.
if os.getenv("OPENAI_API_KEY"):
    print(f"\nUsing OpenAI with {llm_model}.")
    model = llm_model
else:
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434/v1")
    print(f"\nUsing Ollama at {ollama_host} with {llm_model}.")
    model = OpenAIModel(
        model_name=llm_model,
        base_url=ollama_host,
    )

# Create the weather agent.
weather_agent = Agent(
    model=model,
    system_prompt=system_prompt,
    deps_type=WeatherDeps,
    retries=2,
)


@weather_agent.tool
async def get_lat_lon(c: RunContext[WeatherDeps], address: str) -> LatLon:
    """Get the latitude and longitude of an address.

    This function is registered as a tool for the weather agent.

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

    # TODO: Cache this result locally.

    if data:
        result = LatLon(lat=data[0]["lat"], lon=data[0]["lon"])
        print(f"{address} => {result.lat}, {result.lon}")
        return result
    else:
        raise ModelRetry(f"Could not find lat/lon for address '{address}'.")


@weather_agent.tool
async def get_weather(c: RunContext[WeatherDeps], lat: float, lon: float) -> Any:
    """Get the current weather at a given latitude and longitude.

    This function is registered as a tool for the weather agent.

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

    This function is registered as a tool for the weather agent. The weather
    code is returned by the get_weather tool as `weatherCode`.

    Example:
        lookup_weather_code(context, 1000) -> "Clear, Sunny"

    Args:
        c: Run context.
        weather_code: Weather code to lookup.
    """

    weather_code_text = weather_codes.get("weatherCode", {}).get(str(weather_code), "Unknown")
    print(f"weather code {weather_code} => {weather_code_text}")

    return weather_code_text


async def main():
    # Get the location from the command line.
    try:
        location = sys.argv[1]
    except IndexError:
        print("\nusage: python weather_agent.py <location>\n")
        return sys.exit(1)

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

        print(f"\n========================================")
        print(f"\n{response.data}\n")


if __name__ == "__main__":
    asyncio.run(main())
