#!/usr/bin/python
# -*- coding: ISO-8859-1 -*-

# oyster - a python-based jukebox and web-frontend
#
# Copyright (C) 2004 Benjamin Hanzelmann <ben@nabcos.de>,
# Stephan Windmüller <windy@white-hawk.de>, Stefan Naujokat <git@ethric.de>
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

"Provides common functions used by Oyster"

__revision__ = 1

import cgi
import cgitb
import config
import os.path
import urllib
import re
import base64
cgitb.enable()

myconfig = config.get_config()

def navigation_header():

    "Prints the standard header for most pages of Oyster"

    print "Content-Type: text/html; charset=" + myconfig['encoding'] + "\n"
    print "<?xml version='1.0' encoding='" + myconfig['encoding'] + "' ?>"
    print """
<!DOCTYPE html 
     PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
 <title>Oyster-GUI</title>
"""
    print "<meta http-equiv='Content-Type' content='text/html;charset=" + myconfig['encoding'] + "' />"
    print "<link rel='stylesheet' type='text/css' href='themes/" + \
        myconfig['theme'] + "/layout.css' />"
    print "<link rel='shortcut icon' href='themes/" + myconfig['theme'] + \
        "/favicon.png' />"
    print "</head><body>"
    
    print "<ul id='navigation'>"
    print "<li><a href='browse.py'>Browse</a></li>"
    print "<li><a href='search.py'>Search</a></li>"
    print "<li><a href='playlists.py'>Playlists</a></li>"
    print "<li><a href='blacklist.py'>Blacklist</a></li>"
    print "<li><a href='score.py'>Scoring</a></li>"
    print "<li><a href='extras.py'>Extras</a></li>"
    print "</ul><br/>"
    print "<hr/>"

def get_cover (albumdir, imagewidth):

    "Returns a cover-image as a base64-string"

    albumname = os.path.basename(albumdir[:-1])
    albumnameus = albumname.replace(' ', '_')
    coverfiles = myconfig['coverfilenames'].split(',')
    filetype = 'jpeg'
    encoded = ""

    for cover in coverfiles:
        cover = cover.replace('${album}', albumname)
        cover = cover.replace('${albumus}', albumnameus)
        if os.path.exists(albumdir + cover):
            coverfile = open (albumdir + cover)
            encoded = base64.encodestring(coverfile.read())
            coverfile.close()
            filetype = cover[-3:]
            break

    if encoded == "":
        return ''
    else:
        return "<img src='data:image/" + filetype + ";base64," + encoded + \
            "' width='" + imagewidth + "' style='float:right' alt='Cover'/>"

def sort_results (topdir):

    """
    sort_results sorts a directory and its subdirectories by
    "first dirs, then files"

    But do we really need this method?
    """

    skip = '' # Do not add directories twice
    dirs = []
    files = []

    dirregexp = re.compile('\A' + re.escape(topdir) + '([^/]+)/')
    fileregexp = re.compile('\A' + re.escape(topdir) + '[^/]*')

    for line in results:
        if ((skip != '') and not (line.find(skip) == 0)) or (skip == ''):
            dirmatcher = dirregexp.match(line)
            filematcher = fileregexp.match(line)
            if dirmatcher != None:
                # line is a directory
                skip = topdir + dirmatcher.group(1) + "/"
                dirs = dirs + sort_results(skip)
            elif filematcher != None:
                # line is a file
                files.append(line)

    return(dirs + files)

