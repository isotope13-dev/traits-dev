#!/bin/sh
s5cmd --endpoint-url https://storage.example.test cp s3://reports/report.json /srv/reports/report.json
