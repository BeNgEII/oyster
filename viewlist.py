#!/usr/bin/python
# -*- coding: UTF-8 -*-

# oyster - a python-based jukebox and web-frontend
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

"""
CGI-Script for viewing a m3u-like playlist inside of oyster
"""

__revision__ = 1

import cgi
import config
import cgitb
import os.path
import urllib
cgitb.enable()

myconfig = config.get_config()
mediadir = myconfig['mediadir']
form = cgi.FieldStorage()

import common
common.navigation_header()

if 'list' in form:
    givenlist = form['list'].value.replace('../', '')
    if givenlist == '..':
        givenlist = ''
else:
    givenlist = ''

if givenlist != '' and os.path.exists(mediadir + givenlist):

    print "<p>"

    print "<a href='browse.py?dir=/'>Mediadir</a>"

    dirs = givenlist.split('/')
    incdir = ''
    for partdir in dirs:
        escapeddir = urllib.quote(incdir + partdir)
        if partdir[-4:] == '.m3u' or partdir[-4:] == '.pls':
            print "<a class='playlist' href='viewlist.py?list=" + \
                  escapeddir + "'>" + partdir + "</a>"
        else:
            print "<a href='browse.py?dir=" + escapeddir + \
                "'>" + partdir + "</a> / "
        incdir = incdir + partdir + "/"

    print "</strong></p>"

    topdir = os.path.dirname(givenlist.replace(mediadir, '', 1))

    print "<table>"
    
    # alternating betweeen '' and '2'
    alt = '2'

    playlist = open(mediadir + givenlist)
    for line in playlist:
        line = line
        if line[0] != '#':
            line = line[:-1].replace(mediadir, '', 1)
            if line[0:2] == './':
                line = line[2:]
            escapedfile = urllib.quote(topdir + "/" + line)

            if alt == '':
                alt = '2'
            else:
                alt = ''

            print "<tr>"

            if os.path.exists(mediadir + topdir + "/" + line):
                print "<td><a title='Vote this file' class='file" + alt + "' href='home.py?vote=" + escapedfile +\
                      "'><img src='themes/" + myconfig['theme'] + "/votefile" + alt + ".png'/></a></td>"
                print "<td><a class='file" + alt + "' href='fileinfo.py?file=" + escapedfile + "'>" + line + "</a></td>"
            else:
                print "<td></td><td><span class='file" + alt + "'>" + line + "</span> (file missing)</td>"

            print "</tr>"

    print "</table>"


else:
    print "<h1>Error</h1>"
    print "The playlist " + givenlist + "could not be found."
    
print "</body></html>"
