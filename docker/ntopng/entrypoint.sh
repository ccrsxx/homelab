#!/usr/bin/env bash

chown -R redis:redis /var/lib/redis
setsid redis-server /etc/redis/redis.conf --appendonly yes --save 60 1 &
trap "{ echo Received SIGTERM, saving redis data; redis-cli <<< save ; }" SIGTERM
trap "{ echo Received SIGINT, saving redis data; redis-cli <<< save; }" SIGINT
ntopng "$@" $NTOP_CONFIG

