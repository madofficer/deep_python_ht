import asyncio
import argparse
import aiohttp
from aiohttp import ClientError
from aiofiles import open as aio_open


async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            content = await response.text()
            print(f"Fetching {url} as response")
            return content
    except Exception as e:
        print(f"Failed to fetch url {url}: {e}")
        return None


async def process_urls(file_path, max_concurrent_req):
    semaphore = asyncio.Semaphore(max_concurrent_req)

    async def process_line(line):
        url = line.strip()
        if not url:
            return
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                await fetch_url(session, url)

    async with aio_open(file_path, mode="r") as f:
        tasks = []
        async for line in f:
            task = asyncio.create_task(process_line(line))
            tasks.append(task)

            if len(tasks) > max_concurrent_req * 2:
                await asyncio.gather(*tasks)
                tasks = []

            if tasks:
                await asyncio.gather(*tasks)


def parse_fetcher_args():
    parser = argparse.ArgumentParser(
        description="Async server for fetching URL"
    )
    parser.add_argument(
        "-f", "--file", type=str, required=True, help="File path to urls"
    )
    parser.add_argument(
        "-c", "--concurrent", type=int, default=10, help="Max queries at once"
    )
    return parser.parse_args()


def main():
    args = parse_fetcher_args()
    asyncio.run(process_urls(args.file, args.concurrent))


if __name__ == "__main__":
    main()
