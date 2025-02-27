# Pydantic AI Weather Agent

A simple agent that can use tools to get the current weather for a given location. Code was adapted from the [Weather agent](https://ai.pydantic.dev/examples/weather-agent/) example on the Pydantic AI website.

```bash
python weather_agent.py "Chicago, IL"

# => The current weather in Chicago, IL, is 36.7°F with 38% cloud cover, 94% humidity, and a wind speed of 7 mph.
```

1. You will need an OpenAI API key to run this agent.

2. You will need a Tomorrow Weather API key to get weather data. This service provides a limited-use free tier.

3. You will need a Geocode API key to get latitude and longitude data for a given location. This is a free service.

4. Create a `.env` file and update with your settings.
    ```bash
    cp .env.example .env
    ```

5. Install required Python packages.
    ```bash
    pip install -r requirements.txt
    ```

6. Run the weather agent.
    ```bash
    python weather_agent.py "Chicago, IL"
    ```

## Links and resources

- [Weather agent](https://ai.pydantic.dev/examples/weather-agent/)
- [Geocode API](https://geocode.maps.co/) - Request a free API key for up to 5,000 requests per day.
- [Tomorrow Weather API](https://www.tomorrow.io/weather-api/)
- [weather_codes.json](./weather_codes.json) was copied from [docs.tomorrow.io/reference/data-layers-weather-codes](https://docs.tomorrow.io/reference/data-layers-weather-codes).
