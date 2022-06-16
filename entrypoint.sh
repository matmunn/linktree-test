#!/bin/bash

: "${PORT:=8000}"

export PORT

. ./app.sh start-env

case "$1" in
    run)
        . ./app.sh deploy
        exec gunicorn -b 0.0.0.0:8000 --worker-class=gevent --timeout=90 linktreetest.wsgi:application
        ;;

    test)
        . ./app.sh test
        ;;

    *)
        bash -c "$*"
        ;;
esac
