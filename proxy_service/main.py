# coding: utf-8

import logging
import time
import threading
from xmlrpc.server import SimpleXMLRPCServer

from .proxy import Proxy
from .redis_connection import redis_conn


logging.basicConfig(level=logging.INFO)

PROXYFILE = 'proxy.txt'   # put proxy.txt under same folder
MINIMUMAMOUNT = 5         # less then MINIMUMAMOUNT, call produce


class ProxyManager:
    @staticmethod
    def download_proxy():
        pass

    @staticmethod
    def initial_proxy():
        with open(PROXYFILE, 'r') as f:
            for line in f:
                # each line is like: '73.75.142.70:24635\n'
                proxy = Proxy(*line.strip().split(':'))
                proxy.add_to_pool()

    @staticmethod
    def get_a_proxy():
        if redis_conn.llen('proxies') < MINIMUMAMOUNT:
            ProxyManager.produce_proxy()

        proxy = redis_conn.brpop('proxies')[1]
        proxy = eval(proxy.decode())
        proxy = Proxy(proxy['host'], proxy['port'])

        if proxy.check_valid():
            redis_conn.lpush('proxies', proxy.__dict__)
            return proxy.__dict__
        redis_conn.srem('existed_proxies', proxy.host)
        while redis_conn.llen('proxies') > MINIMUMAMOUNT:
            time.sleep(10)
            ProxyManager.get_a_proxy()

    @staticmethod
    def produce_proxy():
        """
        When there is no proxy existed left, call this method
        """
        # 1: replace proxy.txt

        # 2: setup a thread for produce proxy
        t = threading.Thread(target=ProxyManager.initial_proxy)
        t.start()

def scrap_main():
    ProxyManager.initial_proxy()

if __name__ == '__main__':
    server = SimpleXMLRPCServer(
        ('0.0.0.0', 9898),
        logRequests=True,
    )
    server.register_function(ProxyManager.get_a_proxy, 'fetchproxy')
    server.serve_forever()

    # scrap_main()
