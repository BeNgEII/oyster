#!/usr/bin/perl
use CGI qw/:standard -no_xhtml/;
use URI::Escape;
use strict;
use oyster::conf;
use oyster::common;

my %config = oyster::conf->get_config('oyster.conf');
my $playlist = oyster::conf->get_playlist();
my $savedir = $config{'savedir'};

my $playlist = oyster::conf->get_playlist();

oyster::common->navigation_header();

if (param('action') && param('listname')) {
    if (param('action') eq 'addnewlist') {
	my $newlist = param('listname');
	$newlist =~ s/.*\///;
	open (NEWLIST, ">$config{savedir}lists/$newlist");
	close (NEWLIST);
    } elsif (param('action') eq 'delete') {
	my $dellist = param('listname');
	$dellist =~ s/.*\///;
	unlink("$config{savedir}lists/$dellist");
    }
}

my $globdir = "${savedir}lists/";
my @entries = <$globdir*>;

my @files = ();

foreach my $entry (@entries) {
    if (-f "$entry") {
	$entry =~ s/$globdir//;
	push (@files, "$entry");
    }
}

print "<table width='100%' style='margin-bottom: 2em;'>";

foreach my $file (@files) {
    if ($file eq $playlist) {
	print "<tr><td><i>$file</i></td><td>currently playing</td>";
    }
    else {
	print "<tr><td>$file</td>" .
	    "<td><a href='oyster-gui.pl?action=loadlist&amp;file=$file'" .
	    "target='curplay'>Load List</a></td>";
    }
    print "<td><a href='editplaylist.pl?action=edit&amp;" .
	"playlist=$file'>Edit List</a></td>\n";
    print "<td><a href='playlists.pl?action=delete&amp;" .
	"listname=$file'>Delete List</a></td>\n";

}

print "</table>";

print start_form;

print hidden(-name=>'action', -default=>'addnewlist');

print textfield(-name=>'listname',-default=>'');
print submit(-value=>'Create new list',-style=>'margin-left: 2em;');

print end_form;


print end_html;
