# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members


import os
import sys

from twisted.internet import defer

from buildbot.data import connector
from buildbot.test.fake import fakemaster
from buildbot.util import in_reactor


@in_reactor
@defer.inlineCallbacks
def gengraphql(config):
    master = yield fakemaster.make_master(None, wantRealReactor=True)
    data = connector.DataConnector()
    yield data.setServiceParent(master)

    if config['out'] != '--':
        dirs = os.path.dirname(config['out'])
        if dirs and not os.path.exists(dirs):
            os.makedirs(dirs)
        f = open(config['out'], "w")
    else:
        f = sys.stdout
    schema = data.graphql_get_schema()
    f.write(schema)
    return 0
