#!/usr/bin/env python
# -*- encoding: UTF8 -*-

# author: Philipp Klaus, philipp.klaus →AT→ gmail.com

# This file is part of python-inwx-xmlrpc.
#
# python-inwx-xmlrpc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-inwx-xmlrpc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-inwx-xmlrpc. If not, see <http://www.gnu.org/licenses/>.

###########################################################################
###### This file helps to handle the INI-style .cfg files. ######
###### You only need it if you want to test the example script. ######
###### It is not needed if you just want to use the inwx class. ######

import sys

if sys.version_info.major == 3:
    import configparser
else:
    import ConfigParser as configparser

from os.path import expanduser
from ast import literal_eval

def get_account_data(print_errors = False, config_file = 'config.ini', config_section = 'ote'):
    """
    boolean print_errors:   Print errors to stdout instead of raising an exception.
    string config_file:     The name of the configuration file.
    string config_section:  The name of the section to read in the configuration file.
    """
    config = open_config_file(print_errors, config_file)
    try:
        api_url = config.get(config_section, 'url')
        username = config.get(config_section, 'username')
        password = config.get(config_section, 'password')
        shared_secret = config.get(config_section, 'shared_secret')
    except Exception as err:
        message = 'Error: Please make sure your config file %s contains the section %s with the entries "url", "username", "password" and "shared_secret".' % (config_file, config_section)
        if print_errors:
            print(message)
            sys.exit(2)
        else:
            raise NameError(message)
    return (api_url, username, password, shared_secret)

def get_nameservers(print_errors = False, config_file = 'config.ini', config_section = 'ote'):
    config = open_config_file(print_errors, config_file)
    try:
        nameservers = config.get(config_section, 'nameservers')
        nameservers = literal_eval(nameservers)
    except Exception as err:
        message = 'Error: Please make sure your config file %s contains the section %s with the entry "nameservers" and that it is formatted correctly as a list.' % (config_file, config_section)
        if print_errors:
            print(message)
            sys.exit(2)
        else:
            raise NameError(message)
    return nameservers

def open_config_file(print_errors, config_file):
    config = configparser.ConfigParser()
    try:
        if config.read(config_file) == []: raise Exception()
    except:
        message = "Error: Please make sure you adopted the config file: %s" % config_file
        if print_errors:
            print(message)
            sys.exit(2)
        else:
            raise NameError(message)
    return config
