#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 J. Elms(KM6VMZ)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#


import numpy
from gnuradio import gr
from .m17_lich import crc16_m17

class add_crc(gr.basic_block):
    """
    docstring for block add_crc
    """
    def __init__(self, vlen):
        gr.basic_block.__init__(self,
            name="add_crc",
            in_sig=[(numpy.byte, vlen), ],
            out_sig=[(numpy.byte, vlen + 2), ])
        self.vlen = vlen

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        vlen = self.vlen
        count = min(input_items[0].shape[0], output_items[0].shape[0])
        for i in range(count):
            output_items[0][i,:vlen] = input_items[0][i,:]
            crc = crc16_m17(input_items[0][i,:])
            output_items[0][i,vlen:(vlen+2)] = [(crc >> 8) & 0xFF, crc & 0xFF]

        self.consume_each(count)
        return count