def listdir (basepath, counter, cssclass, playlistmode=0, playlist=''):

    """
    listdir shows files from results, sorted by directories
    basepath is cut away for recursive use
    """

    while counter < len(results) and results[counter].find(basepath) == 0:
        newpath = results[counter].replace(basepath, '', 1)
        if newpath.find('/') > -1:
            # $newpath is directory and becomes the top one

            matcher = re.match('\A([^/]*/)', newpath)
            newpath = matcher.group(1)

            # do not add padding for the top level directory

            cutnewpath = newpath[:-1]

            if not basepath == '/':
                escapeddir = urllib.quote(basepath + cutnewpath)
                if playlistmode == 1:
                
                    # Browse-window of playlist editor
                    
                    print "<table width='100%'><tr><td align='left'>"
                    print "<strong><a href='browse.py?mode=playlist&dir=" + \
                        escapeddir + "&amp;playlist=" + playlist + \
                        "' target='browse'>" + cgi.escape(cutnewpath) + \
                        "</a></strong>"
                    print "<td align='right'><a href='editplaylist.py?" + \
                        "playlist=" + playlist + "&deldir=" + escapeddir + \
                        "'>Delete</a></td>"
                    print "</tr></table>"

                elif playlistmode == 2:

                    # Search-window of playlist-editor
                
                    print "<table width='100%'><tr><td align='left'>"
                    print "<strong><a href='browse.py?mode=playlist&dir=" + \
                        escapeddir + "&amp;playlist=" + playlist + \
                        "' target='browse'>" + cgi.escape(cutnewpath) + \
                        "</a></strong>"
                    print "<td align='right'><a href='editplaylist.py?" + \
                        "playlist=" + playlist + "&adddir=" + escapeddir + \
                        "' target='playlist'>Add</a></td>"
                    print "</tr></table>"
                    
                else:
                    print "<strong><a href='browse.py?dir=" + escapeddir + \
                        "'>" + cgi.escape(cutnewpath) + "</a></strong>"
                newpath = basepath + newpath
            else:
                escapeddir = urllib.quote("/" + cutnewpath)
                if playlistmode == 1:
                    print "<table width='100%'><tr><td align='left'>"
                    print "<strong><a href='browse.py?mode=playlist&dir=" + \
                        escapeddir + "&amp;playlist=" + playlist + \
                        "' target='browse'>" + cgi.escape(cutnewpath) + \
                        "</a></strong>"
                    print "<td align='right'><a href='editplaylist.py?" + \
                        "playlist=" + playlist + "&deldir=" + escapeddir + \
                        "'>Delete</a></td>"
                    print "</tr></table>"
                elif playlistmode == 2:
                    print "<table width='100%'><tr><td align='left'>"
                    print "<strong><a href='browse.py?mode=playlist&dir=" + \
                        escapeddir + "&amp;playlist=" + playlist + \
                        "' target='browse'>" + cgi.escape(cutnewpath) + \
                        "</a></strong>"
                    print "<td align='right'><a href='editplaylist.py?" + \
                        "playlist=" + playlist + "&adddir=" + escapeddir + \
                        "' target='playlist'>Add</a></td>"
                    print "</tr></table>"
                else:
                    print "<strong><a href='browse.py?dir=" + escapeddir + \
                        "'>" + cgi.escape(cutnewpath) + "</a></strong>"
                newpath = "/" + newpath

            # Call listdir recursive, then quit padding with <div>

            print "<div style='padding-left: 1em;'>"
            counter = listdir(newpath, counter, cssclass, playlistmode, playlist)
            print "</div>"

        else:

            # $newpath is a regular file without leading directory

            while counter < len(results) and \
                (os.path.dirname(results[counter]) + "/" == basepath or os.path.dirname(results[counter]) == basepath):

                # Print all filenames in basepath

                filename = os.path.basename(results[counter])
                matcher = re.match('(.*)\.([^\.]+)\Z', filename)
                nameonly = matcher.group(1)
                escapedfile = urllib.quote(basepath + filename)

                # $cssclass changes to give each other file
                # another color

                if cssclass == 'file':
                    cssclass = 'file2'
                else:
                    cssclass = 'file'

                print "<table width='100%'><tr>"
                print "<td align='left'><a href='fileinfo.py?file=" + \
                    escapedfile + "' class='" + cssclass + "'>" + \
                    cgi.escape(nameonly) + "</a></td>"
                if playlistmode == 1:
                    print "<td align='right'><a href='editplaylist.py?" + \
                    "playlist=" + playlist + "&delfile=" + escapedfile + \
                        "' class='" + cssclass + "'>Delete</a></td>"
                elif playlistmode == 2:
                    print "<td align='right'><a href='editplaylist.py?" + \
                    "playlist=" + playlist + "&amp;addfile=" + escapedfile + \
                        "' target='playlist' class='" + cssclass + "'>Add</a></td>"
                else:
                    if os.path.exists(myconfig['basedir']):
                        print "<td align='right'><a href='oyster-gui.py" + \
                        "?vote=" + escapedfile + "' class='" + cssclass + \
                        "' target='curplay'>Vote</a></td>"
                    else:
                        print "<td></td>"
                print "</tr></table>\n"
                counter = counter + 1

    return counter
