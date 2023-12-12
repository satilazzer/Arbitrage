import time

import requests
from fake_useragent import UserAgent

ua = UserAgent()


def get_data(data, coin):
    all_exchanges = ['kucoin', 'kraken', 'binance', 'mxc', 'bybit', 'whitebit', 'gate', 'huobi', 'cex', 'bitmart',
                     'hotbit', 'coinbasepro', 'hitbtc', 'exmo']
    if not data:
        return [0, 0]
    for i in data:
        if i['base'] == coin and i['quote'] == 'USDT' and i['exchange'] in all_exchanges:
            res = [i['exchange'], i['rate']]
            return res
    return [0, 0]


def main():
    while True:
        with open('table.txt', 'w', encoding='utf-8') as file:
            file.write('')
        with open('data.txt', encoding='utf-8') as f:
            data = f.read().split(',')
        for coin in data:
            try:
                headers = {
                    'user-agent': ua.random,
                }
                offset = 0
                keep = True
                while keep:
                    r = requests.get(
                        f'https://http-api.livecoinwatch.com/markets?currency=USD&limit=30&search=USDT&offset={offset}&sort=price&order=descending&coin={coin}',
                        headers=headers)
                    time.sleep(0.5)
                    max_val = get_data(r.json()['data'], coin)
                    if max_val != [0,0]:
                        break
                    offset += 30
                    if offset < r.json()['count']:
                        continue
                    else:
                        break

                offset = 0
                keep = True
                while keep:
                    r = requests.get(
                        f'https://http-api.livecoinwatch.com/markets?currency=USD&limit=30&search=USDT&offset={offset}&sort=price&order=ascending&coin={coin}',
                        headers=headers)
                    time.sleep(0.5)
                    min_val = get_data(r.json()['data'], coin)

                    if min_val != [0,0]:
                        break
                    offset += 30
                    if offset < r.json()['count']:
                        continue
                    else:
                        break
            except Exception as ex:
                time.sleep(5)
                print(ex)
                continue

            if min_val[0] == max_val[0]:
                continue
            spread = round((max_val[1] / min_val[1] * 100) - 100, 2)
            line = f'{coin}|{max_val[0]}-{min_val[0]}|{spread}'
            print(line)
            with open('table.txt', 'a', encoding='utf-8') as file:
                file.write(line + '/')
            time.sleep(1)


if __name__ == '__main__':
    main()
