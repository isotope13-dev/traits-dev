"""Historical installer: PyArmor recovery is now maintained by filefacts.

The original outer-container prototype and fixtures remain with this audit for
reproducibility. Reinstalling them would replace the current nested-code decoder
with the obsolete Cleave-local implementation.
"""
raise SystemExit(
    "Do not reinstall this prototype. Use filefacts::pyarmor and Cleave's "
    "archive/pyarmor_members.rs companion-runtime routing. See "
    "docs/taxonomy-audit/triage/python-good-20261030/pyarmor-recovery.md."
)
