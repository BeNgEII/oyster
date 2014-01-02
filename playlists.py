#!/usr/bin/python
# -*- coding: UTF-8 -*
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

import config
myconfig = config.get_config()

def print_playlist(file):
    title = re.sub('\A.*_','',file)
    encfile = urllib.quote(file)

    if os.path.getsize(myconfig['savedir'] + '/lists/' + file) == 0:
        isempty = " <span class='emptylist'>(empty)</span>"
    else:
        isempty = ''

    if file == playlist and file != 'default':
        print "<tr>"
        print "<td class='playlists'><img src='themes/" + myconfig['theme'] +"/currentlyplaying.png' alt='currently playing'/></td>"
        print "<td><i><a href='playlistinfo.py?list=" + encfile + "'>" + title + "</a></i></td>"
        print "</tr>"
    elif file != 'default':
        print "<tr><td>"
        if oysterruns:
            print "<a href='playlists.py?action=loadlist&amp;" + \
                "listname=" + encfile + "' + title='Load'><img src='themes/" + myconfig['theme'] +"/loadplaylist_action.png' alt='load'/></a>"
        print "</td>"
        print "<td><a href='playlistinfo.py?list=" + encfile + "'>"+ title + isempty + "</a></td></tr>"

def confirmdelete():
    playlist = form['listname'].value
    enclist = urllib.quote(playlist)
    print "<h1>Should " + playlist + " be deleted?</h1>"
    print "<a href='playlists.py?action=delete&amp;listname=" + enclist + "'>Yes, delete it</a>"
    print "<br/>"
    print "<a href='playlists.py'>No, return to overview</a>"
    print "</body></html>"

def renameform(playlist):

    entries = os.listdir(myconfig['savedir'] + 'lists/')
    section = {}

    for entry in entries:
        if os.path.exists(myconfig['savedir'] + 'lists/' + entry) and entry.find('_') > -1:
            entry = re.sub('_.*', '', entry)
            section[entry] = 1;

    sections = ['Default']

    sectionkeys = section.keys()
    sectionkeys.sort()

    for section in sectionkeys:
        sections.append(section)

    title = re.sub('\A.*_', '', playlist)

    print "<h1>" + title + "</h1>"
    print "<h2>Move to another section</h2>"
    print "<div style='padding-left: 2em;'>"

    print "<form method='post' action='playlists.py' enctype='application/x-www-form-urlencoded'>"
    print "<input type='hidden' name='action' value='movelistsave'>"
    print "<input type='hidden' name='playlist' value='" + playlist + "'>"
    print "<input type='radio' name='sectiontype' value='existing' checked> " + \
            "in existing Section "

    print "<select name='existingsection'>"
    for existingsection in sections:
        print "<option value='" + existingsection + "'>" + existingsection + "</option>"
    print "</select><br/><br/>"

    print "<input type='radio' name='sectiontype' value='new'> " + \
            "in new Section <input type='text' name='newsection'>"
    print "<br/><br/>"
    print "<input type='submit' value='Move'>"
    print "</form>"

    print "</div><br/>"

    print "<h2>Rename</h2>"
    print "<div style='padding-left: 2em;'>"
    print "<form method='post' action='playlists.py' enctype='application/x-www-form-urlencoded'>"
    print "<input type='hidden' name='action' value='rename'>"
    print "<input type='hidden' name='playlist' value='" + playlist + "'>"
    print "<input type='textfield' name='newname'><br/><br/>"
    print "<input type='submit' value='Rename'>"
    print "</form></div>"
    sys.exit()


def listrename(oldname, newname):
    
    for dirname in ['blacklists/', 'lists/', 'logs/', 'scores/']:
        if os.path.exists(myconfig['savedir'] + dirname + oldname):
            os.rename(myconfig['savedir'] + dirname + oldname, \
            myconfig['savedir'] + dirname + newname)


import cgi
import fifocontrol
import cgitb
import sys
import os.path
import urllib
import re
import common
cgitb.enable()

_ = common.get_prefered_language()

basedir = myconfig['basedir']
savedir = myconfig['savedir']
form = cgi.FieldStorage()

