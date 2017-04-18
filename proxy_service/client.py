import xmlrpc.client

conn = xmlrpc.client.ServerProxy('http://localhost:9898')

proxy = conn.fetchproxy()
# print(proxy)       {'host': '46.105.121.37', 'port': '6493'}

status = conn.status()
# print(status)      {'existed_proxy': 26, 'hours': 0, 'file_time': '2017-04-18 21:00:00', 'alive_proxy': 50}
