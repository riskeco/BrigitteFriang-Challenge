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

#print map { "$_ : $distribution[$_]\n" } (0..255);
#exit;

$level[$#level+1] = 'unknown';
my $bits = '';
my $string = '';
my $lost_sync;

for (my $i=0;$i<$#raw;$i++)
{
	$front[$i] = '';
	$duration++;
	$duration[$i] = $duration;
	my $byte_limit = '';
	if ($level[$i] ne $level[$i+1])	# Front.
	{
		$front[$i] = "front";
		$bit_count[$i] = ($duration / 638);
		$bits .= $level[$i] x int($bit_count[$i]);
		$front_count += $bit_count[$i];
		if ($front_count >= 11)
		{
			$bits = substr($bits, 0, 11);
			$bits =~ s/\A(\d)(\d+)(\d)(\d)\Z/$1 $2 $3 $4/;

			my $start_bit = $1;
			my $data_bits = $2;
			my $parity_bit = $3;
			my $stop_bit = $4;

			my $byte_value = pack('b8', $data_bits);

			$data_bits =~ s/0//g;

			if ($start_bit == 1 || $stop_bit == 0 || (length($data_bits)+$parity_bit)%2 != 0 )
			{
				$lost_sync = 'lost sync or parity error';
			}
			else
			{
				$string .= $byte_value;
				$lost_sync='';
			}


			$byte_limit = "byte limit $bits /$byte_value/ /$string/ $lost_sync";
			$front_count = 0;
			if ($bits eq '0 00000000 0 0')
			{
				$front_count = 1;
				$bits = '0';
				printf "#%06u: value=%03u level=%s duration=%06u %-5s bit_count=%f %s\n", $i, $raw[$i], $level[$i], $duration[$i], $front[$i], (defined $bit_count[$i]?$bit_count[$i]:0), $byte_limit;
				print "Resync after 0 00000000 0 0\n";
				next;
			}
			$bits = '';
		}
		$duration = 0;
	}
	printf "#%06u: value=%03u level=%s duration=%06u %-5s bit_count=%f %s\n", $i, $raw[$i], $level[$i], $duration[$i], $front[$i], (defined $bit_count[$i]?$bit_count[$i]:0), $byte_limit;
}

