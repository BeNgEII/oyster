package oyster::fifocontrol;

use strict;
use warnings;
use oyster::conf;

my %tag;
my %config = oyster::conf->get_config('oyster.conf');
my $VERSION = '1.0';

sub do_action {

    my $action=$_[1];
    my $file=$_[2];

    $file =~ s@//$@/@;
    $file =~ s/\.\.\///g;
    $file = '' if ($file eq "..");

    open(STATUS, "${config{'basedir'}}status");
    my $status = <STATUS>;
    chomp($status);
    close(STATUS);

    my $mediadir = $config{'mediadir'};
    $mediadir =~ s/\/$//;

    open (CONTROL, ">${config{'basedir'}}control");

    if ($action eq 'skip') {
	print CONTROL 'NEXT';
	sleep 4;
    } elsif ($action eq 'start') {
	system("perl oyster.pl &");
	while (!(-e "${config{'basedir'}}info")) {
	    sleep 1;
	}
    } elsif ($action eq 'stop') {
	print CONTROL "QUIT";
    } elsif ($action eq 'pause') {
	if ($status eq 'paused') {
	    print CONTROL "UNPAUSE";
	    $status = 'playing';
	} elsif ($status eq 'playing') {
	    print CONTROL "PAUSE";
	    $status = 'paused';
	}
    } elsif (($action eq 'scoreup') && ($file)) {
	print CONTROL "SCORE + $mediadir" . $file;
    } elsif (($action eq 'scoredown') && ($file)) {
	print CONTROL "SCORE - $mediadir" . $file;
    } 
    close CONTROL;

    return $status;

}

sub do_vote {
    my $votefile=$_[1];
    $votefile = $config{'mediadir'} . $votefile;
    open (CONTROL, ">${config{basedir}}control");
    print CONTROL "VOTE $votefile";
    close CONTROL;
    sleep 1;
}