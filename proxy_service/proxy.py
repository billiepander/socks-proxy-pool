import requests
from proxy_service.redis_connection import redis_conn


class Proxy:
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def check_valid(self):
        proxies = {
            'http': "socks5://{host}:{port}".format(host=self.host, port=self.port),
            'https': "socks5://{host}:{port}".format(host=self.host, port=self.port),
        }
        try:
            requests.get('http://httpbin.org/ip', proxies=proxies, headers=Proxy.header, timeout=4).json()
            return True
        except requests.Timeout:
            return False
        except:
            # do some log here
            return False

    def ready_into_pool(self):
        # anyitem in should_fail_list return True means the proxy cannot join pool
        should_fail_list = [
            redis_conn.sismember('failed_proxies', self.host),
            # failed_proxies does not mean its not valid, but maybe your target web blocked this ip
            redis_conn.sismember('existed_proxies', self.host)
            # add your custom check here
        ]
        return False if any(should_fail_list) else True

    def add_to_pool(self):
        if self.check_valid() and self.ready_into_pool():
            redis_conn.lpush('proxies', self.__dict__)
            redis_conn.sadd('existed_proxies', self.host)
