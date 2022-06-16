#!/bin/bash -e

export PORT
VIRTUALENV_BASE="${VIRTUALENV_BASE:-/virtualenv}"

case "$1" in
    deploy)
        ./manage.py migrate --no-input  # Migrate database
        ./manage.py loaddata auth_fixture # Load our fixture
        ;;

    install-deps)
        . ./app.sh start-env
        poetry install --no-dev
        ;;

    start-env)
        if [ -z "$VIRTUAL_ENV" ]; then
            if [ ! -f "$VIRTUALENV_BASE/bin/activate" ]; then
                echo "Creating virtualenv"
                python -m venv --system-site-packages "$VIRTUALENV_BASE"
            fi
            # squash SC1090. We dont want to lint the source here
            # shellcheck source=/dev/null
            . "$VIRTUALENV_BASE/bin/activate"
        fi
        ;;

    *)
        echo Unknown command
        exit 1
        ;;
esac
