#!/usr/bin/env bash

add-apt-repository ppa:jonathonf/python-3.6
apt-get update

#Setup Locale
export LC_ALL=C
echo "export LC_ALL=C" >> /home/ubuntu/.bashrc
echo "source /home/ubuntu/scilog/bin/activate" >> /home/ubuntu/.bashrc

# Setup Nginx
apt-get install -y nginx
if ! [ -L /var/www ]; then
  rm -rf /var/www
  ln -fs /vagrant /var/www
fi


# Setup Postgres
apt-get install -y postgresql-9.5 postgresql-contrib-9.5 postgresql-server-dev-9.5

PG_VERSION=9.5
PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"

# Edit the following to change the name of the database user that will be created:
APP_DB_USER=scilog
APP_DB_PASS=scilog

# Edit the following to change the name of the database that is created (defaults to the user name)
APP_DB_NAME=scilog

# Edit postgresql.conf to change listen address to '*':
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

# Append to pg_hba.conf to add password auth:
echo "host    all             all             all                     md5" >> "$PG_HBA"

cat << EOF | sudo -u postgres psql
-- Create the database user:
CREATE USER ${APP_DB_USER} WITH PASSWORD '${APP_DB_PASS}' SUPERUSER CREATEDB;
-- Create the database:
CREATE DATABASE ${APP_DB_NAME} WITH OWNER=${APP_DB_USER}
                                  LC_COLLATE='en_US.utf8'
                                  LC_CTYPE='en_US.utf8'
                                  ENCODING='UTF8'
                                  TEMPLATE=template0;
EOF


# Setup python and virtualenv
apt-get install -y python3.6 python3.6-dev python3-pip virtualenv

# echo "export WORKON_HOME=~/.virtualenvs" >> ~/.bashrc

virtualenv -p /usr/bin/python3.6 /home/ubuntu/scilog

source /home/ubuntu/scilog/bin/activate

pip install -r /vagrant/requirements/common.txt
pip install -r /vagrant/requirements/dev.txt

deactivate
