import asyncio
import os
from crawl4ai import AsyncWebCrawler

async def main():
    os.makedirs("data", exist_ok=True)

    async with AsyncWebCrawler() as crawler:
        # You can replace or extend these URLs
        urls = [
            "https://www.healthline.com/nutrition",
            "https://www.verywellfit.com/",
            "https://www.webmd.com/fitness-exercise"
        ]
        for i, url in enumerate(urls):
            result = await crawler.arun(url=url)
            # Save markdown content per source
            fname = f"data/fitness_{i+1}.md"
            with open(fname, "w", encoding="utf-8") as f:
                f.write(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())
