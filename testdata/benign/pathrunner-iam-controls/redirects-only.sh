#!/bin/bash
exec > >(tee /tmp/audit.log) 2>&1
exec 3<>/tmp/control
