<?php

#
# a simple example of php code, we redefine a few "functional" style operations,
# that is array-oriented functions.
#

define("N", 10);
define("EOL", "\n");

function println(string $s) {
	if ($s) {
		print($s);
	}
	print(EOL);
}

function __range(int $a, int $b = -1) {
	if ($b == -1) {
		$b = $a - 1;
		$a = 0;
	}
	$l = array();
	for ($i = $a; $i <= $b; $i++) {
		array_push($l, $i);
	}
	return $l;
}

function __reduce(array $items, callable $cb, $init = null) {
	$r = $init ? $init : array_shift($items);
	foreach ($items as $x) {
		$r = call_user_func($cb, $r, $x);
	}
	return $r;
}

function add2(int $a, int $b) {
	return $a + $b;
}

function sqr2(int $a, int $b) {
	return $a + $b*$b;
}

function cat2(string $a, string $b, string $sep = "-") {
	return $a . $sep . $b;
}

# TODO: define a partial function to add two, or an array of strings, given a "SEP" -

$l = __range(2, N);
echo __reduce($l, "add2"), "\n";
echo __reduce($l, "sqr2"), "\n";

echo __reduce(array("one", "two", "three"), "cat2"), "\n";

?>
