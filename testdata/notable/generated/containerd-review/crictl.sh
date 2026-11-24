#!/bin/sh
crictl pods
crictl ps -a
crictl inspect "$container"
