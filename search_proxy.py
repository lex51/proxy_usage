import aiohttp
import asyncio
import time

async def get_proxies():
    url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&filterUpTime=90&google=false&speed=medium&protocols=http%2Chttps&anonymityLevel=elite&anonymityLevel=anonymous"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as resp:
            proxy_list = await resp.json()
    return proxy_list['data']

async def get_ip(protocol: str = None, ip: str = None, port: str = None) -> str:
    try:
    # if True:
        url = "http://api.ipify.org?format=json"
        proxy=None
        if all([protocol, ip, port]):
            proxy = f"{protocol}://{ip}:{port}"
            # print(proxy)
        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector( ssl=False))
        async with session.get(url=url, proxy=proxy, timeout=10 ) as resp:
            ip = await resp.text()#.json()['ip']
            return ip
    except BaseException as BE:
        print(BE)

# async check_ip():

async def main():
    start_time = time.time()
    local_ip = await get_ip()
    proxy_list = await get_proxies()
    tasks = []
    for pr in proxy_list:
        # print(pr['protocols'][0], pr['ip'], pr['port'])
        task = asyncio.create_task(get_ip(pr['protocols'][0], pr['ip'], pr['port']))
        tasks.append(task)
        # print(pr['protocols'][0], pr['ip'], pr['port'])
        # ip_proxy = await get_ip(pr['protocols'][0], pr['ip'], pr['port'])
        # if pr['ip'] == ip_proxy:
        #     print(pr)
        # res = await task
        # print(res)
    results = await asyncio.gather(*tasks)
    print(results)

loop = asyncio.get_event_loop()
# loop.run_until_complete(get_proxies())
# loop.run_until_complete(get_ip())
loop.run_until_complete(main())
