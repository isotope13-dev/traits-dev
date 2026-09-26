package com.example.ast

import groovy.transform.ASTTest
import org.codehaus.groovy.control.CompilePhase
import spock.lang.Specification

// AST-transform test: the annotation under test is the fixture, not a
// parse-time payload.
class RetryTest extends Specification {
    @ASTTest(value = { true }, phase = CompilePhase.SEMANTIC_ANALYSIS)
    def "retry works"() {
        expect:
        true
    }
}
