import os
import random

import requests

PROXIES_LIST_URL = (
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt'
)


def get_random_proxy() -> str:
    proxies = requests.get(PROXIES_LIST_URL).text.split('\n')
    proxy = random.choice(proxies)
    return proxy


def set_random_proxy():
    proxy = get_random_proxy()
    print(f'setting {proxy} as proxy')
    os.environ['http_proxy'] = proxy
