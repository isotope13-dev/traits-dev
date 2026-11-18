#!/usr/bin/env bash
# Mocked issue-tracker workflow state ids; completing an issue is not cleanup.
jq -e '.variables.input.stateId == "state-done"' "$payload" >/dev/null
state_of_id='{"state-done": {"name": "Done", "type": "completed"}}'
