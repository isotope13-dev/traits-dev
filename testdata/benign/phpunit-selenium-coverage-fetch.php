<?php
// Minimized PHPUnit_Selenium RemoteCoverage pattern: fetches serialized
// code-coverage from the operator-configured coverage URL of the system
// under test, then unserializes the response.
class PHPUnit_Extensions_SeleniumCommon_RemoteCoverage
{
    public function __construct($coverageScriptUrl, $testId)
    {
        $this->coverageScriptUrl = $coverageScriptUrl;
        $this->testId = $testId;
    }

    public function get()
    {
        if (!empty($this->coverageScriptUrl)) {
            $url = sprintf(
              '%s?PHPUNIT_SELENIUM_TEST_ID=%s',
              $this->coverageScriptUrl,
              $this->testId
            );

            $buffer = file_get_contents($url);

            if ($buffer !== FALSE) {
                $coverageData = unserialize($buffer);
                if (is_array($coverageData)) {
                    return $coverageData;
                } else {
                    throw new Exception('Empty or invalid code coverage data received from url "' . $url . '"');
                }
            }
        }

        return array();
    }
}
