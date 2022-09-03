#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 J. Elms
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

PREAMBLE_NBYTES = 128
LICH_NBYTES = 128
FRAME_NBYTES = 128 + 16

class superframe_combiner(gr.basic_block):
    """
    combine preamble, LICH and normal frames into final PHY stream
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="superframe_combiner",
            in_sig=[numpy.byte, numpy.byte, numpy.byte],
            out_sig=[numpy.byte, ])
        self.reset = True
        self.buffer = numpy.array([], dtype=numpy.byte)

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        if self.reset:
            ninput_items_required[0] = PREAMBLE_NBYTES
            ninput_items_required[1] = LICH_NBYTES
        ninput_items_required[2] = FRAME_NBYTES

    def general_work(self, input_items, output_items):
        if self.reset:
            if len(input_items[0]) >= PREAMBLE_NBYTES and \
               len(input_items[1]) >= LICH_NBYTES:
                self.buffer = numpy.concatenate((self.buffer, input_items[0]))
                self.consume_each(len(input_items[0]))
                self.buffer = numpy.concatenate((self.buffer, input_items[1]))
                self.consume_each(len(input_items[1]))
                self.reset = False

        if not self.reset:
            self.buffer = numpy.concatenate((self.buffer, input_items[2]))
            self.consume_each(len(input_items[2]))

        nout = min(len(output_items[0]), len(self.buffer))
        print('nout', nout, len(output_items[0]), len(self.buffer))
        output_items[0][:nout] = self.buffer[:nout]
        self.buffer = self.buffer[nout:]

        return nout
