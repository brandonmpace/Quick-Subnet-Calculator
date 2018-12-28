#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Brandon M. Pace
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


import enum


# Byte-order strings, for use with bytes() objects
BIG = 'big'  # Network-first byte-order
LITTLE = 'little'  # Host-first byte-order

# 4294967295 or 255.255.255.255
V4_MAX_VALUE = 0xffffffff

# 0-32
V4_CIDR_BITCOUNTS = [x for x in range(33)]

# integer list of bit-masks for each CIDR mask from highest to lowest value
# (integer equivalents of 255.255.255.255, 255.255.255.254, 255.255.255.252, etc. down to 0.0.0.0)
V4_CIDR_MASKS = [(V4_MAX_VALUE << offset) & V4_MAX_VALUE for offset in V4_CIDR_BITCOUNTS]

# integer list of bit-masks for each octet of an IPv4 address
V4_OCTET_MASKS = [255 << (8*octet_offset) for octet_offset in range(4)]


# 340282366920938463463374607431768211455 or ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff
V6_MAX_VALUE = 0xffffffffffffffffffffffffffffffff

# 0-128
V6_CIDR_BITCOUNTS = [x for x in range(129)]

# integer list of bit-masks for each CIDR mask from highest to lowest value
# (integer equivalents of ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff, etc. down to ::)
V6_CIDR_MASKS = [(V6_MAX_VALUE << offset) & V6_MAX_VALUE for offset in V6_CIDR_BITCOUNTS]

# integer list of bit-masks for each octet of an IPv4 address
V6_OCTET_MASKS = [255 << (8*octet_offset) for octet_offset in range(4)]


# TODO: consolidate into representation types instead and change CIDR to PREFIX

# enum values that can be used for index of the IP_RE*LIST items
@enum.unique
class ADDRTYPE(enum.IntEnum):
    NONE = -1
    DEC = 0
    HEX = 1
    DOTTED = 2

@enum.unique
class MASKTYPE(enum.IntEnum):
    NONE = -1
    DEC = 0
    HEX = 1
    DOTTED = 2
    CIDR = 3

@enum.unique
class VALTYPE(enum.IntEnum):
    ADDR = 16
    MASK = 32
