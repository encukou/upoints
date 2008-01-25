#! /usr/bin/python -tt
# vim: set sw=4 sts=4 et tw=80 fileencoding=utf-8:
#
"""earth_distance - Modules for working with points on Earth"""
# Copyright (C) 2007-2008  James Rowe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

__version__ = "0.9.0"
__date__ = "2008-01-25"
__author__ = "James Rowe <jnrowe@ukfsn.org>"
__copyright__ = "Copyright (C) 2007-2008 James Rowe"
__license__ = "GNU General Public License Version 3"
__credits__ = "Kelly Turner"
__history__ = "See Mercurial repository"

from email.utils import parseaddr

__doc__ += """.

C{earth_distance} is a collection of GPL v3 licensed modules for working with
points on Earth, or other near spherical objects.  It allows you to calculate
the distance and bearings between points, mangle U{xearth
<http://www.cs.colorado.edu/~tuna/xearth/>}/U{xplanet
<http://xplanet.sourceforge.net/>} data files, work with online UK trigpoint
databases, U{GNU miscfiles <http://www.gnu.org/directory/miscfiles.html>} city
databases, U{NOAA <http://weather.noaa.gov/>}'s weather station databases and
other such location databases.

The C{earth_distance.point} module is the simplest interface available, and is
mainly useful as a naïve object for simple calculation and for subclassing for
specific usage.  An example of how to use it follows:

>>> Home = point.Point(52.015, -0.221)
>>> Telford = point.Point(52.6333, -2.5000)
>>> int(Home.distance(Telford))
169
>>> int(Home.bearing(Telford))
294
>>> int(Home.final_bearing(Telford))
293
>>> import datetime
>>> Home.sun_events(datetime.date(2007, 6, 28))
(datetime.time(3, 42), datetime.time(20, 25))
>>> Home.sunrise(datetime.date(2007, 6, 28))
datetime.time(3, 42)
>>> Home.sunset(datetime.date(2007, 6, 28))
datetime.time(20, 25)

@version: %s
@author: U{%s <mailto:%s>}
@copyright: %s
@status: WIP
@license: %s
""" % ((__version__, ) + parseaddr(__author__) + (__copyright__, __license__))

from earth_distance import (baken, cities, geonames, gpx, kml, nmea, osm, point,
                            trigpoints, tzdata, utils, weather_stations, xearth)

