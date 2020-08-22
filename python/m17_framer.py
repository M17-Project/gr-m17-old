#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
#from . import m17_lich

class m17_framer(gr.basic_block):
    """
    framing for M17 specification
    """
    def __init__(self, dst,src,stream_type,nonce=None):
        gr.basic_block.__init__(self,
            name="m17_framer",
            in_sig=[numpy.byte],
            out_sig=[numpy.byte])

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        # TODO: Need to figure out to trigger preamble and initial LICH
        output_items[0][:] = input_items[0]
        consume(0, len(input_items[0]))
        #self.consume_each(len(input_items[0]))
        return len(output_items[0])
