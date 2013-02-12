#!/usr/bin/env python

from __future__ import print_function

import glob
from os import path, getenv

# if PAPARAZZI_HOME not set, then assume the tree containing this
# file is a reasonable substitute
paparazzi_home = getenv("PAPARAZZI_HOME", path.normpath(path.join(
                        path.dirname(path.abspath(__file__)),
                        '../../../')))

# Directories
paparazzi_firmwares = path.join(paparazzi_home, "conf/firmwares/")
paparazzi_modules   = path.join(paparazzi_home, "conf/modules/")
paparazzi_airframes = path.join(paparazzi_home, "conf/airframes/")


