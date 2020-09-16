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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from golay_enc import golay_enc
import numpy

class qa_golay_enc(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_t(self):
        src_data = numpy.array([0x12, 0xf1, 0x2f], dtype=numpy.uint8)
        expected_result = [0x12, 0xfe, 0x91, 0x12, 0xfe, 0x91]

        src = blocks.vector_source_b(src_data, False, 3)
        uut = golay_enc(False, 3)
        dst = blocks.vector_sink_b(6)
        self.tb.connect(src, uut)
        self.tb.connect(uut, dst)

        self.tb.run()
        result_data = dst.data()
        self.assertFloatTuplesAlmostEqual(expected_result, result_data, 6)


if __name__ == '__main__':
    gr_unittest.run(qa_golay_enc)
