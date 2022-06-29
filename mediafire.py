import asyncio, aiofiles, shutil, re, os
from requests_async import create_request

def merge_files():
    part_files = sorted(list(os.listdir('temp')))
    filenames = {f.split('-')[0] for f in part_files}

    for filename in filenames:
        with open(f'results/{filename}', 'wb+') as output_file:
            for part_file in part_files:
                with open(f'temp/{part_file}', 'rb') as temp_file:
                    output_file.write(temp_file.read())
    shutil.rmtree('temp')

async def downloader(url, filename, **kwargs):
    if kwargs:
        try:
            os.mkdir('temp')
        except FileExistsError:
            pass
            
        filename = f'{filename}-{kwargs.get("idx")}.tmp'
        resp = await create_request(url, 'get_content', headers = kwargs.get("headers"))
        print(f'Filename: {filename} Part: {kwargs.get("idx")} downloaded!')
        filepath = os.path.join('temp', filename)
    else:
        try:
            os.mkdir('results')
        except FileExistsError:
            pass

        filepath = os.path.join('results', filename)
        resp = await create_request(url, 'get_content')
        print(f'Filename: {filename} downloaded!')

    async with aiofiles.open(filepath, mode = 'wb') as f:
        await f.write(resp)
    
async def mediafire_link_parser(urls, debug = False, save_results = False):
    if debug and save_results not in [True, False]:
        print('Error: You passing incorrect argument')
        exit()

    results = []
    datas = await asyncio.gather(*[create_request(url, 'get_html') for url in urls])
    for data in zip(urls, datas):
        direct_download_url = re.search(r'href\=\"(.*?)\"\sid\=\"downloadButton\"\>', data[1])
        try:
            results.append({'original_url':data[0], 'direct_download_url': direct_download_url[1]})
        except TypeError:
            results.append({'original_url':data[0], 'direct_download_url': None})

    for result in results:
        if debug == True:
            print(f'original_url: {result["original_url"]} | direct_download_url: {result["direct_download_url"]}')
        elif debug == False:
            print('Debugging disabled')

        if save_results == True:
            with open('results.txt', 'a') as f:
                if result["direct_download_url"] != None:
                    f.write(f'{result["direct_download_url"]}\n')
        elif save_results == False:
            return [result["direct_download_url"] for result in results if result["direct_download_url"] != None]

async def mediafire_download(urls, max_download = None, split_chunk = None, content_disposition = True):
    tasks = []
    datas = await asyncio.gather(*[create_request(url, 'get_headers') for url in urls])

    for url, data in datas:
        try:
            filename = re.search(r'filename\=\"(.*?)\"', data['Content-Disposition'].encode('iso-8859-1').decode('utf-8'))[1]
        except TypeError:
            raise TypeError('File doesn\'t exists')

        if filename != None:
            size = int(data['Content-Length'])

        if type(split_chunk) == int:
            sections = [[0, 0] for _ in range(split_chunk)]
            each_size = size // split_chunk
            print(f"Each size is {each_size} bytes")
            for idx, _ in enumerate(sections):
                sections[idx][0] = 0 if idx == 0 else sections[idx - 1][1] + 1
                if idx < split_chunk - 1:
                    sections[idx][1] = sections[idx][0] + each_size
                else:
                    sections[idx][1] = size - 1

            for idx, section in enumerate(sections):
                headers = {'Range': f"bytes={section[0]}-{section[1]}"}
                tasks.append(downloader(url, filename, idx = idx, headers = headers))
        else:
            tasks.append(downloader(url, filename))

    await asyncio.gather(*tasks)
    try:
        merge_files()
    except FileNotFoundError:
        pass