if os.path.exists(myconfig['basedir']):
    oysterruns = 1
else:
    oysterruns = 0

import common
common.navigation_header("Playlists")

if form.has_key('action') and (form.has_key('listname') or form.has_key('newlistname')):
    if form['action'].value == 'confirmdelete':
        confirmdelete()
        sys.exit()
    else:
        if form.has_key('listname'):
            file = form['listname'].value
        else:
            file = form['newlistname'].value
        fifocontrol.do_action(form['action'].value, file)

if form.has_key('playlist') and form.has_key('action') and form['action'].value == 'move':
    renameform(form['playlist'].value)

if form.has_key('action') and form['action'].value == 'rename' and \
    form.has_key('playlist') and form.has_key('newname'):
    if form['playlist'].value.find('_') > -1:
        section = re.sub('_.*\Z', '_', form['playlist'].value)
    else:
        section = ''
    listrename(form['playlist'].value, section + form['newname'].value)

# Move playlist to new or existing section

if form.has_key('action') and form['action'].value == 'movelistsave' and \
    form.has_key('sectiontype') and form.has_key('playlist'):

    newsection = ''
    
    if form['sectiontype'].value == 'existing' and form.has_key('existingsection'):
    
        if not form['existingsection'].value == 'Default':
            newsection = form['existingsection'].value + '_'

    elif form['sectiontype'].value == 'new' and form.has_key('newsection'):

        if form.has_key('newsection') and not form['newsection'].value == 'Default':
            newsection = form['newsection'].value + '_'
        
    onlyplaylist = re.sub('\A.*_', '', form['playlist'].value)
    
    listrename(form['playlist'].value, newsection + onlyplaylist)

entries = os.listdir(savedir + "lists/")
entries.sort()

files = []
section = {}

for entry in entries:
    if os.path.isfile(savedir + "lists/" + entry):
        files.append(entry)
        if entry.find('_') > -1:
            entry = re.sub('_.*','',entry)
            section[entry] = 1

if form.has_key('action') and form['action'].value == 'loadlist' and form.has_key('listname'):
    playlist = form['listname'].value
else:
    playlist = config.get_playlist()

print "<table id='playlists'>"

print "<tr><td colspan='2'><h1>" + _("Playlists") + "</h1></td></tr>"

# Print default playlist

if playlist == 'default':
    print "<tr style='height:3em;'>"
    print "<td class='playlists'><img src='themes/" + myconfig['theme'] +"/currentlyplaying.png' alt='currently playing'/></td>"
    print "<td><a href='playlistinfo.py?list=default'><i>default (All songs)</i></a></td>"
    print "</tr>"
else:
    print "<tr style='height:3em;'>"
    print "<td class='playlists'>"
    if oysterruns:
        print "<a href='playlists.py?action=loadlist&amp;listname=default' title='Load'>"
        print "<img src='themes/" + myconfig['theme'] +"/loadplaylist_action.png' alt='load'/>"
        print "</a>"
    print "</td>"
    print "<td><a href='playlistinfo.py?list=default'>default (All songs)</a></td>"
    print "</tr>"

# Print playlists without a section

for file in files:
    if file.find('_') == -1:
        print_playlist(file)

# Print all sections

sectionkeys = section.keys()
sectionkeys.sort()

for section in sectionkeys:
    print "<tr><td colspan='5'><h2>" + section + "</h2></td></tr>"
    for file in files:
        if file.find(section + "_") == 0:
            print_playlist(file)

print "</table>"

if oysterruns:
    print "<form method='post' target='_top' action='editplaylist.py' " + \
        "enctype='application/x-www-form-urlencoded'>"
    print "<input type='hidden' name='action' value='addnewlist'/><input " + \
        "type='text' name='newlistname'/>"
    print "<input type='submit' name='.submit' value='New list' " + \
        "style='margin-left: 2em;'/>"
    print "<div></div></form><br/>"
else:
    print "<p>To create a new list, start oyster first!</p><br/>"

print "<a href='configedit.py'>Configuration Editor</a>"

print "</body></html>"
