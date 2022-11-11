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
from add_fn import add_fn
import numpy

class qa_add_fn(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_add_fn(self):
        src_data = numpy.arange(16)
        expected_result = numpy.concatenate( ([0, 0], src_data) )

        src = blocks.vector_source_b(src_data, False, 16)
        dut = add_fn(0)
        dst = blocks.vector_sink_b(18)
        self.tb.connect(src, dut)
        self.tb.connect(dut, dst)

        self.tb.run()
        result_data = dst.data()
        self.assertFloatTuplesAlmostEqual(expected_result, result_data, 18)


if __name__ == '__main__':
    gr_unittest.run(qa_add_fn)
