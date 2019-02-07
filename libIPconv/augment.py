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


"""This module contains functions for string manipulation/augmentation"""


def add_byte_separator(input_value: str, sep: str = ':') -> str:
    """Add a separator between each byte in hex representation. Beginning gets padded to avoid unexpected results."""
    if input_value.startswith('0x') or input_value.startswith('0X'):
        prefix = input_value[0:2]
        work_string = input_value.lstrip('0xX')
    else:
        prefix = ''
        work_string = input_value

    # using iter() keeps memory usage low
    if len(work_string) % 2:
        iterable = iter(pad_even_length(work_string))
    else:
        iterable = iter(work_string)
    padded_string = sep.join(first_char + second_char for first_char, second_char in zip(iterable, iterable))
    if prefix:
        padded_string = f'{prefix}{padded_string}'
    return padded_string


def pad_dotted_right(input_value: str) -> str:
    """Pad dotted-quad IPv4 string on the right side until they are valid. e.g. 255. becomes 255.0.0.0"""
    octet_values = [value if value else '0' for value in input_value.split('.')]
    return_value = '.'.join(octet_values + ['0' for needed_padding in range(4 - len(octet_values))])
    return return_value


def pad_even_length(input_value: str, pad_value: str = '0') -> str:
    """Add padding to beginning of string until its length is divisible by 2"""
    if not pad_value:
        raise ValueError('pad_value must be at least one character')
    check_value = input_value
    while check_value % 2:
        check_value = ''.join([pad_value, check_value])
    else:
        return check_value
