import xmlrpc.client

conn = xmlrpc.client.ServerProxy('http://localhost:9898')

proxy = conn.fetchproxy()
