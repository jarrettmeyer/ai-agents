import asyncio
import requests

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from typing import List
from xml.etree import ElementTree


sitemap_xml_url = "https://ai.pydantic.dev/sitemap.xml"
max_concurrent = 10


async def crawl_parallel(urls: List[str], max_concurrent: int = 3):
    print("\n=== Crawl Parallel ===")

    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )

    crawl_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

    # Create a new crawler instance.
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()
    print("\nCrawler started.")

    try:
        success_count = 0
        fail_count = 0

        # Chunk the URLs in batches.
        for idx_1 in range(0, len(urls), max_concurrent):
            batch = urls[idx_1 : idx_1 + max_concurrent]
            tasks = []

            for idx_2, url in enumerate(batch):
                # Unique session_id per concurrent sub-task
                session_id = f"parallel_session_{idx_1}_{idx_2}"
                task = crawler.arun(url=url, config=crawl_config, session_id=session_id)
                tasks.append(task)

            # Gather results
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Evaluate results
            for url, result in zip(batch, results):
                if result.success:
                    success_count += 1
                else:
                    if isinstance(result, Exception):
                        print(f"Error crawling {url}: {result}")
                    fail_count += 1

        print(f"\nSummary:")
        print(f"\t- Successfully crawled: {success_count}")
        print(f"\t- Failed: {fail_count}")
    finally:
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
        await crawl_parallel(urls, max_concurrent=max_concurrent)
    else:
        print("No URLs to crawl.")


if __name__ == "__main__":
    asyncio.run(main())