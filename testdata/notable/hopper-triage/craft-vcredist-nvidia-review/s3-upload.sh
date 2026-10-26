#!/bin/sh
s5cmd --endpoint-url https://storage.example.test cp /srv/reports/report.json s3://reports/report.json
