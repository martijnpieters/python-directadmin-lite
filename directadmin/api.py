#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Directadmin API - Lite Python implementation of Directadmin Web API

Copyright (C) 2009, Andrés Gattinoni
Portions (C) 2014, Martijn Pieters

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

=======================================================================

Original project URL: http://code.google.com/p/python-directadmin/

For more information about Directadmin's Web API, visit:
http://www.directadmin.com/api.html

Original author: Andrés Gattinoni <andresgattinoni@gmail.com>
Author: Martijn Pieters <python@martijnpieters.nl>
"""

import urllib.request, urllib.error, urllib.parse
import base64

_user_agent = "Python Directadmin"


class ApiError(Exception):
    """API Error

    Generic exception for API error handling
    """
    pass


class ApiConnector(object):
    """API Connector

    Basic object to handle API connection.
    Connect and send commands.
    """
    _hostname = None
    _port = 0
    _username = None
    _password = None
    _https = False

    def __init__(self,
                  username,
                  password,
                  hostname="localhost",
                  port=2222,
                  https=False):
        """Constructor

        Parameters:
        username = username to login on Directadmin
        password = password to login on Directadmin
        hostname = Directadmin's hostname (default: localhost)
        port = port on which Directadmin listens (default: 2222)
        https -- boolean, if True all transactions will
                 be performed using HTTPS (default: False)
        """
        self._hostname = hostname
        self._port = int(port)
        self._username = username
        self._password = password
        self._https = bool(https)

    def execute(self, cmd, parameters=None, get=None):
        """Execute command

        Executes a command of the API
        processes the result and returns it

        Parameters:
        cmd = command name
        parameters = list of tuples with parameters (default: None)
        get = list of tuples or dict with get parameters (default: None)
        """
        url = self._get_url(cmd)

        if get is not None:
            url = '%s?%s' % (url, urllib.parse.urlencode(get))

        if parameters is not None:
            parameters = urllib.parse.urlencode(parameters).encode('utf-8')

        request = urllib.request.Request(url, parameters)

        # Directadmin's API requires Basic HTTP Authentication
        bytestring = bytes("%s:%s" % (self._username, self._password), 'utf-8')
        base_auth = base64.b64encode(bytestring)
        request.add_header('Authorization', 'Basic %s' % base_auth.decode('utf-8'))

        # Identify our app with a custom User-Agent
        request.add_header('User-Agent', _user_agent)

        # Open the URL and handle the response
        try:
            return self._handle_response(urllib.request.urlopen(request))
        except urllib.error.URLError as e:
            raise ApiError("HTTP Error: %s" % e.reason)

    def _get_url(self, cmd):
        """Get URL

        Returns the URL for a specific command
        """
        if self._https:
            protocol = "https"
        else:
            protocol = "http"
        return '%s://%s:%d/%s' % \
               (protocol,
                self._hostname,
                self._port,
                cmd)

    def _handle_response(self, response):
        """Handle response

        Takes the response string returned by
        Directadmin server, checks for errors
        and returns a python-friendly object

        Parameters:
        response -- response object

        Returns a list or dictionary according
        to the method

        Raises ApiError on errors
        """
        # Get response headers to check if there
        # was any problem with login
        info = response.info()
        if response.getheader('X-DirectAdmin') == 'unauthorized':
            raise ApiError("Invalid username or password")

        # If we're getting HTML content we'll search for known
        # error messages.
        if response.getheader('Content-Type') == 'text/html':
            errors = ['You cannot execute that command']
            response = response.read()
            for msg in errors:
                if response.find(bytes(msg, 'utf-8')) > -1:
                    raise ApiError(msg)
            # If we don't find any known error messages,
            # we exit anyway, because we can't handle this
            raise ApiError('Got unexpected HTML response from server')

        # Parse the response query string
        response = urllib.parse.parse_qs(response.read())

        # Check for 'error' flag
        if 'error' in response:
            # If 'error' is 0, the operation was successful
            if response['error'][0] == "0":
                return True
            # If not, check for details of the error
            else:
                if 'details' in response:
                    raise ApiError(response['details'][0])
                if 'text' in response:
                    raise ApiError(response['text'][0])
                else:
                    raise ApiError("Unknown error detected")
        # If we got a 'list[]' keyword, we return only the list
        elif 'list[]' in response:
            return response['list[]']
        # On any other case return the whole structure
        else:
            return response


class Api(object):
    """API

    Directadmin API implementation
    """
    _connector = None

    def __init__(self,
                  username,
                  password,
                  hostname="localhost",
                  port=2222,
                  https=False):
        """Constructor

        Initializes the connection for the API

        Parameters:
        username -- Directadmin username
        password -- Directadmin password
        hostname -- Directadmin server host (default: localhost)
        port -- Directadmin server port (default: 2222)
        https -- boolean, if True all transactions will
                 be performed using HTTPS (default: False)
        """
        self._connector = ApiConnector(username,
                                       password,
                                       hostname,
                                       port,
                                       https)

    def execute(self, cmd, parameters=None, get=None):
        """Execute command

        Executes a command using the Connection object
        """
        return self._connector.execute(cmd, parameters, get)
