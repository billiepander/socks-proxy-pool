## socks-proxy-pool
a socks proxy pool in redis, touch it trough python xmlrpc moudule

## clone it
    ~$: git clone git@github.com:billiepander/socks-proxy-pool.git  
    ~$: cd socks-proxy-pool  
    ~/socks-proxy-pool: 


## download the socks proxies
1. visit http://www.gatherproxy.com/zh/sockslist[* you need proxy to visit it] and download the socks list fiel,
It take to find this awesome & free socks proxy provider website, it holds 1500 free socks proxies in average
2. rename the file to proxy.txt
3. replace my proxy.txt with it  

[^_^]:
    I tried to download it automaticly, but as my proxy is not that stable
    and the download the proxy once can use whole day for my situation,
    so I choose to download it manually.


[^_^]:
    of course you can add your own proxy source into that file, and please recommend me the proxy provider if if that rocks

    
## run redis
1. build docker image  
    ~/socks-proxy-pool/docker_redis: sudo docker build -t *redis_6388* .  
2. start redis  
    ~/socks-proxy-pool/docker_redis: sudo docker run -d -v ~/socks-proxy-pool/docker_redis/Data:/Data --name *c_redis_6388* -p 6388:6388 --net="host" -it *redis_6388*

now redis is running on your "0.0.0.0:6388" with password "yourpasswd"  
you can change that in ~/socks-proxy-pool/docker_redis/redis.conf


## run python service
1. build docker image  
    ~/socks-proxy-pool/proxy_service: docker build -t proxypool .
2. start service  
    ~/socks-proxy-pool/proxy_service: docker run --name c_proxypool -p 9898:9898 --net="host" -ti proxypool  
now proxy service is running on your "0.0.0.0:9898" 

<br><br>
_ _ _
by now, all the server side work is done, bellow will talk about usage in your client python file
_ _ _
<br><br>
## fetch a proxy

    import xmlrpc.client  
    conn = xmlrpc.client.ServerProxy('http://yourhost:9898')  
    proxy = conn.fetchproxy()
    # proxy is a valid socks proxy as dict
    # e.g: {'host': '46.105.121.37', 'port': '6493'}

## get proxy pool status

    import xmlrpc.client
    conn = xmlrpc.client.ServerProxy('http://yourhost:9898')
    status = conn.status()
    # status is proxy pool status as dict
    # {'existed_proxy': 26, 'hours': 0, 'file_time': '2017-04-18 21:00:00', 'alive_proxy': 50}


## TODO
...
