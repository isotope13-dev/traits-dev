package com.example.policies

import spock.lang.Specification

// Policy-name table: the suite names the builtin policies it asserts on.
// A "Crontab Execution" row names the policy; it installs no cron entry.
class BuiltinPolicies extends Specification {
    def "builtin policy names"() {
        expect:
        policies.contains("crontab Execution")
    }
}
