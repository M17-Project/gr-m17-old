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

class add_sync(gr.basic_block):
    """
    Adds a 2 byte M17 sync to each packed packet (46 bytes/368 bits)
    """

    # section 3.2 of M17 spec
    SYNC = [0x32, 0x43]
    IN_VLEN = 46
    OUT_VLEN = 48

    def __init__(self):
        gr.basic_block.__init__(self,
            name="add_sync",
            in_sig=[(numpy.byte, self.IN_VLEN), ],
            out_sig=[(numpy.byte, self.OUT_VLEN), ])

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        nin = min(input_items[0].shape[0], output_items[0].shape[0])
        nout = nin
        gr.log.debug("sync {} input {} output {}".format(len(self.SYNC),
                                                         input_items[0].shape,
                                                         output_items[0].shape))

        output_items[0][:nout, :] = numpy.concatenate(
            (numpy.repeat([self.SYNC], nin, axis=0), input_items[0][:nin,:], ),
            axis=1)

        self.consume_each(nin)
        return nout
