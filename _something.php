#!/usr/bin/php -q
<?php

const PI = 3.14;
const DEFAULT_D = PI;

function add($a = 0.0, $b = PI) {
	return (double) ($a + $b);
}

$a_few_numbers = [2, -1, 0, 5, 1, 4];
$l = array_map( "add", $a_few_numbers );

print_r( $l );

?>
