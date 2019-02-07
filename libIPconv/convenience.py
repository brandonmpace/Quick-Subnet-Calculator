#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (C) 2018, 2019 Brandon M. Pace
#
# This file is part of Quick Subnet Calculator
#
# Quick Subnet Calculator is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Quick Subnet Calculator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with Quick Subnet Calculator.
# If not, see <https://www.gnu.org/licenses/>.


"""This file has small convenience functions that don't align with the goal of other files"""


def get_byte_width(value: int):
    """Returns number of bytes needed to represent the integer value. (useful for reversing byte order)"""
    return (value.bit_length() + 7) // 8
