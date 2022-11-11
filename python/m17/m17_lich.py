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

import struct


_BASE40_LUT = ['\0',
               'A', 'B', 'C', 'D', 'E', 'F', 'G',
               'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T',
               'U', 'V', 'W', 'X', 'Y', 'Z',
               '0','1','2','3','4','5','6','7','8','9',
               '-','/','.']

def _encode_base40(in_str):
    """
    Encode string(ie callsign) in base40
    """
    assert(len(in_str) <= 9)
    enc = 0
    for c in in_str[::-1]:
        assert((enc << 3) + (enc << 5) + _BASE40_LUT.index(c) == enc * 40 + _BASE40_LUT.index(c))
        enc = enc * 40 + _BASE40_LUT.index(c)
    return bytearray(struct.pack('>q', enc)[2:])

def _decode_base40(in_val):
    """
    Decode base40 int or packed str into a string
    """
    if isinstance(in_val, str) or isinstance(in_val, bytearray):
        assert(len(in_val) == 6)
        in_val = struct.unpack('>q', bytearray(b'\x00\x00') + in_val)[0]
    ret = ''
    while (in_val > 0):
        ret += _BASE40_LUT[int(in_val % 40)]
        in_val = int(in_val / 40)
    return ret

def crc16(data_in, poly, normal_form=True, init_val=0x0000):
    """
    Calculate CRC using normal or Koopman(aka reversed recipricol) polynomial representation.
    Assumes no reflection or output XOR.

    * https://en.wikipedia.org/wiki/Cyclic_redundancy_check#Specification
    * https://users.ece.cmu.edu/~koopman/crc/#notation
    """
    reg = init_val
    def calc_byte(reg, in_byte):
        for i in range(7, -1, -1):
            bit = (in_byte >> i) & 1
            out = (reg >> 15) & 1
            inp = bit ^ out
            if normal_form:
                reg = ((reg << 1) ^ (poly * inp)) & 0xffff
            else:
                reg = (((reg ^ (poly * inp)) << 1) | inp) & 0xffff
        return reg

    for byte in data_in:
        reg = calc_byte(reg, byte)

    return reg & 0xFFFF


def crc16_m17(data_in):
    """
    Calculate M17 CRC for a stream of data
    """
    return crc16(data_in, 0x5935, True, 0xFFFF)

class lich(object):
    """
    Encapsulate M17 LICH structure
    """

    def __init__(self, dst, src, stream_type, nonce=None):
        self.dst = dst
        self.src = src
        self.stream_type = stream_type
        self.nonce = nonce

    def _encode(self):
        lich_data = bytearray(
            _encode_base40(self.dst) +
            _encode_base40(self.src) +
            struct.pack('>H', self.stream_type) +
            self.nonce
        )
        crc = crc16_m17(lich_data)
        return lich_data + struct.pack('>H', crc)

    def asList(self):
        """
        return representation of LICH as list of bytes
        """
        return list(self._encode())

    def asByteArray(self):
        """
        return representation of LICH as python bytearray
        """
        return self._encode()

    def __str__(self):
        return 'dst: {}, src: {}, stream_type: {}, nonce: {}'.format(
            self.dst,
            self.src,
            self.stream_type,
            list(self.nonce))

    @staticmethod
    def fromByteArray(inp, check_crc=True):
        """
        Parse LICH from bytearray. Optionally(default=yes) check CRC.
        """
        assert(len(inp) == 30) # 240 bits is 30 bytes
        if check_crc:
            assert(crc16_m17(inp) == 0)
        dst = _decode_base40(inp[0:6])
        src = _decode_base40(inp[6:12])
        stream_type = struct.unpack('>H', inp[12:14])[0]
        nonce_bytes = inp[14:28]
        return lich(dst, src, stream_type, nonce_bytes)

if __name__ == '__main__':
    ts = "KM6VMZ/M"
    enc1 = _encode_base40(ts)
    print('encoded', list(enc1))
    dec1 = _decode_base40(enc1)
    print('decoded', dec1)
    print(ts, dec1, ts == dec1)
    assert(ts == dec1)

    l1 = lich('SP5WWP', 'KM6VMZ', 0x03, bytearray(14))
    print(l1)
    print(l1.asList())

    barray = l1.asByteArray()
    print('l2', barray)
    l2 = lich.fromByteArray(barray)
    print(l2)

    assert(l2.dst == l1.dst)
    assert(l2.src == l1.src)
    assert(l2.nonce == l1.nonce)
    assert(l2.stream_type == l1.stream_type)
