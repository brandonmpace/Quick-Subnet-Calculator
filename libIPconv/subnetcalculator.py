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


import ipaddress


network_classes = {4: ipaddress.IPv4Network, 6: ipaddress.IPv6Network}


class SubnetCalculator(object):
    def __init__(self, safe=True):
        self.safe = safe
        self._value = None

    def set_value(self, value, version: int = 4) -> bool:
        network_class = network_classes[version]
        # TODO: handle different input representations to allow supporting more than ipaddress module does
        try:
            self._value = network_class(value, strict=False)
        except ValueError:
            if not self.safe:
                raise
            else:
                return False

        return True

    def subnet_info(self) -> dict:
        info_dict = {
            'broadcast_addr': '', 'first_addr': '', 'last_addr': '', 'netmask': '', 'network_addr': '', 'prefix': '',
            'usable': ''
        }
        if self._value:
            usable = (self._value.num_addresses - 2) if (self._value.num_addresses > 2) else self._value.num_addresses
            first_addr = (
                (self._value.network_address + 1) if (self._value.num_addresses > 2) else self._value.network_address
            )
            last_addr = (
                (self._value.broadcast_address - 1) if (self._value.num_addresses > 2) else self._value.broadcast_address
            )
            try:
                info_dict['broadcast_addr'] = f'{self._value.broadcast_address}'
                info_dict['first_addr'] = f'{first_addr}'
                info_dict['last_addr'] = f'{last_addr}'
                info_dict['netmask'] = f'{self._value.netmask}'
                info_dict['network_addr'] = f'{self._value.network_address}'
                info_dict['prefix'] = f'{self._value.prefixlen}'
                info_dict['usable'] = f'{usable}'
            except ValueError:
                if not self.safe:
                    raise
        elif not self.safe:
            raise AttributeError(f'Value has not yet been set successfully! Hint: call .set_value() first')

        return info_dict
