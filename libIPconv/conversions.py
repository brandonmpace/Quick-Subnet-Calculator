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


def cidrToDec(input_value) -> int:
    if isinstance(input_value, str) and input_value.isdecimal():
        int_value = int(input_value)
    elif isinstance(input_value, int):
        int_value = input_value
    else:
        raise TypeError(f'expected decimal str or int, got type {type(input_value)} with value {input_value}')
    if int_value in V4_CIDR_BITCOUNTS:
        return_value = (V4_MAX_VALUE << (32 - int_value)) & V4_MAX_VALUE
    else:
        raise ValueError(f'{input_value} is not a valid CIDR bit count')
    return return_value


def cidrToDecStr(input_value) -> str:
    return str(cidrToDec(input_value))


def cidrToDottedQuadStr(input_value) -> str:
    if isinstance(input_value, str) and input_value.isdecimal():
        int_value = int(input_value)
    elif isinstance(input_value, int):
        int_value = input_value
    else:
        raise TypeError(f'expected decimal str or int, got type {type(input_value)} with value {input_value}')

    if (int_value < 0) or (int_value > 32):
        raise ValueError(f'value {int_value} it outside expected range of 0-32')

    mask_value = cidrToDec(int_value)
    return_value = decToDottedQuadStr(mask_value)
    return return_value


def convertAddrStrToType(input_value: str, input_type: int, output_type: int, reverse: bool = False, safe: bool = False) -> str:
    """
    Be sure to use isValidIPv4() before this to sanity-check your input!
    :param input_value: str value to convert
    :param input_type: int value type from ADDRTYPE enum determining what the source type is
    :param output_type: int value type from the ADDRTYPE enum determining what the destination type is
    :param reverse: bool for whether or not to reverse the byte-order
    :param safe: bool for whether or not to avoid raising exceptions
    :return: str converted value or '' on error/failure when safe is True
    """
    return_value = ''
    try:
        if input_type == output_type:
            raise ValueError('output_type should be different than input_type')

        if input_type == ADDRTYPE.DEC:
            if output_type == ADDRTYPE.DOTTED:
                return_value = decStrToDottedQuadStr(input_value, reverse)
            elif output_type == ADDRTYPE.HEX:
                return_value = decStrToHexStr(input_value, reverse)
        elif input_type == ADDRTYPE.DOTTED:
            if output_type == ADDRTYPE.DEC:
                return_value = dottedQuadStrToDecStr(input_value, reverse)
            elif output_type == ADDRTYPE.HEX:
                return_value = dottedQuadStrToHexStr(input_value, reverse)
        elif input_type == ADDRTYPE.HEX:
            if output_type == ADDRTYPE.DEC:
                return_value = hexToDecStr(input_value, reverse)
            elif output_type == ADDRTYPE.DOTTED:
                int_value = hexToDecStr(input_value, False)
                return_value = decStrToDottedQuadStr(int_value, reverse)
    except ValueError:
        if not safe:
            raise
        else:
            return ''
    else:
        return return_value


def convertMaskStrToType(input_value: str, input_type: int, output_type: int, safe: bool = False) -> str:
    """
    Be sure to use isValidIPv4() before this to sanity-check your input!
    :param input_value: str value to convert
    :param input_type: int value type from MASKTYPE enum determining what the source type is
    :param output_type: int value type from the MASKTYPE enum determining what the destination type is
    :param safe: bool for whether or not to avoid raising exceptions
    :return: str converted value or '' on error/failure when safe is True
    """
    return_value = ''
    reverse = False
    try:
        if input_type == output_type:
            raise ValueError('output_type should be different than input_type')

        if input_type == MASKTYPE.CIDR:
            if output_type == MASKTYPE.DOTTED:
                return_value = cidrToDottedQuadStr(input_value)
            elif output_type == MASKTYPE.DEC:
                return_value = cidrToDecStr(input_value)
            elif output_type == MASKTYPE.HEX:
                return_value = decStrToHexStr(cidrToDecStr(input_value))
        elif input_type == MASKTYPE.DOTTED:
            if output_type == MASKTYPE.CIDR:
                return_value = dottedQuadStrToCIDRStr(input_value)
            elif output_type == MASKTYPE.DEC:
                return_value = cidrToDecStr(dottedQuadStrToCIDRStr(input_value))
            elif output_type == MASKTYPE.HEX:
                return_value = dottedCIDRToHex(input_value)
        elif input_type == MASKTYPE.HEX:
            if output_type == MASKTYPE.CIDR:
                return_value = decToCIDRStr(hexToDec(input_value))
            if output_type == MASKTYPE.DEC:
                return_value = hexToDecCIDRStr(input_value)
            elif output_type == MASKTYPE.DOTTED:
                return_value = decStrToDottedQuadStr(hexToDecCIDRStr(input_value))
    except ValueError:
        if not safe:
            raise
        else:
            return ''
    else:
        return return_value


