<?php
// Benign control: old-style PHPUnit security test. Attack strings below are
// quoted regression vectors for the eval sandbox, part of this security test.
class SecurityVectorsTest extends PHPUnit_Framework_TestCase
{
	public function testEvalRejectsReversedSystem()
	{
		$result = (string) victim_eval("strrev('metsys') ('whoami')", 1, 1);
		$this->assertEquals('', $result);
	}
	public function testEvalRejectsWhoami()
	{
		$s = 'new abc->invoke(\'whoami\')';
		$this->assertNotContains('whoami', victim_eval($s, 1, 1));
		$this->assertTrue(true, 'whoami must never execute');
	}
}
