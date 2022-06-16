#!/bin/bash

: "${PORT:=8000}"

export PORT

. ./app.sh start-env

case "$1" in
    run)
        . ./app.sh deploy
        exec gunicorn -b 0.0.0.0:8000 linktreetest.wsgi:application
        ;;

    *)
        bash -c "$*"
        ;;
esac
