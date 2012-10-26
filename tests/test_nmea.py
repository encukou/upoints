#
#
"""test_nmea - Test nmea support"""
# Copyright (C) 2006-2011  James Rowe <jnrowe@gmail.com>
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

import datetime

from upoints.nmea import (Fix, Locations, LoranPosition, Position, Waypoint,
                          calc_checksum, nmea_latitude, nmea_longitude,
                          parse_latitude, parse_longitude)


def test_calc_checksum():
    """
    >>> calc_checksum("$GPGGA,142058,5308.6414,N,00300.9257,W,1,04,5.6,1374.6,M,34.5,M,,*6B")
    107
    >>> calc_checksum("GPGGA,142058,5308.6414,N,00300.9257,W,1,04,5.6,1374.6,M,34.5,M,,*6B")
    107
    >>> calc_checksum("$GPGGA,142058,5308.6414,N,00300.9257,W,1,04,5.6,1374.6,M,34.5,M,,")
    107
    >>> calc_checksum("GPGGA,142058,5308.6414,N,00300.9257,W,1,04,5.6,1374.6,M,34.5,M,,")
    107

    """


def test_nmea_latitude():
    """
    >>> nmea_latitude(53.144023333333337)
    ('5308.6414', 'N')

    """

def test_nmea_longitude():
    """
    >>> nmea_longitude(-3.0154283333333334)
    ('00300.9257', 'W')

    """


def test_parse_latitude():
    """
    >>> parse_latitude("5308.6414", "N")
    53.14402333333334

    """


def test_parse_longitude():
    """
    >>> parse_longitude("00300.9257", "W")
    -3.0154283333333334

    """


class TestLoranPosition():
    def test___init__(self):
        """
        >>> from dtopt import NORMALIZE_WHITESPACE
        >>> LoranPosition(53.1440233333, -3.01542833333,
        ...               datetime.time(14, 20, 58, 14), True, None)
        LoranPosition(53.1440233333, -3.01542833333,
                      datetime.time(14, 20, 58, 14), True, None)
        >>> LoranPosition(53.1440233333, -3.01542833333,
        ...               datetime.time(14, 20, 58, 14), True, "A")
        LoranPosition(53.1440233333, -3.01542833333,
                      datetime.time(14, 20, 58, 14), True, 'A')

        """

    def test___str__(self):
        """
        >>> from dtopt import NORMALIZE_WHITESPACE  # For \r handling
        >>> print(LoranPosition(53.1440233333, -3.01542833333,
        ...                     datetime.time(14, 20, 58), True, None))
        $GPGLL,5308.6414,N,00300.9257,W,142058.00,A*1F
        >>> print(LoranPosition(53.1440233333, -3.01542833333,
        ...                     datetime.time(14, 20, 58), True, "A"))
        $GPGLL,5308.6414,N,00300.9257,W,142058.00,A,A*72

        """

    def test_mode_string(self):
        """
        >>> position = LoranPosition(53.1440233333, -3.01542833333,
        ...                          datetime.time(14, 20, 58), True, None)
        >>> print(position.mode_string())
        Unknown
        >>> position.mode = "A"
        >>> print(position.mode_string())
        Autonomous

        """

    def test_parse_elements(self):
        """
        >>> from dtopt import NORMALIZE_WHITESPACE
        >>> LoranPosition.parse_elements(["52.32144", "N", "00300.9257", "W",
        ...                               "14205914", "A"])
        LoranPosition(52.0053573333, -3.01542833333,
                      datetime.time(14, 20, 59, 140000), True, None)

        """


class TestPosition():
    def test___init__(self):
        """
        >>> from dtopt import NORMALIZE_WHITESPACE
        >>> Position(datetime.time(14, 20, 58), True, 53.1440233333,
        ...          -3.01542833333, 109394.7, 202.9,
        ...          datetime.date(2007, 11, 19), 5.0)
        Position(datetime.time(14, 20, 58), True, 53.1440233333,
                 -3.01542833333, 109394.7, 202.9, datetime.date(2007, 11, 19),
                 5.0, None)

        """

    def test___str__(self):
        """
        >>> from dtopt import NORMALIZE_WHITESPACE  # For \r handling
        >>> print(Position(datetime.time(14, 20, 58), True, 53.1440233333,
        ...                -3.01542833333, 109394.7, 202.9,
        ...                datetime.date(2007, 11, 19), 5.0))
        $GPRMC,142058,A,5308.6414,N,00300.9257,W,109394.7,202.9,191107,5,E*41

        """

    def test_mode_string(self):
        """
        >>> position = Position(datetime.time(14, 20, 58), True, 53.1440233333,
        ...                     -3.01542833333, 109394.7, 202.9,
        ...                     datetime.date(2007, 11, 19), 5.0)
        >>> print(position.mode_string())
        Unknown
        >>> position.mode = "A"
        >>> print(position.mode_string())
        Autonomous

        """

    def test_parse_elements(self):
        """
        >>> from dtopt import NORMALIZE_WHITESPACE
        >>> Position.parse_elements(["142058", "A", "5308.6414", "N",
        ...                          "00300.9257", "W", "109394.7", "202.9",
        ...                          "191107", "5", "E", "A"])
        Position(datetime.time(14, 20, 58), True, 53.1440233333,
                 -3.01542833333, 109394.7, 202.9, datetime.date(2007, 11, 19),
                 5.0, 'A')
        >>> Position.parse_elements(["142100", "A", "5200.9000", "N",
        ...                          "00316.6600", "W", "123142.7", "188.1",
        ...                          "191107", "5", "E", "A"])
        Position(datetime.time(14, 21), True, 52.015, -3.27766666667, 123142.7,
                 188.1, datetime.date(2007, 11, 19), 5.0, 'A')

        """


