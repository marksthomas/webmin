#!/usr/local/bin/perl
# Show a form for editing or creating an jail

use strict;
use warnings;
require './fail2ban-lib.pl';
our (%in, %text);
&ReadParse();

my ($jail, $def);

# Show header and get the jail object
if ($in{'new'}) {
	&ui_print_header(undef, $text{'jail_title1'}, "");
	$jail = { };
	}
else {
	&ui_print_header(undef, $text{'jail_title2'}, "");
	($jail) = grep { $_->{'name'} eq $in{'name'} } &list_jails();
	$jail || &error($text{'jail_egone'});
	}

print &ui_form_start("save_jail.cgi", "post");
print &ui_hidden("new", $in{'new'});
print &ui_hidden("old", $in{'name'});
print &ui_table_start($text{'jail_header'}, undef, 2);

# Jail name
print &ui_table_row($text{'jail_name'},
	&ui_textbox("name", $jail->{'name'}, 30));

# Enabled or disabled?
my $enabled = &find_value("enabled", $jail);
print &ui_table_row($text{'jail_enabled'},
	&ui_yesno_radio("enabled", $enabled =~ /true|yes|1/i));

# Filter to match
my @filters = &list_filters();
my $filter = &find_value("filter", $jail);
print &ui_table_row($text{'jail_filter'},
	&ui_select("filter",
		   $filter,
		   [ map { &filename_to_name($_->[0]->{'file'}) } @filters ],
		   1, 0, $filter ? 1 : 0));

# Actions to run
my @actions = &list_filters();
my $atable = &ui_columns_start([
		$text{'jail_action'},
		$text{'jail_name'},
		$text{'jail_port'},
		$text{'jail_protocol'},
		]);
my $i = 0;
foreach my $a (@{$jail->{'words'}}, undef) {
	my $action;
	my %opts;
	if ($a =~ /^(\S+)\[(.*)\]$/) {
		$action = $1;
		%opts = map { split(/=/, $_) } split(/,\s*/, $2);
		}
	else {
		$action = $a;
		}
	$atable .= &ui_columns_row([
		&ui_select("action_$i", $action,
		   [ map { &filename_to_name($_->[0]->{'file'}) } @actions ],
		   1, 0, $action ? 1 : 0),
		&ui_textbox("name_$i", $opts{'name'}, 20),
		&ui_textbox("port_$i", $opts{'port'}, 6),
		&ui_select("protocol_$i", $opts{'protocol'},
			   [ 'tcp', 'udp', 'icmp' ]),
		]);
	$i++;
	}
$atable .= &ui_columns_end();
print &ui_table_row($text{'jail_actions'}, $atable);

# Log file paths
my $logpath = &find_value("logpath", $jail);
print &ui_table_row($text{'jail_logpath'},
	&ui_textarea("logpath", $logpath, 5, 80, "hard"));

# IPs to ignore
my $ignoreip = &find_value("ignoreip", $jail);
# XXX

print &ui_table_end();
if ($in{'new'}) {
	print &ui_form_end([ [ undef, $text{'create'} ] ]);
	}
else {
	print &ui_form_end([ [ undef, $text{'save'} ],
			     [ 'delete', $text{'delete'} ] ]);
	}

&ui_print_footer("list_jails.cgi", $text{'jails_return'});
