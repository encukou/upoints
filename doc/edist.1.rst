edist.py
========

Simple command line coordinate processing
"""""""""""""""""""""""""""""""""""""""""

:Author: James Rowe <jnrowe@gmail.com>
:Date: 2008-01-22
:Copyright: GPL v3
:Manual section: 1
:Manual group: GIS

SYNOPSIS
--------

    edist.py [OPTIONS] location...

DESCRIPTION
-----------

**edist.py** operates on one, or more, locations specified in various
formats.  For example, a location string of "52.015;\-0.221" would be
interpreted as 52.015 degrees North by 0.221 degrees West, as would
"52d0m54s N 000d13m15s W".  Positive values can be specified with a "+"
prefix, but it isn't required.

It is possible to use Maidenhead locators, such as "IO92" or "IO92va",
for users who are accustomed to working with them.

Users can maintain a local configuration file that lists locations with
assigned names, and then use the names on the command line.  This makes
command lines much easier to read, and also makes reusing locations at
a later date simpler.  See `CONFIGURATION FILE`_.

OPTIONS
-------

--version
    show program's version number and exit

-h, --help
    show this help message and exit

--config-file = **file**
    Config file to read custom locations from

--csv-file = **csv_file**
    CSV file (gpsbabel format) to read route/locations from

Calculation modes
'''''''''''''''''

-p, --print
    pretty print the location(s)

-d, --distance
    calculate the distance between locations

-b, --bearing
    calculate the initial bearing between locations

-f, --final-bearing
    calculate the final bearing between locations

-r **range**, --range **range**
    calculate whether locations are within a given **range**

-s **distance@bearing**, --destination **distance@bearing**
    calculate the destination for a given distance and bearing

-y, --sunrise
    calculate the sunrise time for a given location

-z, --sunset
    calculate the sunset time for a given location

-F, --flight-plan
    calculate the flight plan corresponding to locations (route)

-S **speed**, --speed **speed**
    speed to calculate elapsed time

Output options
''''''''''''''

--unicode
    produce Unicode output

--ascii
    produce ASCII output

-o **FORMAT**, --format **FORMAT**
    produce output in dms, dm, d format or Maidenhead locator

-l **LOCATOR**, --locator **LOCATOR**
    accuracy of Maidenhead locator output

-g, --string
    display named bearings

-v, --verbose
    produce verbose output

-q, --quiet
    output only results and errors

-u **km**, --units **km**
    display distances in km(default), mile or nm

-u **km**, --units **km**
   display distances in kilometres(default), statute miles or nautical miles

-t **h**, --time **h**
   display time in hours(default), minutes or seconds


CONFIGURATION FILE
------------------

The configuration file, by default **~/.edist.conf**, is a simple
**INI** format file, with sections headers defining the name of the
location and their data defining the actual position.  You can define
locations by either their latitude and longitude, or with a Maidenhead
locator string.  Any options that aren't handled will simply ignored.
For example::

    [Home]
    latitude = 52.015
    longitude = -0.221

    [Cambridge]
    latitude = 52.200
    longitude = 0.183

    [Pin]
    locator = IO92

With the above configuration file one could find the distance from
**Home** to **Cambridge** using **edist.py --distance Home Cambridge**.

BUGS
----

None known.

AUTHOR
------

Written by `James Rowe <mailto:jnrowe@gmail.com>`__

RESOURCES
---------

Home page: http://github.com/JNRowe/upoints

COPYING
-------

Copyright © 2006-2010  James Rowe.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

.. vim: set ft=rst ts=8 sw=4 tw=80 et: