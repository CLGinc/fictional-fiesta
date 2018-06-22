#!/usr/bin/env bash

# If a subcommand exists with a non 0 code the script will exit as well.
set -e

echo "------------ Waiting for db ------------"
python wait_for_db.py

echo "------------ Run DB Migrations ------------"
python manage.py migrate

exec $@
