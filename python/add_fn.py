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

class add_fn(gr.basic_block):
    """
    docstring for block add_fn
    """
    def __init__(self, fn_init=0):
        gr.basic_block.__init__(self,
            name="add_fn",
            in_sig=[(numpy.byte, 16), ],
            out_sig=[(numpy.byte, 18), ])
        self.fn = fn_init

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        nout = min(output_items[0].shape[0], input_items[0].shape[0])
        for i in range(nout):
            output_items[0][i,:] = numpy.concatenate(
                ([self.fn >> 8, self.fn & 0xff],
                input_items[0][i,:]))
            self.fn += 1
        self.consume_each(nout)
        return nout
