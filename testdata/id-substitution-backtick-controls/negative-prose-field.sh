#!/bin/sh
# Task queue record: every queued record carries an `id`, a `text` body,
# and a state (`queued` | `picked` | `dropped`). Advance the card with
# `todo done <t-id>` once its evidence file exists under .reports/.
ls "$QUEUE_DIR"
