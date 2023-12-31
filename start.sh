#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


python manage.py collectstatic --noinput
python manage.py migrate

exec gunicorn config.asgi -k uvicorn.workers.UvicornWorker
