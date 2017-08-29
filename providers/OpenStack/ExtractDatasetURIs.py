################################################################################
#
# Copyright (c) 2017 Philippe Merle, Inria
#
# This file is part of CloudLex.
#
# CloudLex is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CloudLex is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CloudLex.  If not, see <http://www.gnu.org/licenses/>.
#
# Contributors:
# - Philippe Merle <philippe.merle@inria.fr>
#
################################################################################

#
# This script generates the URIs Dataset for OpenStack.
# 

import sys
from cloudlex import extraction

extraction.extractDatasetURIsFromCsvFileOfSwaggerJsonURIs(
	sys.argv[1],
	'OpenStack',
	'http://openstack.provider.com',
	[
		# align variable paths of OpenStack identity-admin API.
		['/users/{name}', '/users/{userId}'],
		['/users/{user_id}', '/users/{userId}']
	]
)
