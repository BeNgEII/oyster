#!/usr/bin/python
# -*- coding: ISO-8859-1 -*-
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

"Tests the configuration of oyster for common errors"

__revision__ = '1.0'

import config
import os.path
import re
import cgitb
cgitb.enable()

def print_result (result):

    "Generates the OK or ERROR labels"

    if result == 0:
        print "<td align='center' class='configok'>OK</td>"
    elif result == 1:
        print "<td align='center' class='configerror'>ERROR</td>"

def test_readable (name, var):

    "Tests if the given var exists and is readable"

    if os.path.exists(var) and os.access(var, os.R_OK):
        result = 0
    else:
        result = 1

    print "<tr>"
    print "<td>Is " + name + " (" + var + ") readable?</td>"
    print_result(result)
    print "</tr>"

def test_writeable (name, var):

    "Tests if the given var exists and is writeable"
    
    if os.path.exists(var) and os.access(var, os.W_OK):
        result = 0
    else:
        result = 1

    print "<tr>"
    print "<td>Is " + name + " (" + var + ") writeable?</td>"
    print_result(result)
    print "</tr>"

def test_createable (name, var):

    "Tests if the given directory can be created"
    
    if os.path.exists(var) and os.access(var, os.W_OK):
        # basedir already exists
        result = 0
    elif os.access(re.sub('[^/]*/\Z','',var), os.W_OK):
        # basedir can be created
        result = 0
    else:
        result = 1

    print "<tr>"
    print "<td>Can " + name + " (" + var + ") be created?</td>"
    print_result(result)
    print "</tr>"

def test_program (name, var):

    "Tests if the given program exists and can be executed"
    
    if os.path.exists(var) and os.access(var, os.X_OK):
        result = 0
    else:
        result = 1

    print "<tr>"
    print "<td>Is " + name + " (" + var + ") installed and executable?</td>"
    print_result(result)
    print "</tr>"

myconfig = config.get_config()

print "Content-Type: text/html\n"
print "<?xml version='1.0' ?>"
print """
<!DOCTYPE html 
         PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
         "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
 <title>Oyster Configuration Checker</title>
"""
print " <meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />"

print " <link rel='stylesheet' type='text/css' href='themes/" + \
    myconfig['theme'] + "/layout.css'/>"
print "</head>"
print "<body>"
print "<h1>Configuration Checker</h1>"

print "<table width='100%'>"

print "<tr><th colspan='2' class='configsection'>" + \
    "Testing permissions...</th></tr>"

test_readable('savedir', myconfig['savedir'])
test_writeable('savedir', myconfig['savedir'])
test_createable('basedir', myconfig['basedir'])
test_readable('mediadir', myconfig['mediadir'])

print "<tr><td></td></tr>"
print "<tr><th colspan='2' class='configsection'>" + \
    "Testing playback capabilities...</th></tr>"

test_writeable('the sounddevice', '/dev/dsp')
test_readable('the mixerdevice', '/dev/mixer')
test_writeable('the mixerdevice', '/dev/mixer')
test_program('the MP3-player', myconfig['mp3'])
test_program('the OGG-player', myconfig['ogg'])
test_program('the FLAC-player', myconfig['flac'])
test_program('the mixer program', '/usr/bin/aumix')
test_program('the mp3 tag reader', '/usr/bin/id3v2')
test_program('the ogg/flac tag reader', '/usr/bin/ogg123')

print "</table>"

print "<p><a href='oyster-gui.py'>Back to main screen</a></p>"

print "</body></html>"
