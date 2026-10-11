#!/bin/sh
echo "rm -rf $HOME/.ssh"
rm -rf /tmp/staging; echo $HOME/.ssh
rm -rf "$HOME/.ssh/known_hosts"
rm -rf '$HOME/.aws'
