# Build-converter shape (cf. upb tools/make_cmakelists.py in grpcio): the
# converter interprets checked-in Bazel files by exec'ing them into stub
# namespaces at module scope to harvest rules. Explicit local-input
# interpreter behavior, not a concealed import-time payload.
"""Convert Bazel build files between formats."""

rules = []


def _stub_cc_library(name, srcs):
    rules.append((name, list(srcs)))


def _stub_workspace(name):
    rules.append((name, []))


workspace = {"workspace": _stub_workspace}
exec(open("WORKSPACE").read(), workspace)

build = {"cc_library": _stub_cc_library}
exec(open("BUILD").read(), build)
