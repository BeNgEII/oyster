#!/usr/bin/perl
use CGI qw/:standard -no_xhtml/;
use URI::Escape;
use strict;
use oyster::conf;

print
    header,
    start_html(-title=>'Oyster-GUI',
	       -style=>{'src'=>'layout.css'},
	       -head=>CGI::meta({-http_equiv => 'Content-Type',
				 -content    => 'text/html; charset=iso-8859-1'}));

print "<table width='100%'><tr>";
print "<td align='left' width='30%'><a href='browse.pl'>Browse</a></td>";
print "<td align='center' width='40%'><a href='search.pl'>Search</a></td>";
print "<td align='right' width='30%'><a href='blacklist.pl'>Blacklist</a></td>";print "</tr></table>";
print "<hr>";

my %config = oyster::conf->get_config('oyster.conf');

my $basedir = $config{'mediadir'};
my $rootdir=$basedir;
my $file;

if (param()) {
    $basedir = param('file');
    $basedir =~ s@//$@/@;
    $basedir =~ s/\.\.\///g;
    $basedir = $rootdir if (($basedir eq "..") || ($basedir eq ""));
    $file = $basedir;
    $basedir =~ s/\/[^\/]*$//;
    $file =~ s/.*\///;
    $basedir = $rootdir if (($basedir eq "..") || ($basedir eq ""));
}

$basedir = $rootdir if (!($basedir =~ /^\Q$rootdir\E/));

print "<p>Tag-Info for ";

my $subdir = $basedir;
$subdir =~ s/^\Q$rootdir\E//;
my @dirs = split(/\//, $subdir);
my $incdir = '';
foreach my $partdir (@dirs) {
    my $escapeddir = uri_escape("$rootdir$incdir$partdir", "^A-Za-z");
    print "<a href='browse.pl?dir=$escapeddir'>$partdir</a> / ";
    $incdir = $incdir . "$partdir/";
}

print "$file</p>\n";

print "<p><a class='file' href='oyster-gui.pl?vote=$basedir/$file' target='curplay'>Vote for this song</a></p>\n";

if ($file =~ /mp3$/) {
    open (MP3, "id3v2 -l \"$basedir/$file\"|") or die $!;
    my @output = <MP3>;

    foreach my $line (@output) {
	print $line . "<br>";
    }

    close (MP3);

} elsif ($file =~ /ogg$/) {
    open (OGG, "ogginfo \"$basedir/$file\"|") or die $!;
    my @output = <OGG>;
    
    foreach my $line (@output) {
	print $line . "<br>";
    }

    close (OGG);
}

print end_html;
