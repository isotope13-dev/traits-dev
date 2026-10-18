#!/bin/bash
# append BASH_ENV=/tmp/example to $GITHUB_ENV is dangerous
env -u GITHUB_ENV worker
