#!/usr/bin/env perl

use warnings;
use strict;

use CGI qw(:standard);
use HTML::Scrubber;

my $scrubber = HTML::Scrubber->new;

my $username = $scrubber->scrub(param('pausername')) || "Unknown";
my $password = $scrubber->scrub(param('papassword')) || "Unknown";
	
open(FILE, ">>/Users/admin/website-mgmt/account-requests.txt");
print FILE $username, ":", $password, "\n";
close(FILE);
	
print "Content-type: text/html\n\n";
print <<EOHTML
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>Request processed</title>
	<style type="text/css">
		body
		{
			text-align: center;
			font-family: "Times New Roman", Georgia, Serif;
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
		<h1>Thank you $username!</h1>
	<p>Your request has been processed.</p>
</body>
</html>
EOHTML
