FROM redis:latest

COPY ./redis.conf /usr/local/etc/redis/redis.conf

ENTRYPOINT ["redis-server"]

CMD [ "/usr/local/etc/redis/redis.conf", "--appendonly yes"  ] 

