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


from .convregex import *
from .globals import *


def isValidIPv4(input_value, addr_type: int = ADDRTYPE.NONE, strict: bool = False) -> bool:
    """
    Accepts string or int value and returns True if it is a value in the range of valid IPv4 addresses.
    The addr_type argument should be a value from the ADDRTYPE enum. If input is int you must use NONE or DEC addr_type.
    The string can be a dotted-quad format, hex format, or decimal format. (no leading or trailing whitespace)
    strict mode will require dotted-quad format to include four valid octets
    """
    check_value = -1

    if isinstance(input_value, str):
        if '.' in input_value and (addr_type in [ADDRTYPE.NONE, ADDRTYPE.DOTTED]):
            # Confirm match for dotted-quad format
            if len(input_value) <= 15 and IP_RECLIST[ADDRTYPE.DOTTED].fullmatch(input_value):
                if strict and not DOTTEDQUADIP_STRICTREC.fullmatch(input_value):
                    check_value = -2
                else:
                    check_value = 0
            else:
                check_value = -3
        elif IP_RECLIST[ADDRTYPE.DEC].fullmatch(input_value) and (addr_type in [ADDRTYPE.NONE, ADDRTYPE.DEC]):
            check_value = int(input_value)
        elif IP_RECLIST[ADDRTYPE.HEX].fullmatch(input_value) and (addr_type in [ADDRTYPE.NONE, ADDRTYPE.HEX]):
            check_value = int(input_value, 16)
    elif isinstance(input_value, int):
        if addr_type in [ADDRTYPE.NONE, ADDRTYPE.DEC]:
            check_value = input_value
        else:
            raise ValueError('Type int input_value passed with incompatible addr_type of {addr_type}')
    else:
        raise ValueError(f'Expected input type str or int. Got {type(input_value)}')

    return (check_value >= 0) and (check_value <= V4_MAX_VALUE)


def isValidIPv4Mask(input_value, mask_type: int = MASKTYPE.NONE) -> bool:
    """
    Accepts string or int value and returns True if it is a value in the range of valid IPv4 subnet masks.
    The mask_type argument should be a value from the MASKTYPE enum. If input is int you must use NONE or DEC mask_type.
    The string can be a dotted-quad format, hex format, or decimal format. (no leading or trailing whitespace)
    """
    check_value = -1

    if isinstance(input_value, str):
        if '.' in input_value and (mask_type in [MASKTYPE.NONE, MASKTYPE.DOTTED]):
            # Confirm match for dotted-quad format
            if len(input_value) <= 15 and DOTTEDV4MASK_REC.fullmatch(input_value):
                check_value = 0
            else:
                check_value = -2
        elif IP_RECLIST[MASKTYPE.DEC].fullmatch(input_value) and (mask_type in [MASKTYPE.NONE, MASKTYPE.DEC]):
            check_value = int(input_value)
        elif IP_RECLIST[MASKTYPE.HEX].fullmatch(input_value) and (mask_type in [MASKTYPE.NONE, MASKTYPE.HEX]):
            check_value = int(input_value, 16)
    elif isinstance(input_value, int):
        if mask_type in [MASKTYPE.NONE, MASKTYPE.DEC]:
            check_value = input_value
        else:
            raise ValueError(f'Type int input_value passed with incompatible mask_type of {mask_type}')
    else:
        raise ValueError(f'Expected input type str or int. Got {type(input_value)}')

    return check_value in V4_CIDR_MASKS


# TODO: decide if this will all go away or just use ipaddress module for backend (especially for IPv6)


def validate_addr(addr: int, version: int):
    return (addr >= 0) and (addr <= (V6_MAX_VALUE if version == 6 else V4_MAX_VALUE))


def validate_mask(addr: int, version: int):
    return addr in (V6_CIDR_MASKS if version == 6 else V4_CIDR_MASKS)


def validate_version(version: int):
    return version in [4, 6]
