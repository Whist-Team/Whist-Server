#!/bin/bash
echo "Start mongo server."
systemctl start mongod
echo "Mongo server started"

echo "Enter host address for whist server (127.0.0.1):"
read host_addr
if [ -z "$host_addr"]
then
  host_addr=127.0.0.1
fi

echo "Enter host port for whist server (8000):"
read host_port
if [ -z "$host_port"]
then
  host_port=8000
fi

echo "Enter administrator's username (admin):"
read admin_name
if [ -z "$admin_name"]
then
  admin_name="admin"
fi

echo "Enter administrator's password (admin):"
read admin_pwd
if [ -z "$admin_pwd"]
then
  admin_pwd="admin"
fi

python -m whist_server $host_addr $host_port --admin_name $admin_name --admin_pwd $admin_pwd &

exit 0