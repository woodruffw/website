#!/usr/bin/env perl

use strict;
use warnings;

use LWP::Simple qw(get);
use XML::Simple;
use CGI qw(:standard);
use HTML::Scrubber;

my $scrubber = HTML::Scrubber->new;

my $attendance_url = "http://schools.nyc.gov/aboutus/data/attendancexml/";
my $school_id = $scrubber->scrub(param('schoolname')) || shift || "none found";

my $school_name;
my $school_attn;

my $xml_data = get($attendance_url);
my $decoded_xml_data = XMLin($xml_data);

foreach (@{$decoded_xml_data->{'item'}}) {
	if (($_->{'SCHOOL_NAME'} eq uc($school_id)) || ($_->{'DBN'} eq uc($school_id)))
	{
		$school_name =  "School: " . $_->{'SCHOOL_NAME'};
		$school_attn = "Attendance: " . $_->{'ATTN_PCT'} . "% as of " . split_date($_->{'ATTN_DATE_YMD'}) . "\n";
		last;
	}

	else
	{
		$school_name = "School: " . $school_id;
		$school_attn = "Attendance: Unknown";
	}
}

sub split_date
{
	return substr($_[0], 4, 2) . "/" . substr($_[0], 6, 2) . "/" . substr($_[0], 0, 4);
}


print "Content-type: text/html\n\n";
print <<EOHTML
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>School Attendance</title>
	<style type="text/css">
		body
		{
			font-family: "Times New Roman", Georgia, Serif;
			text-align: center;
		}

		div
		{
			text-align: left;
		}
	</style>
</head>
<body>
	<div>
	<a href="/index.html">Home</a>
	</div>

	<h1>Results</h1>
	<p>
	$school_name <br>
	$school_attn
	<p>
</body>
</html>
EOHTML

