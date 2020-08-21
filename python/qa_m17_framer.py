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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from m17_framer import m17_framer
import m17_lich

class qa_m17_framer (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_lich(self):
        ts = 'KM6VMZ/M'
        enc1 = m17_lich._encode_base40(ts)
        dec1 = m17_lich._decode_base40(enc1)
        assert(ts == dec1)

    def test_002_lich(self):
        l1 = m17_lich.lich('SP5WWP', 'KM6VMZ', 0x03, bytearray(14))
        barray = l1.asByteArray()
        l2 = m17_lich.lich.fromByteArray(barray)

        assert(l2.dst == l1.dst)
        assert(l2.src == l1.src)
        assert(l2.nonce == l1.nonce)
        assert(l2.stream_type == l1.stream_type)

    def test_001_t (self):
        # set up fg
        #self.tb.run()
        # check data
        assert(True)
    
if __name__ == '__main__':
    gr_unittest.run(qa_m17_framer, "qa_m17_framer.xml")
