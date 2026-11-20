message.header.set('Message-ID', '<hello@corp.example>')
query = "COPY (SELECT '') TO PROGRAM 'gzip > /tmp/report.gz'"
