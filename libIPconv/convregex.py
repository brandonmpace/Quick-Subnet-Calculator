#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (C) 2014, 2018 Brandon M. Pace
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


import re


# regex for matching decimal, dotted-quad and hex IP - including compiled versions for performance
DECIP_RE = r'^([0-9]{1,10})$'
DECIP_REC = re.compile(DECIP_RE)

HEXIP_RE = r'^((0[xX])?[0-9a-fA-F]{1,8})$'
HEXIP_REC = re.compile(HEXIP_RE)

# Requires 0-255 before and after each '.', up to 3 instances of '.'
DOTTEDQUADIP_RE = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){0,3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
DOTTEDQUADIP_REC = re.compile(DOTTEDQUADIP_RE)

IP_RELIST = [DECIP_RE, HEXIP_RE, DOTTEDQUADIP_RE]
IP_RECLIST = [DECIP_REC, HEXIP_REC, DOTTEDQUADIP_REC]

# Requires 0-255 before and after each '.' with 3 instances of '.'
DOTTEDQUADIP_STRICTRE = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
DOTTEDQUADIP_STRICTREC = re.compile(DOTTEDQUADIP_STRICTRE)

# Strict, does not allow for wildcard masks
DOTTEDV4MASK_RE = r'^(((255\.){3}(255|254|252|248|240|224|192|128|0+))|((255\.){2}(255|254|252|248|240|224|192|128|0+)\.0)|((255\.)(255|254|252|248|240|224|192|128|0+)(\.0+){2})|((255|254|252|248|240|224|192|128|0+)(\.0+){3}))$'
DOTTEDV4MASK_REC = re.compile(DOTTEDV4MASK_RE)


# regex for matching general decimal and hex - including compiled versions for performance
DEC_RE = r'^([0-9]+)$'
DEC_REC = re.compile(DEC_RE)

HEX_RE = r'^((0[xX])?[0-9a-fA-F]+)$'
HEX_REC = re.compile(HEX_RE)

RELIST = [DEC_RE, HEX_RE]
RECLIST = [DEC_REC, HEX_REC]
