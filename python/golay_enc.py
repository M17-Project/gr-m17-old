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


def parity(val):
    accum = 0
    while val > 0:
        accum = accum ^ (val & 1)
        val = val >>1
    return accum

class golay_enc(gr.basic_block):
    """
    golay_enc
     - process unpacked bits
     - process packed bits
       - must provide vlen=3*i (always even number of symbols)
    """
    def __init__(self, unpacked=True, vlen=12):
        gr.basic_block.__init__(self,
            name="golay_enc",
            in_sig=[(numpy.byte, vlen), ],
            out_sig=[(numpy.byte, 2 * vlen), ])

        # https://www.johndcook.com/blog/2019/10/18/golay-code/
        g_str = """100000000000101000111011
        010000000000110100011101
        001000000000011010001111
        000100000000101101000111
        000010000000110110100011
        000001000000111011010001
        000000100000011101101001
        000000010000001110110101
        000000001000000111011011
        000000000100100011101101
        000000000010010001110111
        000000000001111111111110"""

        self.G_bits = numpy.array([ [int(d) for d in line]
                                    for line in g_str.split()])

        self.G_bytes = [sum([j << (11-i) for i,j in enumerate(ii)])
                        for ii in self.G_bits[:,12:].T]

        self.unpacked = unpacked
        self.vlen = vlen
        if unpacked:
            # TODO add assert to GRC
            assert(vlen%3 == 0)

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        count = min(output_items[0].shape[0], input_items[0].shape[0])
        if self.unpacked:
            for i in range(count):
                output_items[0][i, :] = (input_items[0][i,:] * self.G_bits) & 1
        else:
            for i in range(count):
                for j in range(self.vlen//3):
                    # 24 bits (2 symbols) input at a time
                    s1 = (numpy.uint8(input_items[0][i, j]) << 4) | \
                        (numpy.uint8(input_items[0][i, j + 1]) >> 4)
                    s2 = ((numpy.uint8(input_items[0][i, j+1]) << 8) & 0x0f00) | \
                        numpy.uint8(input_items[0][i, j + 2])
                    o1 = 0
                    o2 = 0
                    for k in range(12):
                        o1 |= (parity(self.G_bytes[k] & s1) & 1) << (11 - k)
                        o2 |= (parity(self.G_bytes[k] & s2) & 1) << (11 - k)
                    output = [s1 >> 4,
                              ((s1 & 0x0f) << 4) | (o1 >> 8),
                              o1 & 0xff,
                              s2 >> 4,
                              ((s2 & 0x0f) << 4) | (o2 >> 8),
                              o2 & 0xff]
                    output_items[0][i, (2 * j):(2 * j + 6)] = output

        self.consume_each(count)
        return count
