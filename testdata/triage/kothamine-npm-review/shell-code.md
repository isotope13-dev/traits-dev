#!/bin/sh
: <<'DOC'
## Install

```shell
$ npm install example
```
DOC
result=`id`
printf '%s\n' "$result"
