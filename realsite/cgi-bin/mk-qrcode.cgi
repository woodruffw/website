#!/usr/bin/env perl

use strict;
use warnings;

use Imager::QRCode;
use CGI;
use HTML::Scrubber;

my $cgi = CGI->new;
my $scrubber = HTML::Scrubber->new;
my $size = 5;
my $data = $scrubber->scrub($cgi->param('qrtext'));
my $qr = Imager::QRCode->new(size => $size, level => 'H', casesensitive => 1);
my $img = $qr->plot($data);

print $cgi->header('image/png');
$img->write(fh => \*STDOUT, type => 'png');
