import time

import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent

ua = UserAgent()

offset = 0

keep = True
while keep:
    headers = {
        'user-agent': ua.random,
    }
    all_exchanges = 'kraken,binance,bybit,coinbasepro,exmo'
    r = requests.get(
        f'https://http-api.livecoinwatch.com/coins?offset={offset}&limit=200&sort=cap&order=descending&currency=USD&exchanges=kucoin%2Ckraken%2Cbinance%2Cmxc%2Cbybit%2Cwhitebit%2Cgate%2Chuobi%2Ccex%2Cbitmart%2Chotbit%2Ccoinbasepro%2Chitbtc%2Cexmo&platforms=',
        headers=headers)
    for coin in r.json()['data']:
        if coin['cap'] == 0:
            keep = False
            break
        coin = coin['code']
        with open('data.txt', 'a', encoding='utf-8') as f:
            f.write(f"{coin.replace('_', '')},")
    time.sleep(2)
    offset += 200
