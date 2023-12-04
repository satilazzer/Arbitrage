from django.shortcuts import render
import requests
import json

from django.views.decorators.csrf import csrf_exempt
from fake_useragent import UserAgent

ua = UserAgent()


def main(request):
    with open('table.txt', encoding='utf-8') as f:
        table = f.read().split('/')[0:-1]
    res = [[i.split('|')[0], i.split('|')[1], i.split('|')[2]] for i in table]
    return render(request, 'main/index.html', {'data': res})


b'0=BTC&0=cex-kucoin&0=0.41&0=ETH&0=coinbasepro-kraken&0=0.15&0=BNB&0=bitmart-kucoin&0=0.07'
