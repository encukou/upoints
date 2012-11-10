#
# coding=utf-8
"""test_point - Test point support"""
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
import math

from unittest import TestCase

from expecter import expect

from upoints import utils
from upoints.point import (KeyedPoints, Point, Points, TimedPoint, TimedPoints)


class TestPoint(TestCase):
    def test___init__(self):
        test = Point(math.pi / 4, math.pi / 2, angle="radians")
        expect(test.latitude) == 45
        expect(test.longitude) == 90

        test = Point((50, 20, 10), (-1, -3, -12))
        expect("%.3f" % test.latitude) == '50.336'
        expect("%.3f" % test.longitude) == '-1.053'

        with expect.raises(ValueError, "Unknown angle type `None'"):
            Point(52.015, -0.221, angle=None)
        with expect.raises(ValueError, "Invalid latitude value `-92.000000'"):
            Point(-92, -0.221)
        with expect.raises(ValueError, "Invalid longitude value `185.000000'"):
            Point(52.015, 185)
        with expect.raises(ValueError, "Unknown units type `None'"):
            Point(52.015, -0.221, units=None)

    def test___dict__(self):
        Home = Point(52.015, -0.221)
        expect(sorted(Home.__dict__.items())) == \
            [('_angle', 'degrees'), ('_latitude', 52.015),
             ('_longitude', -0.221), ('_rad_latitude', 0.9078330104248505),
             ('_rad_longitude', -0.0038571776469074684), ('timezone', 0),
             ('units', 'metric')]

        class Test(Point):
            __slots__ = ("TEST", )

            def __init__(self, latitude, longitude):
                super(Test, self).__init__(latitude, longitude)
                self.TEST = "tested"

        a = Test(52.015, -0.221)
        expect(sorted(a.__dict__.items())) == \
            [('TEST', 'tested'), ('_angle', 'degrees'),
            ('_latitude', 52.015), ('_longitude', -0.221),
            ('_rad_latitude', 0.9078330104248505),
            ('_rad_longitude', -0.0038571776469074684), ('timezone', 0),
            ('units', 'metric')]

    def test___repr__(self):
        expect(repr(Point(52.015, -0.221))) == \
            "Point(52.015, -0.221, 'metric', 'degrees', 0)"

    def test___str__(self):
        expect(str(Point(52.015, -0.221))) == 'N52.015°; W000.221°'
        expect(str(Point(52.015, -0.221).__str__(mode="dm"))) == \
            "52°00.90'N, 000°13.26'W"
        expect(str(Point(52.015, -0.221).__str__(mode="dms"))) == \
            """52°00'54"N, 000°13'15"W"""
        expect(str(Point(33.9400, -118.4000).__str__(mode="dms"))) == \
            """33°56'23"N, 118°24'00"W"""
        expect(str(Point(52.015, -0.221).__str__(mode="locator"))) == 'IO92'

    def test___unicode__(self):
        expect(str(Point(52.015, -0.221))) == 'N52.015°; W000.221°'
        expect(str(Point(52.015, -0.221).__unicode__(mode="dm"))) == \
            '52°00.90′N, 000°13.26′W'
        expect(str(Point(52.015, -0.221).__unicode__(mode="dms"))) == \
            '52°00′54″N, 000°13′15″W'
        expect(str(Point(33.9400, -118.4000).__unicode__(mode="dms"))) == \
            '33°56′23″N, 118°24′00″W'
        expect(str(Point(52.015, -0.221).__unicode__(mode="locator"))) == \
            'IO92'

    def test___eq__(self):
        expect(Point(52.015, -0.221)) == Point(52.015, -0.221)

    def test___ne__(self):
        expect(Point(52.015, -0.221)) != Point(52.6333, -2.5)

    def test_to_grid_locator(self):
        Home = Point(52.015, -0.221)
        expect(Home.to_grid_locator("extsquare")) == 'IO92va33'
        expect(Home.to_grid_locator("subsquare")) == 'IO92va'
        expect(Home.to_grid_locator()) == 'IO92'

    def test_distance(self):
        Home = Point(52.015, -0.221)
        dest = Point(52.6333, -2.5)
        expect("%i kM" % Home.distance(dest)) == '169 kM'
        expect("%i kM" % Home.distance(dest, method="sloc")) == '169 kM'

        with expect.raises(ValueError, "Unknown method type `Invalid'"):
            Home.distance(dest, method="Invalid")

        start = Point(36.1200, -86.6700)
        dest = Point(33.9400, -118.4000)
        expect("%i kM" % start.distance(dest)) == '2884 kM'
        start.units = 'imperial'
        expect("%i mi" % start.distance(dest)) == '1792 mi'
        start.units = 'nautical'
        expect("%i nmi" % start.distance(dest)) == '1557 nmi'
        start.units = 'metric'
        expect("%i kM" % start.distance(dest, method="sloc")) == '2884 kM'

    def test_bearing(self):
        expect(int(Point(52.015, -0.221).bearing(Point(52.6333, -2.5)))) == 294
        expect(int(Point(52.6333, -2.5).bearing(Point(52.015, -0.221)))) == 113
        expect(int(Point(36.1200, -86.6700).bearing(Point(33.9400, -118.4000)))) == \
            274
        expect(int(Point(33.9400, -118.4000).bearing(Point(36.1200, -86.6700)))) == \
            76
        expect(Point(52.015, -0.221).bearing(Point(52.6333, -2.5),
                                             format="string")) == 'North-west'

    def test_midpoint(self):
        expect(Point(52.015, -0.221).midpoint(Point(52.6333, -2.5))) == \
            Point(52.3296314054, -1.35253686056, 'metric', 'degrees', 0)
        expect(Point(36.1200, -86.6700).midpoint(Point(33.9400, -118.4000))) == \
            Point(36.082394919, -102.752173705, 'metric', 'degrees', 0)

    def test_final_bearing(self):
        expect(int(Point(52.015, -0.221).final_bearing(Point(52.6333, -2.5)))) == 293
        expect(int(Point(52.6333, -2.5).final_bearing(Point(52.015, -0.221)))) == \
            114
        expect(int(Point(36.1200, -86.6700).final_bearing(Point(33.9400, -118.4000)))) == \
            256
        expect(int(Point(33.9400, -118.4000).final_bearing(Point(36.1200, -86.6700)))) == \
            94
        expect(Point(52.015, -0.221).bearing(Point(52.6333, -2.5),
                                             format="string")) == 'North-west'

    def test_destination(self):
        expect(Point(52.015, -0.221).destination(294, 169)) == \
            Point(52.6116387502, -2.50937408195, 'metric', 'degrees', 0)
        Home = Point(52.015, -0.221, "imperial")
        expect(Home.destination(294, 169 / utils.STATUTE_MILE)) == \
            Point(52.6116387502, -2.50937408195, 'metric', 'degrees', 0)
        Home = Point(52.015, -0.221, "nautical")
        expect(Home.destination(294, 169 / utils.NAUTICAL_MILE)) == \
            Point(52.6116387502, -2.50937408195, 'metric', 'degrees', 0)
        expect(Point(36.1200, -86.6700).destination(274, 2885)) == \
            Point(33.6872799138, -118.327218421, 'metric', 'degrees', 0)

    def test_sunrise(self):
        date = datetime.date(2007, 6, 15)
        expect(Point(52.015, -0.221).sunrise(date)) == datetime.time(3, 40)
        expect(Point(52.6333, -2.5).sunrise(date)) == datetime.time(3, 45)
        expect(Point(36.1200, -86.6700).sunrise(date)) == datetime.time(10, 29)
        expect(Point(33.9400, -118.4000).sunrise(date)) == datetime.time(12, 41)

    def test_sunset(self):
        date = datetime.date(2007, 6, 15)
        expect(Point(52.015, -0.221).sunset(date)) == datetime.time(20, 22)
        expect(Point(52.6333, -2.5).sunset(date)) == datetime.time(20, 35)
        expect(Point(36.1200, -86.6700).sunset(date)) == datetime.time(1, 5)
        expect(Point(33.9400, -118.4000).sunset(date)) == datetime.time(3, 6)

    def test_sun_events(self):
        date = datetime.date(2007, 6, 15)
        expect(Point(52.015, -0.221).sun_events(date)) == \
            (datetime.time(3, 40), datetime.time(20, 22))
        expect(Point(52.6333, -2.5).sun_events(date)) == \
            (datetime.time(3, 45), datetime.time(20, 35))
        expect(Point(36.1200, -86.6700).sun_events(date)) == \
            (datetime.time(10, 29), datetime.time(1, 5))
        expect(Point(33.9400, -118.4000).sun_events(date)) == \
            (datetime.time(12, 41), datetime.time(3, 6))

    def test_inverse(self):
        bearing, dist = Point(52.015, -0.221).inverse(Point(52.6333, -2.5))
        expect(int(bearing)) == 294
        expect(int(dist)) == 169


