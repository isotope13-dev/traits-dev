#!/usr/bin/env bats
# E2E test for an installer script (mirrors roxagent quadlet install tests):
# ssh/scp/virtctl are recording stubs and the tests assert the argv the
# installer passes, including `-p 22`. No port is ever probed.
#
# The discovery rule must not read a mocked `-p 22` assertion as an SSH port
# availability check.

setup() {
    BIN_DIR="$(mktemp -d)"
    CALL_LOG="${BATS_TEST_TMPDIR}/calls.log"
    FAKE_ROOT="${BATS_TEST_TMPDIR}/fake-root"
    INSTALL_SCRIPT="${BATS_TEST_DIRNAME}/../../install.sh"
    export PATH="${BIN_DIR}:${PATH}"
    mkdir -p "${BIN_DIR}" "${FAKE_ROOT}"
    : > "${CALL_LOG}"
}

teardown() {
    rm -rf "${BIN_DIR}" "${FAKE_ROOT}"
}

write_recording_stub() {
    local name="$1"
    {
        echo '#!/bin/bash'
        echo "echo \"${name} \$@\" >> \"${CALL_LOG}\""
    } > "${BIN_DIR}/${name}"
    chmod +x "${BIN_DIR}/${name}"
}

write_unexpected_stub() {
    local name="$1"
    {
        echo '#!/bin/bash'
        echo "echo \"unexpected call to ${name}: \$@\" >&2"
        echo 'exit 99'
    } > "${BIN_DIR}/${name}"
    chmod +x "${BIN_DIR}/${name}"
}

call_count() {
    local name="$1"
    grep -c "^${name} " "${CALL_LOG}" || true
}

first_call_args() {
    local name="$1"
    grep "^${name} " "${CALL_LOG}" | head -n 1 | cut -d' ' -f2-
}

make_fake_virtctl() {
    local root="$1"
    {
        echo '#!/bin/bash'
        echo 'sub="$1"; shift'
        echo 'case "${sub}" in'
        echo '  ssh) echo "virtctl ssh $@" ;;'
        echo '  scp) echo "virtctl scp $@" ;;'
        echo '  *) echo "unknown virtctl subcommand: ${sub}" >&2; exit 2 ;;'
        echo 'esac'
    } > "${root}/virtctl"
    chmod +x "${root}/virtctl"
}

collect_logs() {
    local dest="$1"
    mkdir -p "${dest}"
    local f
    for f in "${BIN_DIR}"/*; do
        cp "${f}" "${dest}/" 2>/dev/null || true
    done
    tar -czf "${dest}/stubs.tar.gz" -C "${dest}" .
    ls -la "${dest}"
}

@test "--ssh without host fails with usage" {
    run bash "${INSTALL_SCRIPT}" --ssh
    assert_failure
    assert_output --partial "usage:"
}

@test "--ssh user@host invokes scp and ssh with port 22" {
    write_recording_stub ssh
    write_recording_stub scp
    run bash "${INSTALL_SCRIPT}" --ssh "testuser@10.0.0.1"
    assert_success
    # ssh should be called with -p 22
    assert_output --partial "ssh -p 22 testuser@10.0.0.1"
    assert_output --partial "scp -P 22"
    [ "$(call_count ssh)" -eq 1 ]
}

@test "--ssh user@host 2222 uses custom port" {
    write_recording_stub ssh
    write_recording_stub scp
    run bash "${INSTALL_SCRIPT}" --ssh "testuser@10.0.0.1" 2222
    assert_success
    assert_output --partial "ssh -p 2222 testuser@10.0.0.1"
}

@test "local mode never touches ssh" {
    write_unexpected_stub ssh
    write_unexpected_stub scp
    run bash "${INSTALL_SCRIPT}" --local "${FAKE_ROOT}"
    assert_success
    refute_output --partial "ssh -p 22"
    collect_logs "${FAKE_ROOT}/logs"
}

@test "virtctl mode forwards flags and target" {
    make_fake_virtctl "${BIN_DIR}"
    run bash "${INSTALL_SCRIPT}" --virtctl -n openshift-cnv --local-ssh-opts="-o StrictHostKeyChecking=no" "cloud-user@vmi/rhel10-1"
    assert_success
    # virtctl ssh should pass the flags and target
    assert_output --partial "virtctl ssh -n openshift-cnv cloud-user@vmi/rhel10-1"
    assert_output --partial "virtctl scp -n openshift-cnv --local-ssh-opts=-o StrictHostKeyChecking=no"
}
