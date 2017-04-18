# coding: utf-8
import os
import logging
import time
import threading
import multiprocessing
import datetime
from xmlrpc.server import SimpleXMLRPCServer
from collections import namedtuple
import schedule

from proxy_service.helpers import send_wechat_reminder
from proxy_service.proxy import Proxy
from proxy_service.redis_connection import redis_conn

logging.basicConfig(level=logging.INFO)

PROXYFILE = os.getcwd() + '/proxy.txt'  # put proxy.txt under same folder
MINIMUMAMOUNT = 5           # less then MINIMUMAMOUNT, call produce
TIMETOUPDATEPROXYFILE = 6   # each 6 hour to replace proxy.txt


class ProxyManager:
    @staticmethod
    def download_proxy():
        pass

    @staticmethod
    def exist_proxy_fiel(remind_me=False):
        if not os.path.exists(PROXYFILE) and remind_me:
            send_wechat_reminder('No proxy.txt', 'you naughty', 'hurry hurry up', '')
            return False
        return True

    @staticmethod
    def initial_proxy():
        if not ProxyManager.exist_proxy_fiel(remind_me=True):
            while not ProxyManager.exist_proxy_fiel():
                time.sleep(60)

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
        # 1: TODO: auto replace proxy.txt

        # 2: setup a thread for produce proxy
        if 'produce_proxy_thread' not in [t.name for t in threading.enumerate()]:
            t = threading.Thread(target=ProxyManager.initial_proxy, name='produce_proxy_thread')
            t.start()

    @staticmethod
    def pool_status():
        alive_proxy = redis_conn.llen('proxies')
        existed_proxy = redis_conn.scard('existed_proxies')
        file_time = datetime.datetime.fromtimestamp(os.stat(PROXYFILE).st_ctime)
        gap = datetime.datetime.now() - file_time
        hour_gap = gap.seconds // 3600

        ProxyStatus = namedtuple('ProxyStatus', ['alive_proxy', 'existed_proxy', 'file_time', 'hours'])
        proxy_status = ProxyStatus(alive_proxy, existed_proxy, str(file_time).split('.')[0], hour_gap)
        return proxy_status

    @staticmethod
    def self_check():
        status = ProxyManager.pool_status()
        if status.hours > TIMETOUPDATEPROXYFILE:
            # write your warning here
            send_wechat_reminder('proxypool', 'replace file', '', '')
            return
        if status.alive_proxy < MINIMUMAMOUNT:
            ProxyManager.produce_proxy()

    @staticmethod
    def show_status():
        status = ProxyManager.pool_status()
        return dict(status._asdict())


def scrap_main():
    ProxyManager.initial_proxy()


def schedule_run_forever():
    schedule.every(40).minutes.do(ProxyManager.self_check)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    p = multiprocessing.Process(target=schedule_run_forever, name='schedule_process')
    p.start()

    server = SimpleXMLRPCServer(
        ('0.0.0.0', 9898),
        logRequests=True,
    )
    server.register_function(ProxyManager.get_a_proxy, 'fetchproxy')
    server.register_function(ProxyManager.show_status, 'status')
    server.serve_forever()

    # scrap_main()
