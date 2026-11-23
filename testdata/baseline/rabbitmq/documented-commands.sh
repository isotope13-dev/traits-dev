#!/bin/sh
echo "sudo rabbitmqctl add_user demo demo"
echo "rabbitmqctl set_permissions demo '.*' '.*' '.*'"
# rabbitmqctl add_user demo demo
