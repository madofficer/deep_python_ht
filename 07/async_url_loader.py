import aiohttp
import asyncio
import argparse
from aiohttp import ClientError


async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            print(f"Fetched {url}: {response.status}")
            return await response.text()
    except ClientError as e:
        print(f"Failed to fetch {url}: {e}")
        return None


async def fetch_all(urls, concurrency):
    semaphore = asyncio.Semaphore(concurrency)

    async def fetch_with_semaphore(session, url):
        async with semaphore:
            return await fetch_url(session, url)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_semaphore(session, url) for url in urls]
        return await asyncio.gather(*tasks)


def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]


def main():
    parser = argparse.ArgumentParser(description="Async URL Fetcher")
    parser.add_argument("concurrency", type=int, help="Количество одновременных запросов")
    parser.add_argument("file", type=str, help="Путь к файлу со списком URL-ов")

    args = parser.parse_args()
    concurrency = args.concurrency
    file_path = args.file

    urls = read_urls_from_file(file_path)
    print(f"Found {len(urls)} URLs to fetch.")

    asyncio.run(fetch_all(urls, concurrency))


if __name__ == "__main__":
    main()
