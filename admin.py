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

import anydbm
import cgi
import cgitb
import common
import config
import Cookie
import datetime
import hashlib
import os
import uuid
import sys

cgitb.enable()

form = cgi.FieldStorage()

just_authenticated = False

config = config.get_config()

password_failed = False

if 'password' in form and os.path.exists(config['basedir']):
    password = form['password'].value
    if password == config['partymodepassword']:
        cookie = Cookie.SimpleCookie()
        sessionid = str(uuid.uuid1())
        hashed_id = hashlib.sha1(sessionid).hexdigest()
        cookie["oyster-sessionid"] = sessionid
        id_storage = anydbm.open('/tmp/oyster_sessionids', 'c')
        id_storage[hashed_id] = str(datetime.datetime.now())
        id_storage.close()
        print cookie
        just_authenticated = True
    else:
        password_failed = True

common.navigation_header(title="Admin Login")

if not os.path.exists(config['basedir']):
    print "<p>Please start Oyster before trying to login.</p>"
    common.html_footer()
    sys.exit()

if password_failed:
    print "<p>Password incorrect.</p>"
elif just_authenticated or common.is_authenticated():
    print "<p>Authenticated! Please visit the <a class='file' href='home.py'>main page</a> now.</p>"
    common.html_footer()
    sys.exit()

print """
<form method='post' action='admin.py' " + "enctype='application/x-www-form-urlencoded'>
    <input type="password" name="password"/>
    <input type="submit" value="Login"/>
</form>
"""

common.html_footer()