class TestPoints(TestCase):
    def setUp(self):
        self.locs = Points(["52.015;-0.221", "52.168;0.040", "52.855;0.657"],
                           parse=True)

    def test___repr__(self):
        locations = [Point(0, 0)] * 4
        expect(repr(Points(locations))) == \
            ("Points([Point(0.0, 0.0, 'metric', 'degrees', 0), "
             "Point(0.0, 0.0, 'metric', 'degrees', 0), "
             "Point(0.0, 0.0, 'metric', 'degrees', 0), "
             "Point(0.0, 0.0, 'metric', 'degrees', 0)], "
             "False, 'metric')")

    def test_import_locations(self):
        locations = Points()
        locations.import_locations(["0;0", "52.015 -0.221"])
        expect(repr(locations)) == \
            ("Points([Point(0.0, 0.0, 'metric', 'degrees', 0), "
             "Point(52.015, -0.221, 'metric', 'degrees', 0)], "
             "False, 'metric')")

    def test_distance(self):
        expect("%.3f" % sum(self.locs.distance())) == '111.632'

    def test_bearing(self):
        expect(["%.3f" % x for x in self.locs.bearing()]) == \
            ['46.242', '28.416']

    def test_final_bearing(self):
        expect(["%.3f" % x for x in self.locs.final_bearing()]) == \
            ['46.448', '28.906']

    def test_inverse(self):
        expect(list(self.locs.inverse())) == \
            [(46.24239319802467, 24.629669163425465),
             (28.41617384845358, 87.00207583308533)]

    def test_midpoint(self):
        expect(list(self.locs.midpoint())) == \
            [Point(52.0915720432, -0.0907237539143, 'metric', 'degrees', 0),
            Point(52.5119010509, 0.346088603087, 'metric', 'degrees', 0)]

    def test_range(self):
        expect(list(self.locs.range(Point(52.015, -0.221), 20))) == \
            [Point(52.015, -0.221, 'metric', 'degrees', 0)]

    def test_destination(self):
        expect(list(self.locs.destination(42, 240))) == \
            [Point(53.5956078217, 2.2141813684, 'metric', 'degrees', 0),
             Point(53.7484691495, 2.48403821375, 'metric', 'degrees', 0),
             Point(54.4348338045, 3.14183478498, 'metric', 'degrees', 0)]

    def test_sunrise(self):
        expect(list(self.locs.sunrise(datetime.date(2008, 5, 2)))) == \
            [datetime.time(4, 28), datetime.time(4, 26), datetime.time(4, 21)]

    def test_sunset(self):
        expect(list(self.locs.sunset(datetime.date(2008, 5, 2)))) == \
            [datetime.time(19, 28), datetime.time(19, 27),
             datetime.time(19, 27)]

    def test_sun_events(self):
        expect(list(self.locs.sun_events(datetime.date(2008, 5, 2)))) == \
        [(datetime.time(4, 28), datetime.time(19, 28)),
         (datetime.time(4, 26), datetime.time(19, 27)),
         (datetime.time(4, 21), datetime.time(19, 27))]

    def test_to_grid_locator(self):
        expect(list(self.locs.to_grid_locator("extsquare"))) == \
            ['IO92va33', 'JO02ae40', 'JO02hu85']
        expect(list(self.locs.to_grid_locator("subsquare"))) == \
            ['IO92va', 'JO02ae', 'JO02hu']


