import asyncio
import crawl4ai
import requests

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from typing import List
from xml.etree import ElementTree


sitemap_xml_url = "https://ai.pydantic.dev/sitemap.xml"


async def crawl_sequential(urls: List[str]):
    print("\n=== Crawl Sequential ===")

    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )

    crawl_config = CrawlerRunConfig(markdown_generator=DefaultMarkdownGenerator())

    # Create a new crawler instance.
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()
    print("\nCrawler started.")

    try:
        session_id = "session_1"

        for url in urls:
            result = await crawler.arun(url=url, config=crawl_config, session_id=session_id)
            if result.success:
                print(f"Successfully crawled: {url}")
                print(f"Markdown length: {len(result.markdown_v2.raw_markdown)}")
            else:
                print(f"Failed to crawl: {url}; Error: {result.error}")
    finally:
        # Clean up resources.
        print("\nClosing crawler...")
        await crawler.close()
        print("\nCrawler closed.")


def get_urls():
    try:
        response = requests.get(sitemap_xml_url)
        response.raise_for_status()

        root = ElementTree.fromstring(response.content)

        ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [loc.text for loc in root.findall(".//ns:loc", ns)]

        return urls
    except Exception as e:
        print(f"Failed to fetch sitemap.xml: {e}")
        return []


async def main():
    urls = get_urls()
    if urls:
        print(f"Found {len(urls)} URLs to crawl.")
        await crawl_sequential(urls)
    else:
        print("No URLs to crawl.")


if __name__ == "__main__":
    asyncio.run(main())