import asyncio
import aiohttp
from aiohttp.client import ClientSession
from urllib3.exceptions import ReadTimeoutError
from requests.exceptions import ProxyError, ConnectTimeout
import requests

async def get_cur_ip(protocol: str = None, ip: str = None, port: str = None) -> str:
    try:
        url = "http://api.ipify.org?format=json"
        proxies=None
        if all([protocol, ip, port]):
            proxies={str(protocol):f"{protocol}://{ip}:{port}"}
            print(proxies)
        # print(proxies)
        ip_res = requests.get(url, timeout=10, proxies=proxies).json()["ip"]
        print(ip_res)
        # return requests.get(url, timeout=10, proxies=proxies).json()["ip"]
        return ip_res
    except (ReadTimeoutError, ConnectTimeout):
        print('time...')
    except ProxyError:
        print('proxy..')
    except BaseException as BE:
        print(BE)

async def get_ip(proxy=None)->str:
    url = "http://api.ipify.org?format=json"
    with ClientSession.get(url=url, proxy=proxy) as resp:
        print(123)
        ip = await resp.json()['ip']
        return ip


async def get_proxies():
    url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&filterUpTime=90&google=false&speed=medium&protocols=http%2Chttps&anonymityLevel=elite&anonymityLevel=anonymous"
    url = "https://www.bing.com"
    # data = requests.get(url).json()
    async with ClientSession as session:
        with session.get(url) as resp:
            proxy_list = await resp['data']
    return await proxy_list

async def main():
    real_ip = await get_cur_ip()
    connector = aiohttp.TCPConnector(limit=10)
    

# print()
# asyncio.run(get_proxies())
# asyncio.run(get_cur_ip())
# asyncio.run(get_ip())
asyncio.run(get_proxies())