def decStrToDottedQuadStr(input_value: str, reverse: bool = False) -> str:
    if RECLIST[ADDRTYPE.DEC].fullmatch(input_value):
        return decToDottedQuadStr(int(input_value), reverse)
    else:
        return ''


def decToDottedQuadList(input_value: int, reverse: bool = False) -> list:
    if (input_value < 0) or (input_value > V4_MAX_VALUE):
        raise ValueError(f'Input value is outside of IPv4 range: {input_value}')
    if reverse:
        byte_order = 'little'
    else:
        byte_order = 'big'
    return [octet for octet in input_value.to_bytes(4, byte_order)]


def decStrToHexStr(input_value: str, reverse: bool = False) -> str:
    return_value = ''
    if input_value.isdecimal():
        if reverse:
            byte_order = 'little'
        else:
            byte_order = 'big'
        int_value = int(input_value)
        return_value = int_value.to_bytes(((int_value.bit_length() + 7) // 8), byte_order).hex()
    return return_value


def decToCIDR(input_value: int) -> int:
    if isinstance(input_value, str) and input_value.isdecimal():
        int_value = int(input_value)
    elif isinstance(input_value, int):
        int_value = input_value
    else:
        raise TypeError(f'expected decimal str or int, got type {type(input_value)} with value {input_value}')
    if int_value not in V4_CIDR_MASKS:
        raise ValueError(f'{input_value} is not a valid CIDR mask')
    cidr_value = bin(int_value).count('1')
    return cidr_value


def decToCIDRStr(input_value) -> str:
    return str(decToCIDR(input_value))


def decToDottedQuadStr(input_value: int, reverse: bool = False) -> str:
    return '.'.join([str(octet) for octet in decToDottedQuadList(input_value, reverse)])


def dottedCIDRToHex(input_value: str):
    dec_value = dottedQuadStrToDecStr(input_value)
    if dec_value in V4_CIDR_MASKS:
        return dottedQuadStrToHexStr(input_value)
    else:
        raise ValueError(f'{input_value} is not a valid CIDR mask')


def dottedQuadStrToCIDR(input_value: str) -> int:
    dec_value = int(dottedQuadStrToDecStr(input_value))
    if dec_value not in V4_CIDR_MASKS:
        raise ValueError(f'{input_value} is not a valid CIDR mask')
    cidr_value = decToCIDR(dec_value)
    return cidr_value


def dottedQuadStrToCIDRStr(input_value: str) -> str:
    return str(dottedQuadStrToCIDR(input_value))


def dottedQuadStrToDecStr(input_value: str, reverse: bool = False) -> str:
    split_value = [int(value) for value in input_value.split('.')]
    if reverse:
        byte_order = 'little'
    else:
        byte_order = 'big'
    return str(int.from_bytes(split_value, byte_order))


def dottedQuadStrToHexStr(input_value: str, reverse: bool = False) -> str:
    split_value = [int(value) for value in input_value.split('.')]
    if reverse:
        split_value.reverse()
    byte_value = bytes(split_value)
    return byte_value.hex()


def hexToDec(input_value: str, reverse: bool = False) -> int:
    if RECLIST[ADDRTYPE.HEX].fullmatch(input_value):
        trimmed = input_value.lstrip('0xX')
        if len(trimmed) % 2:
            trimmed = '0' + trimmed
        byte_value = bytes.fromhex(trimmed)
        if reverse:
            byte_order = 'little'
        else:
            byte_order = 'big'
        return int.from_bytes(byte_value, byte_order)
    else:
        return -1


def hexToDecCIDR(input_value: str):
    dec_value = hexToDec(input_value)
    if dec_value in V4_CIDR_MASKS:
        return dec_value
    else:
        raise ValueError(f'{input_value} is not a valid CIDR mask')


def hexToDecCIDRStr(input_value: str):
    return str(hexToDecCIDR(input_value))


def hexToDecStr(hex_addr: str, reverse: bool = False) -> str:
    check_value = hexToDec(hex_addr, reverse)
    return '' if (check_value == -1) else str(check_value)
