#!/usr/bin/env python
import time
import os
from psycopg2 import connect, OperationalError

CONN_WAIT_SECONDS = float(os.environ.get('CONN_WAIT_SECONDS', 0.5))
MAX_RETRIES = int(os.environ.get('MAX_RETRIES', 20))
err = None

if __name__ == '__main__':
    conn = False
    db_name = os.environ.get('DATABASE_NAME')
    db_host = os.environ.get('DATABASE_HOST')
    db_user = os.environ.get('DATABASE_USER')
    db_password = os.environ.get('DATABASE_PASSWORD')
    for retry in range(MAX_RETRIES):
        try:
            conn = connect(
                dbname=db_name,
                user=db_user,
                host=db_host,
                password=db_password
            )
            break
        except OperationalError as e:
            err = e
            print('{}: Could not connect to the database. '
                  'Retrying in {} seconds.'
                  .format(retry, CONN_WAIT_SECONDS))
            time.sleep(CONN_WAIT_SECONDS)
    if conn:
        print('Connection established: {}.'.format(conn))
    else:
        print('Reached maximum retries, exiting.')
        raise err
