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

class vector_concat(gr.basic_block):
    """
    docstring for block vector_concat
    """
    def __init__(self, dtype, input_vlens=[1,1], verbose=False):
        inputs = [(dtype, i) for i in input_vlens]
        gr.basic_block.__init__(self,
            name="vector_concat",
            in_sig=inputs,
            out_sig=[(dtype, sum(input_vlens)), ])

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        count = numpy.min([x.shape[0] for x in (output_items + input_items)])
        for i in range(count):
            output_items[0][i, :] = numpy.concatenate(
                tuple(x[i,:] for x in input_items) )
        self.consume_each(count)
        return count
