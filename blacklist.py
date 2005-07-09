#!/usr/bin/python
# -*- coding: ISO-8859-1 -*
# oyster - a perl-based jukebox and web-frontend
#
# Copyright (C) 2004 Benjamin Hanzelmann <ben@nabcos.de>,
#  Stephan Windmüller <windy@white-hawk.de>,
#  Stefan Naujokat <git@ethric.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import cgi
import config
import taginfo
import fifocontrol
import cgitb
import sys
import os.path
import urllib
import common
import re
cgitb.enable()

def print_blacklist ():

    # Opens current blacklist and prints each line

    lineaffects = {}

    blacklistlines = []
    blacklist = open(myconfig['savedir'] + "blacklists/" + playlist)
    for line in blacklist.readlines():
        blacklistlines.append(line[:-1])
        line = line.replace(mediadir,'',1)[:-1]
        lineaffects[line] = 0
    blacklist.close()

    list = open(myconfig['savedir'] + "lists/" + playlist)

    totalaffected = 0

    # Count affected files for each rule

    for line in list.readlines():
        isblacklisted = 0
        line = line.replace(mediadir,'',1)[:-1]
        for blacklistline in blacklistlines:
            if re.match(blacklistline,line):
                isblacklisted = 1
                lineaffects[blacklistline] = lineaffects[blacklistline] + 1
        if isblacklisted:
            totalaffected = totalaffected + 1

    list.close()

    print "<table width='100%'>"
    for line in blacklistlines:
        escapedline = urllib.quote(line)
        print "<tr><td width='60%'>" + line + "</td>"
        print "<td width='25%' align='left'><a href='blacklist.py?action=test&amp;" + \
            "affects=" + escapedline + "'>Affects</a> (" + str(lineaffects[line]) + ")</td>"
        print "<td width='15%' align='center'><a href='blacklist.py?" + \
            "action=delete&amp;affects=" + escapedline + "'>Delete</a></td></tr>"

    print "</table>"

    print "<p><strong>Total files affected:</strong> " + str(totalaffected) + "</p>"

def print_affects (affects):

    # Shows all files, which are affected by a blacklist-rule

    results = []
    list = open (myconfig['savedir'] + "lists/" + playlist)

    # Add all matching lines to results

    print "Teste auf " + affects + "<br>"
    for line in list.readlines():
        line = line.replace(mediadir,'',1)[:-1]
        if re.match(affects, line):
            results.append(line)
    
    list.close()

    # Sort results alphabetically

    if results != []:
        results.sort()
        common.results = results
        results = common.sort_results('/')
        common.listdir('/', 0,'file2')
    else:
        print "<p>No songs match these rule.</p>"

def add_to_blacklist (affects):

    # Appends a rule to the blacklist

    blacklist = open(savedir + "blacklists/" + playlist, 'a')
    blacklist.write(affects + "\n")
    blacklist.close()

def delete_from_blacklist (affects):

    # removes a rule from the blacklist

    os.system ("cp " + savedir + "blacklists/" + playlist + " " + savedir + "blacklist.tmp")
    blacklist = open(savedir + "blacklist.tmp")
    newblacklist = open(savedir + "blacklists/" + playlist, 'w')
    for line in blacklist.readlines():
        if line[:-1] != affects:
            newblacklist.write(line)
    blacklist.close()
    newblacklist.close()
    os.unlink (savedir + "blacklist.tmp")

myconfig = config.get_config('oyster.conf')
basedir = myconfig['basedir']
savedir = myconfig['savedir']
mediadir = myconfig['mediadir'][:-1]
form = cgi.FieldStorage()
playlist = config.get_playlist()

common.navigation_header()

results = []

if form.has_key('affects') and form.has_key('action') and form['action'].value == 'test':
    affects = cgi.escape(form['affects'].value)
else:
    affects = ''

# Create form

print "<form method='post' action='blacklist.py' enctype='application/x-www-form-urlencoded'>"
print "<table border='0'><tr><td><input type='text' name='affects' ></td>"
print "<td><input type='radio' name='action' value='test' checked='checked'> Test Only<br>"
print "<input type='radio' name='action' value='add'> Add to Blacklist<br></td>"
print "<td><input type='submit' name='.submit' value='Go' style='margin-left: 2em;'></td></tr></table>"
print "<div><input type='hidden' name='.cgifields' value='action'></div></form>"

print "<p><a href='blacklist.py'>Show current blacklist</a></p>"

if form.has_key('action') and form.has_key('affects'):
    if form['action'].value == 'test':
        print_affects(form['affects'].value)
    elif form['action'].value == 'add':
        add_to_blacklist(form['affects'].value)
        print_blacklist()
    elif form['action'].value == 'delete':
        delete_from_blacklist(form['affects'].value)
        print_blacklist()
else:
    print_blacklist()

print "</body></html>"
