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


import string
from .globals import ADDRTYPE


dec_allowed_ascii = [ord(ch) for ch in string.digits]
dotted_allowed_ascii = dec_allowed_ascii + [ord('.')]
hex_allowed_ascii = [ord(ch) for ch in string.hexdigits]


def filterASCII(key_codes: list, addr_type: int) -> list:
    if addr_type == ADDRTYPE.DEC:
        retval = [key for key in key_codes if key in dec_allowed_ascii]
    elif addr_type == ADDRTYPE.DOTTED:
        retval = [key for key in key_codes if key in dotted_allowed_ascii]
    elif addr_type == ADDRTYPE.HEX:
        retval = [key for key in key_codes if key in hex_allowed_ascii]
    else:
        raise ValueError(f'addr_type of {addr_type} is not valid')
    return retval


def filterChars(chars: str, addr_type: int) -> str:
    if addr_type == ADDRTYPE.DEC:
        retval = ''.join(ch for ch in chars if ch in string.digits)
    elif addr_type == ADDRTYPE.DOTTED:
        retval = ''.join(ch for ch in chars if ch in string.digits or ch in '.')
    elif addr_type == ADDRTYPE.HEX:
        retval = ''.join(ch for ch in chars if ch in string.hexdigits)
    else:
        raise ValueError(f'addr_type of {addr_type} is not valid')
    return retval


def isAllowedASCII(key_code: int, addr_type: int) -> bool:
    if addr_type == ADDRTYPE.DEC:
        retval = key_code in dec_allowed_ascii
    elif addr_type == ADDRTYPE.DOTTED:
        retval = key_code in dotted_allowed_ascii
    elif addr_type == ADDRTYPE.HEX:
        retval = key_code in hex_allowed_ascii
    else:
        raise ValueError(f'addr_type of {addr_type} is not valid')
    return retval


def isAllowedChar(char: str, addr_type: int) -> bool:
    if len(char) != 1:
        raise ValueError(f'char input includes more than one character: {char}')
    if addr_type == ADDRTYPE.DEC:
        retval = char in string.digits
    elif addr_type == ADDRTYPE.DOTTED:
        retval = char in string.digits or char in '.'
    elif addr_type == ADDRTYPE.HEX:
        retval = char in string.hexdigits
    else:
        raise ValueError(f'addr_type of {addr_type} is not valid')
    return retval
