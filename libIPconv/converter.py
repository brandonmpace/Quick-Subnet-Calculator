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


from .conversions import *


class Converter(object):
    _supported_addr_types = [ADDRTYPE.DEC, ADDRTYPE.DOTTED, ADDRTYPE.HEX]

    def __init__(self, safe=True):
        self.reverse = False
        self.safe = safe
        self._callbacks = {key: None for key in self._supported_addr_types}
        self._values = {key: '' for key in self._supported_addr_types}

    def is_addr_type_supported(self, addr_type: int) -> bool:
        return addr_type in self._supported_addr_types

    def register_callback(self, callback_function, addr_type: int):
        """
        Allows calling a single-argument function for values changed as a result of set_value.
        When one value changes, callbacks for the others are called with the converted string value,
        which can be '' if the set value is invalid.
        :param callback_function: function that takes a single argument (the new value)
        :param addr_type: int from the ADDRTYPE enum
        :return: None
        """
        if not callable(callback_function):
            raise ValueError('callback_function is not callable')
        self._check_addr_type(addr_type)

        self._callbacks[addr_type] = callback_function

    def reset_values(self):
        for key in self._values.keys():
            self._values[key] = ''

    def run_callbacks(self, addr_type: int):
        """Run callback functions for types other than the input addr_type"""
        for typeval in self._supported_addr_types:
            if (typeval != addr_type) and self._callbacks[typeval]:
                self._callbacks[typeval](self._values[typeval])

    def run_conversions(self, addr_type: int):
        """Convert the currently stored value of addr_type to other types"""
        self._check_addr_type(addr_type)
        for typeval in self._supported_addr_types:
            if typeval != addr_type:
                self._values[typeval] = convertAddrStrToType(
                    self._values[addr_type], addr_type, typeval, reverse=self.reverse, safe=self.safe)

    def set_value(self, value: str, addr_type: int):
        self._check_addr_type(addr_type)

        self._values[addr_type] = value

        if not value:
            self.reset_values()
        else:
            self.run_conversions(addr_type)

        # call callbacks
        self.run_callbacks(addr_type)

    def _check_addr_type(self, addr_type: int):
        if not self.is_addr_type_supported(addr_type):
            raise ValueError(f'addr_type value of {addr_type} is not supported')
