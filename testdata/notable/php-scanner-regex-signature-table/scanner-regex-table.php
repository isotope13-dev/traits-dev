<?php

declare(strict_types=1);

namespace Example\Scanner;

defined( 'ABSPATH' ) || exit;

/**
 * Signature table for a PHP file scanner. The split in 'ev' . 'al' here is documentation, not code.
 */
final class SignatureTable {
	private const LIMIT = '(*LIMIT_MATCH=200000)';

	/** @return array<string, string> */
	public static function patterns(): array {
		return array(
			'EX-SIG-001' => '/' . self::LIMIT . 'eval\s*\(\s*base64_decode\s*\(/i',
			'EX-SIG-002' => '/' . self::LIMIT . 'system\s*\(\s*\$_GET\s*\[/i',
			'EX-SIG-003' => '/' . self::LIMIT . 'str_rot13\s*\(\s*[\'"]/i',
		);
	}

	public static function count( string $bytes ): int {
		return preg_match_all( '/' . self::LIMIT . 'eval\s*\(/i', $bytes );
	}
}
