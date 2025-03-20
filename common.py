#!/usr/bin/python
# -*- coding: latin-1 -*-

# Reggie Next - New Super Mario Bros. Wii Level Editor
# Milestone 4
# Copyright (C) 2009-2020 Treeki, Tempus, angelsl, JasonP27, Kamek64,
# MalStar1000, RoadrunnerWMC, AboodXD, John10v10, TheGrop, CLF78,
# Zementblock, Danster64

# This file is part of Reggie Next.

# Reggie Next is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Reggie Next is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Reggie Next.  If not, see <http://www.gnu.org/licenses/>.


# common.py
# API for general Wii-related functions.
# From the wii.py library.


################################################################
################################################################


import os.path
import struct
import sys


def clamp(var, min, max):
    if var < min: var = min
    if var > max: var = max
    return var


def find_first_available_id(used: set, maximum: int, minimum: int = 0):
    """
    Returns the smallest integer in the range [minimum = 0, maximum) that is
    not in the given set. If there is no such integer, None is returned.
    """
    for i in range(minimum, maximum):
        if i not in used:
            return i

    return None

