#!/usr/bin/perl -w

use strict;
use warnings qw(all);

###
package main;
#

use Iterator::Util;
use Data::Entropy::RawSource::RandomnumbersInfo;
use Digest::SHA qw(sha256_base64);

my $info = Data::Entropy::RawSource::RandomnumbersInfo->new;

sub _getRandomCode {
	my $data;
	$info->read($data, 1024);
	return join '-' => unpack("(a4)*", sha256_base64($data));
}

for my $i (ihead 10, (irange 0)) {
	print "$i: ";
	print _getRandomCode();
	print "\n";
}
