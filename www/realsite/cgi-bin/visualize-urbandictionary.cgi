#!/usr/bin/env perl

#  visualize-urbandictionary.pl
#  Author: William Woodruff
#  ------------------------
#  Grabs data from Urban Dictionary's JSON API, visualizing it using Chart.js.
#  ------------------------
#  Depends on JSON, LWP::Simple, CGI, and HTML::Scrubber.
#  ------------------------
#  Public domain.

use LWP::Simple;
use JSON qw(decode_json);
use CGI;
use HTML::Scrubber;

my $cgi = CGI->new;
my $scrubber = HTML::Scrubber->new;

my $query = $scrubber->scrub($cgi->param('udquery') || "empty");

my $urban_url = "http://api.urbandictionary.com/v0/define?term=" . $query;

my $data = get($urban_url);
my $decoded_data = decode_json($data);
my @defs = @{$decoded_data->{'list'}};
my $num_defs = scalar @defs;
my $tags = "@{$decoded_data->{'tags'}}";
my $tags = join(", ", @{$decoded_data->{'tags'}});

if ($num_defs == 10)
{
	print "Content-type: text/html\n\n";
	print <<EOHTML
	<!DOCTYPE html>
	<html>
	<head>
		<meta charset="UTF-8">
		<title>Urban Dictionary Visualization</title>
		<script src="/realsite/res/libs/Chart.min.js"></script>
		<style type="text/css">
			body
			{
				font-family: "Times New Roman", Georgia, Serif;
				text-align: center;
			}
		</style>
	</head>
	<body>
		<h1>Results for "<a href="http://www.urbandictionary.com/define.php?term=$query">$query</a>"</h1>
		<h2>Most popular answer (by user: $defs[0]->{'author'})</h2>
		<p>$defs[0]->{'definition'}<p>
		<h2>Top 10 Most Popular Visualization</h2>
		<p>Clockwise, in terms of "thumbs ups."</p>
		<canvas id="pop-canvas" height="600" width="600"></canvas>
		<h2>Top 10 Least Popular Visualization</h2>
		<p>Clockwise, in terms of "thumbs downs."</p>
		<canvas id="unpop-canvas" height="600" width="600"></canvas>
		<h2>Similar tags</h2>
		<p>$tags</p>
		<script>
			var data = [
				{
					value: $defs[0]->{'thumbs_up'},
					color: "#42EF98"
				},
				{
					value: $defs[1]->{'thumbs_up'},
					color: "#598e1e"
				},
				{
					value: $defs[2]->{'thumbs_up'},
					color: "#0800cd"
				},
				{
					value: $defs[3]->{'thumbs_up'},
					color: "#4d7aba"
				},
				{
					value: $defs[4]->{'thumbs_up'},
					color: "#6ef34f"
				},
				{
					value: $defs[5]->{'thumbs_up'},
					color: "#5f56eb"
				},
				{
					value: $defs[6]->{'thumbs_up'},
					color: "#fd179c"
				},
				{
					value: $defs[7]->{'thumbs_up'},
					color: "#0e5e7f"
				},
				{
					value: $defs[8]->{'thumbs_up'},
					color: "#363912"
				},
				{
					value: $defs[9]->{'thumbs_up'},
					color: "#ea1d35"
				},
			];

			var pie = new Chart(document.getElementById("pop-canvas").getContext("2d")).Pie(data);

			var data = [
				{
					value: $defs[0]->{'thumbs_down'},
					color: "#42EF98"
				},
				{
					value: $defs[1]->{'thumbs_down'},
					color: "#598e1e"
				},
				{
					value: $defs[2]->{'thumbs_down'},
					color: "#0800cd"
				},
				{
					value: $defs[3]->{'thumbs_down'},
					color: "#4d7aba"
				},
				{
					value: $defs[4]->{'thumbs_down'},
					color: "#6ef34f"
				},
				{
					value: $defs[5]->{'thumbs_down'},
					color: "#5f56eb"
				},
				{
					value: $defs[6]->{'thumbs_down'},
					color: "#fd179c"
				},
				{
					value: $defs[7]->{'thumbs_down'},
					color: "#0e5e7f"
				},
				{
					value: $defs[8]->{'thumbs_down'},
					color: "#363912"
				},
				{
					value: $defs[9]->{'thumbs_down'},
					color: "#ea1d35"
				},
			];

			var pie = new Chart(document.getElementById("unpop-canvas").getContext("2d")).Pie(data);
		</script>
	</body>
	</html>
EOHTML
}

else
{
	print "Content-type: text/html\n\n";
	print <<EOHTML
	<!DOCTYPE html>
	<html>
	<head>
		<meta charset="UTF-8">
		<title>Urban Dictionary Visualization</title>
		<style type="text/css">
			body
			{
				font-family: "Times New Roman", Georgia, Serif;
				text-align: center;
			}
		</style>
	</head>
	<body>
		<h1>Results for "$query"</h1>
		<p>Found $num_defs results, which is not enough for a popularity visualization.<p>
		<h2>Most popular answer (by user: $defs[0]->{'author'})</h2>
		<p>$defs[0]->{'definition'}<p>
		<h2>Similar tags</h2>
		<p>$tags</p>
	</body>
	</html>
EOHTML
}