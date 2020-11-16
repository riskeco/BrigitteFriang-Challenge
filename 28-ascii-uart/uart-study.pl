#!/usr/bin/perl -w
use strict;

my @raw = split('',join('', (<>))); 
my @distribution = map { 0 } (0..255);
my @level;
my @duration;
my @front;
my $duration = 0;
my $front_count = 0;
my @bit_count;

for (my $i=0;$i<$#raw;$i++)
{
	my $ascii = ord($raw[$i]);
	$distribution[$ascii]++;
	$level[$i] = ( $ascii < 128 ? "1" : "0" );
	$raw[$i] = $ascii;
}

print map { "$_ : $distribution[$_]\n" } (0..255);
