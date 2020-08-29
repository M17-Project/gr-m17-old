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
from m17.m17_lich import lich

class m17_lich_gen(gr.sync_block):
    """
    Generate LICH full block
    """
    def __init__(self, dst, src, stream_type, nonce=None):
        gr.sync_block.__init__(self,
            name="m17_lich_gen",
            in_sig=None,
            out_sig=[numpy.byte, ])

        if nonce is None:
            nonce = bytearray(NONCE_NBYTES)
        self.lich = lich(dst, src, stream_type, nonce)
        self.lich_array = numpy.array(self.lich.asList(), dtype=numpy.int8)

        gr.log.debug('LICH {}'.format(self.lich))
        gr.log.debug('LICH bytes {}'.format(self.lich_array))


    def work(self, input_items, output_items):
        output_items[0][:len(self.lich_array)] = self.lich_array
        return len(self.lich_array)