class TestFix():
    def test___init__(self):
        """
        >>> from dtopt import NORMALIZE_WHITESPACE
        >>> Fix(datetime.time(14, 20, 27), 52.1380333333, -2.56861166667, 1, 4,
        ...     5.6, 1052.3, 34.5)
        Fix(datetime.time(14, 20, 27), 52.1380333333, -2.56861166667, 1, 4,
            5.6, 1052.3, 34.5, None, None, None)
        >>> Fix(datetime.time(14, 20, 27), 52.1380333333, -2.56861166667, 1, 4,
        ...     5.6, 1052.3, 34.5, 12, 4, None)
        Fix(datetime.time(14, 20, 27), 52.1380333333, -2.56861166667, 1, 4,
            5.6, 1052.3, 34.5, 12, 4, None)

        """

    def test___str__(self):
        """
        >>> from dtopt import NORMALIZE_WHITESPACE  # For \r handling
        >>> print(Fix(datetime.time(14, 20, 27), 52.1380333333, -2.56861166667,
        ...           1, 4, 5.6, 1052.3, 34.5))
        $GPGGA,142027,5208.2820,N,00234.1167,W,1,04,5.6,1052.3,M,34.5,M,,*61
        >>> print(Fix(datetime.time(14, 20, 27), 52.1380333333, -2.56861166667,
        ...           1, 4, 5.6, 1052.3, 34.5, 12, 4))
        $GPGGA,142027,5208.2820,N,00234.1167,W,1,04,5.6,1052.3,M,34.5,M,12.0,0004*78

        """

    def test_quality_string(self):
        """
        >>> fix = Fix(datetime.time(14, 20, 58), 53.1440233333, -3.01542833333,
        ...           1, 4, 5.6, 1374.6, 34.5, None, None)
        >>> print(fix.quality_string())
        GPS

        """

    def parse_elements(self):
        """
        >>> from dtopt import NORMALIZE_WHITESPACE
        >>> Fix.parse_elements(["142058", "5308.6414", "N", "00300.9257", "W",
        ...                     "1", "04", "5.6", "1374.6", "M", "34.5", "M",
        ...                     "", ""])
        Fix(datetime.time(14, 20, 58), 53.1440233333, -3.01542833333, 1, 4,
            5.6, 1374.6, 34.5, None, None, None)
        >>> Fix.parse_elements(["142100", "5200.9000", "N", "00316.6600", "W",
        ...                     "1", "04", "5.6", "1000.0", "M", "34.5", "M",
        ...                     "", ""])
        Fix(datetime.time(14, 21), 52.015, -3.27766666667, 1, 4, 5.6, 1000.0,
            34.5, None, None, None)

        """


class TestWaypoint():
    def test___init__(self):
        """
        >>> Waypoint(52.015, -0.221, "Home")
        Waypoint(52.015, -0.221, 'HOME')

        """

    def test___str__(self):
        """
        >>> from dtopt import NORMALIZE_WHITESPACE  # For \r handling
        >>> print(Waypoint(52.015, -0.221, "Home"))
        $GPWPL,5200.9000,N,00013.2600,W,HOME*5E

        """

    def test_parse_elements(self):
        """
        >>> Waypoint.parse_elements(["5200.9000", "N", "00013.2600", "W",
        ...                          "HOME"])
        Waypoint(52.015, -0.221, 'HOME')

        """


class TestLocations():
    def test_import_locations(self):
        r"""
        >>> locations = Locations(open("test/data/gpsdata"))
        >>> from dtopt import NORMALIZE_WHITESPACE  # For \r handling
        >>> for value in locations:
        ...     print(value)
        $GPGGA,142058,5308.6414,N,00300.9257,W,1,04,5.6,1374.6,M,34.5,M,,*6B
        $GPRMC,142058,A,5308.6414,N,00300.9257,W,109394.7,202.9,191107,5,E,A*2C
        $GPWPL,5200.9000,N,00013.2600,W,HOME*5E
        $GPGGA,142100,5200.9000,N,00316.6600,W,1,04,5.6,1000.0,M,34.5,M,,*68
        $GPRMC,142100,A,5200.9000,N,00316.6600,W,123142.7,188.1,191107,5,E,A*21

        """
