import asyncio
import crawl4ai


async def main():
    url = "https://ai.pydantic.dev/"
    async with crawl4ai.AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        print(result.markdown)


if __name__ == "__main__":
    asyncio.run(main())