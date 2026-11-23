#!/bin/sh
rabbitmqctl add_user demo "$PASSWORD"
rabbitmqctl set_permissions demo ".*" ".*" ".*"
