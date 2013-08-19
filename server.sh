#!/bin/bash

case "$1" in
"start")
./manage.py runfcgi method=prefork host=127.0.0.1 port=15055 pidfile=/tmp/lmdb_server.pid
;;
"stop")
kill -9 `cat /tmp/lmdb_server.pid`
;;
"restart")
$0 stop
sleep 1
$0 start
;;
*) echo "Usage: ./server.sh {start|stop|restart}";;
esac