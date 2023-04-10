#!/bin/sh -e

until nc -vz host:3306 > /dev/null; do
    >&2 echo "host:3306 is unavailable - sleeping"
    sleep 2
  done
  >&2 echo "host:3306 is up"

pwd
ls
python app/main.py

exit 0