#!/usr/bin/env python3
import winrm
session = winrm.Session('192.0.2.1', auth=('operator', 'example'))
session.run_cmd('whoami')
