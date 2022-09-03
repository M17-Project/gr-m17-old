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
from m17.m17_lich import crc16_m17

MAC_DATA_IN_NBITS = 128
MAC_FN_NBITS = 16
MAC_TOTAL_NBITS = MAC_FN_NBITS + MAC_DATA_IN_NBITS

NONCE_NBYTES = 112 // 8

class m17_framer(gr.basic_block):
    """
    framing for M17 specification
    """

    def __init__(self, dst, src, stream_type, nonce=None):
        gr.basic_block.__init__(self,
            name="m17_framer",
            in_sig=[numpy.byte],
            out_sig=[numpy.byte])
        # TODO: not sure if this helps in any way
        self.set_relative_rate(MAC_TOTAL_NBITS, MAC_DATA_IN_NBITS)

        self.buffer = numpy.array([])
        self.fn = 0

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required = MAC_DATA_IN_NBITS // 8 * (noutput_items // (MAC_TOTAL_NBITS // 8))
        #gr.log.debug("forecast {} {}".format(noutput_items, ninput_items_required))

    def general_work(self, input_items, output_items):

        self.buffer = numpy.concatenate((self.buffer, input_items[0],) )
        self.consume_each(len(input_items[0]))

        nout = 0
        data_in_nbytes = MAC_DATA_IN_NBITS // 8
        while len(self.buffer) > data_in_nbytes:
            self.fn += 1

            # fn
            output_items[0][nout:(nout + 2)] = [self.fn >> 8, self.fn & 0xff]
            nout += 2

            # data w/ CRC
            # TODO: clean this up
            crc = crc16_m17(bytearray(self.buffer[:data_in_nbytes]))
            output_items[0][nout:(nout + data_in_nbytes + 2)] = numpy.concatenate( (self.buffer[:data_in_nbytes], [crc >> 8, crc & 0xff]) )
            self.buffer = self.buffer[data_in_nbytes:]
            nout += data_in_nbytes + 2

        if nout > 0 or len(input_items[0]) > 0:
            gr.log.debug("rx: {} gen: {}".format(len(input_items[0]), nout))

        return nout