class TestTimedPoints(TestCase):
    def speed(self):
        locations = TimedPoints()
        locations.extend([
            TimedPoint(52.015, -0.221,
                time=datetime.datetime(2008, 7, 28, 16, 38)),
            TimedPoint(52.168, 0.040,
                time=datetime.datetime(2008, 7, 28, 18, 38)),
            TimedPoint(52.855, 0.657,
                time=datetime.datetime(2008, 7, 28, 19, 17)),
        ])
        expect(map(lambda s: "%.3f" % s, locations.speed())) == \
            ['12.315', '133.849']


class TestKeyedPoints(TestCase):
    def setUp(self):
        self.locs = KeyedPoints([("home", "52.015;-0.221"),
                                 ("Carol", "52.168;0.040"),
                                 ("Kenny", "52.855;0.657")],
                                parse=True)

    def test_import_locations(self):
        locations = KeyedPoints()
        locations.import_locations([("prime", "0;0"), ("home", "52.015 -0.221")])
        expect(locations) == \
            KeyedPoints({'prime': Point(0.0, 0.0, 'metric', 'degrees', 0),
                         'home': Point(52.015, -0.221, 'metric', 'degrees', 0)},
                         False, 'metric')

    def test_distance(self):
        expect("%.3f" % sum(self.locs.distance(("home", "Carol", "Kenny")))) == '111.632'

    def test_bearing(self):
        expect(["%.3f" % x for x in self.locs.bearing(("home", "Carol", "Kenny"))]) == \
            ['46.242', '28.416']

    def test_final_bearing(self):
        expect(["%.3f" % x for x in self.locs.final_bearing(("home", "Carol", "Kenny"))]) == \
            ['46.448', '28.906']

    def test_inverse(self):
        expect(list(self.locs.inverse(("home", "Carol", "Kenny")))) == \
            [(46.24239319802467, 24.629669163425465),
            (28.41617384845358, 87.00207583308533)]

    def test_midpoint(self):
        expect(list(self.locs.midpoint(("home", "Carol", "Kenny")))) == \
            [Point(52.0915720432, -0.0907237539143, 'metric', 'degrees', 0),
             Point(52.5119010509, 0.346088603087, 'metric', 'degrees', 0)]

    def test_range(self):
        expect(list(self.locs.range(Point(52.015, -0.221), 20))) == \
            [('home', Point(52.015, -0.221, 'metric', 'degrees', 0))]

    def test_destination(self):
        expect(sorted(self.locs.destination(42, 240))) == \
            [('Carol', Point(53.7484691495, 2.48403821375, 'metric', 'degrees', 0)),
             ('Kenny', Point(54.4348338045, 3.14183478498, 'metric', 'degrees', 0)),
             ('home', Point(53.5956078217, 2.2141813684, 'metric', 'degrees', 0))]

    def test_sunrise(self):
        expect(sorted(self.locs.sunrise(datetime.date(2008, 5, 2)))) == \
            [('Carol', datetime.time(4, 26)),
             ('Kenny', datetime.time(4, 21)),
             ('home', datetime.time(4, 28))]

    def test_sunset(self):
        expect(sorted(self.locs.sunset(datetime.date(2008, 5, 2)))) == \
            [('Carol', datetime.time(19, 27)),
             ('Kenny', datetime.time(19, 27)),
             ('home', datetime.time(19, 28))]

    def test_sun_events(self):
        expect(sorted(self.locs.sun_events(datetime.date(2008, 5, 2)))) == \
            [('Carol', (datetime.time(4, 26), datetime.time(19, 27))),
             ('Kenny', (datetime.time(4, 21), datetime.time(19, 27))),
             ('home', (datetime.time(4, 28), datetime.time(19, 28)))]

    def test_to_grid_locator(self):
        expect(sorted(self.locs.to_grid_locator("extsquare"))) == \
            [('Carol', 'JO02ae40'), ('Kenny', 'JO02hu85'), ('home', 'IO92va33')]
        expect(sorted(self.locs.to_grid_locator("subsquare"))) == \
            [('Carol', 'JO02ae'), ('Kenny', 'JO02hu'), ('home', 'IO92va')]