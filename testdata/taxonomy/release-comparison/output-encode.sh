#!/bin/bash
id | base64
cat "$CONFIG" | base64
{ echo ready; } | base64
