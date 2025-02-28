import asyncio
import logfire
import os
import sys

from devtools import debug
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel


load_dotenv(verbose=True)

# Send logs only if LOGFIRE_TOKEN is environment variable is set.
logfire.configure(send_to_logfire="if-token-present")

llm_model = os.getenv("LLM_MODEL", "llama3.2")
ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434/v1")

model = OpenAIModel(
    model_name=llm_model,
    base_url=ollama_host,
)

agent = Agent(model=model)

try:
    prompt = sys.argv[1]
except IndexError:
    print("\nusage: python ollama_example.py <prompt>\n")
    sys.exit(1)


async def main():
    print(f"User prompt: {prompt}")
    print(f"\n========================================\n")

    response = await agent.run(prompt)
    print(response.data)

    print(f"\n========================================\n")
    print(f"Usage: {response.usage()}\n")


if __name__ == "__main__":
    asyncio.run(main())
