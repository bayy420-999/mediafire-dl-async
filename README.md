# Mediafire Async downloader
## Usage
First, download the projects and go to projects folder
```
git clone https://github.com/bayy420-999/mediafire-dl-async.git
```
Then install dependencies by running command below in your terminal
```
pip install -r requirments.txt
```
After that, you need to setup `main.py` file and put mediafire url inside urls

Example:
```
import asyncio
from mediafire import mediafire_link_parser, mediafire_download, merge_files

async def main():
    urls = [
        'url1',
        'url2',
        'url3'
    ]

    new_urls = await mediafire_link_parser(urls) #parse direct link
    await mediafire_download(new_urls, split_chunk = 10) #download files

if __name__ == '__main__':
    asyncio.run(main())
```
Then run `main.py`
```
python main.python
```
## Additional note
You need to use python3.9+ to use this program, because i use `requests` and `asyncio.to_thread()` to make async HTTP request, and `asyncio.to_thread()` only available in python3.9+

`mediafire.py` has few functions and each function can run separately

`mediafire_link_parser()` used to get direct mediafire link, it has few paramater:

- `debug` accepting value `True/False` with `False` as default value, if you set it to `True`, it will tell you if you have broken link or if direct download link can't be founded 
- `save_results` accepting value `True/False` with `False` as default value, if you set it to `True`, the results will be saved in txt file, else it will returning the results

`mediafire_download()` used to download files from mediafire, it has few parameter:

- `split_chunk` accepting integers value, it's used to split download into multiple chunks

`merge_files()` used to merge `part file` into one file