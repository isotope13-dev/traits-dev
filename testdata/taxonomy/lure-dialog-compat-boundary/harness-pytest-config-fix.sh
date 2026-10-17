#!/bin/bash
# First, fix the pytest compatibility issue by updating setup.cfg
sed -i 's/^\[pytest\]$/[tool:pytest]/' setup.cfg
pytest tests/ -x -q
