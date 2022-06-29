import asyncio
from mediafire import mediafire_link_parser, mediafire_download, merge_files

async def main():
    urls = []

    new_urls = await mediafire_link_parser(urls) #parse direct link
    await mediafire_download(new_urls, split_chunk = 10) #download files

if __name__ == '__main__':
    asyncio.run(main())