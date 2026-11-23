#!/bin/sh
sudo rabbitmqctl add_user operator "inline-pass"
$SUDO rabbitmqctl set_permissions operator '.*' '.*' '.*'
systemctl enable --now application.service
