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


import GUI
import libIPconv as conv
import wx


class MainFrame(GUI.SubnetCalcFrame):
    def __init__(self, *args, **kwds):
        GUI.SubnetCalcFrame.__init__(self, *args, **kwds)

        self.text_ctrl_dotted.addr_type = conv.ADDRTYPE.DOTTED
        self.text_ctrl_dotted.is_mask = False

        self.text_ctrl_mask.addr_type = conv.ADDRTYPE.DOTTED
        self.text_ctrl_mask.mask_type = conv.MASKTYPE.DOTTED
        self.text_ctrl_mask.is_mask = True

        main_calculator.set_value(f'{self.text_ctrl_dotted.GetValue()}/{self.spin_ctrl_mask.GetValue()}')
        self.text_ctrl_mask.SetValue(conv.cidrToDottedQuadStr(self.slider_mask.GetValue()))
        self.update()

    def on_char(self, event):
        super().on_char(event)

        if event.GetSkipped():
            return  # return if the key was already allowed

        event_control = event.GetEventObject()
        event_key = event.GetKeyCode()

        if conv.filters.isAllowedASCII(event_key, event_control.addr_type):
            event.Skip()
            if event_control.addr_type == conv.ADDRTYPE.DOTTED:
                control_content = event_control.GetValue()
                control_selection = event_control.GetSelection()

                # Insert the new character at the insertion point, over-writing any selected characters
                first = control_content[0:control_selection[0]]
                last = control_content[control_selection[1]:]
                check_value = first + chr(event_key) + last

                if event.GetSkipped():
                    check_value = conv.augment.pad_dotted_right(check_value)
                    if not conv.isValidIPv4(check_value, conv.ADDRTYPE.DOTTED):
                        event.Skip(False)
            else:
                event.Skip()

    def on_paste(self, event):
        success, pasted_string = super().on_paste(event)

        event_object = event.GetEventObject()

        filtered_string = conv.filters.filterChars(pasted_string, event_object.addr_type)
        if not filtered_string:
            return  # nothing to insert

        control_content = event_object.GetValue()
        control_selection = event_object.GetSelection()

        # Insert the new string at the insertion point, over-writing any selected characters
        first = control_content[0:control_selection[0]]
        last = control_content[control_selection[1]:]
        final_value = first + filtered_string + last

        event_object.SetValue(final_value)
        event_object.SetInsertionPoint(len(first + filtered_string))

    def on_slider(self, event):
        super().on_slider(event)
        self.update(self.slider_mask)

    def on_spinctrl(self, event):
        super().on_spinctrl(event)
        self.update(self.spin_ctrl_mask)

    def on_text(self, event):
        event_object = event.GetEventObject()
        self.update(trigger_object=event_object)

    def update(self, trigger_object=None):
        if trigger_object in [self.slider_mask, self.spin_ctrl_mask, self.text_ctrl_mask]:
            mask_object = trigger_object
        else:
            mask_object = self.spin_ctrl_mask

        if main_calculator.set_value(f'{self.text_ctrl_dotted.GetValue()}/{mask_object.GetValue()}'):
            new_info = main_calculator.subnet_info()
            self.text_ctrl_network.SetValue(new_info['network_addr'])
            self.text_ctrl_broadcast.SetValue(new_info['broadcast_addr'])
            self.text_ctrl_first_addr.SetValue(new_info['first_addr'])
            self.text_ctrl_last_addr.SetValue(new_info['last_addr'])
            self.text_ctrl_usable.SetValue(new_info['usable'])
            if mask_object is self.text_ctrl_mask:
                self.slider_mask.SetValue(int(new_info['prefix']))
                self.spin_ctrl_mask.SetValue(int(new_info['prefix']))
            else:
                self.text_ctrl_mask.SetValue(new_info['netmask'])
        else:
            self.reset_results()


class MainApp(wx.App):
    def OnInit(self):
        self.frame_main = MainFrame(None, wx.ID_ANY, "", name='MainFrame')
        self.SetTopWindow(self.frame_main)
        self.frame_main.Show()
        return True


if __name__ == "__main__":
    main_calculator = conv.SubnetCalculator()
    app = MainApp(0)
    app.MainLoop()
