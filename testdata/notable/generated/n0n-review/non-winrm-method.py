#!/usr/bin/env python3
class Session:
    def run_ps(self, text):
        print(text)
session = Session()
session.run_ps("Write-Output 'maintenance'")
