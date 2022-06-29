import asyncio, requests

def get_resp(url, method = None, headers = None):
    if method == 'get_html':
        return requests.get(url).text
    elif method == 'get_headers':
        return [url, requests.head(url).headers]
    elif method == 'get_content':
        if headers:
            return requests.get(url, headers = headers).content
        else:
            return requests.get(url).content
    else:
        print('Error: Wrong method!')
        exit()

async def create_request(url, method, headers = None):
    return await asyncio.to_thread(get_resp, url, method = method, headers = headers)
