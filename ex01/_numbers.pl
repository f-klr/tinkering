#!/usr/bin/perl -w

use strict;
use warnings qw(all);

###
package main;
#

use List::Util qw(shuffle reduce first);

sub _take {
	my $md5 = qx!head -c 512 /dev/random | md5 -q!;
	chomp($md5);
	return unpack("(a2)*", $md5);
}

my @a_few_numbers = ();
for (1 .. 10) {
	my @list = map { hex '0x' . $_ } _take;
	push @a_few_numbers, (first { $_ < 30 } shuffle @list) || 0;
}

stdout->say( join(', ', @a_few_numbers), " ->(+) ", reduce { $a + $b } @a_few_numbers );
stdout->say( "\n" );
