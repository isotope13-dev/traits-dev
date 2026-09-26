"""CI workflow helper: import shared steps from the repo's OpenShift CI
directory. `.openshift-ci` is the platform's conventional helper location,
not a concealed module directory."""

import sys

sys.path.append('.openshift-ci')

from ci_helpers import run_step


def main():
    run_step("pre-test")
