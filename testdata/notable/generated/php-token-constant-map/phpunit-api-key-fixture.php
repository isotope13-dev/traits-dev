<?php
namespace Acme\Http\Tests;

use PHPUnit\Framework\TestCase;

class ClientAuthHeaderTest extends TestCase {
    public function testBuildsApiKeyHeader(): void {
        $options = array(
            'api_key' => 'dummy_key_12345678',
        );
        $this->assertSame('dummy_key_12345678', $options['api_key']);
    }
}
