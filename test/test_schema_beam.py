#
# Copyright (c) 2013 Matwey V. Kornilov <matwey.kornilov@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from pybeam.schema import beam
from pybeam.schema.beam.chunks import Atom, AtU8, Attr, CInf, LitT
from construct import Container, StreamError
from construct.core import TerminatedError
import unittest

class BEAMConstructTest(unittest.TestCase):
	def setUp(self):
		pass
	def test_beam1(self):
		c = beam
		self.assertEqual(c.parse(b'FOR1\x00\x00\x00\x04BEAM'), {})
	def test_beam2(self):
		c = beam
		raw = b'FOR1\x00\x00\x02TBEAMAtU8\x00\x00\x002\x00\x00\x00\x07\x01m\x04fact\x06erlang\x01-\x01*\x0bmodule_info\x0fget_module_info\x00\x00Code\x00\x00\x00w\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x99\x00\x00\x00\x08\x00\x00\x00\x03\x01\x10\x99\x10\x02\x12"\x10\x01 \'5\x01\x03\x0e\x10\x10\x99\x10}\x05\x10\x00\x03\x11\x13@\x03\x04@\x13\x03\x99\x10\x04\x10%\x99\x10}\x05\x10\x10\x04\x03\x03\x12\x10\x13\x010+\x15\x03\x01@\x11\x03\x13\x01@\x99\x00\x02\x12b\x00\x01P@\x12\x03\x99\x00N\x10 \x01`\x99\x00\x02\x12b\x10\x01p@\x03\x13@\x12\x03\x99\x00N 0\x03\x00StrT\x00\x00\x00\x00ImpT\x00\x00\x004\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x05\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x07\x00\x00\x00\x01\x00\x00\x00\x03\x00\x00\x00\x07\x00\x00\x00\x02ExpT\x00\x00\x00(\x00\x00\x00\x03\x00\x00\x00\x06\x00\x00\x00\x01\x00\x00\x00\x07\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02LocT\x00\x00\x00\x04\x00\x00\x00\x00Attr\x00\x00\x00(\x83l\x00\x00\x00\x01h\x02d\x00\x03vsnl\x00\x00\x00\x01n\x10\x007\xfc\x18\xc42\x03\xc0\xfa\xe0\x91w.a\xb8\xebqjjCInf\x00\x00\x00l\x83l\x00\x00\x00\x03h\x02d\x00\x07optionsl\x00\x00\x00\x01d\x00\rno_debug_infojh\x02d\x00\x07versionk\x00\x057.1.5h\x02d\x00\x06sourcek\x00!/home/matwey/rpmbuild/BUILD/m.erljDbgi\x00\x00\x00F\x83h\x03d\x00\rdebug_info_v1d\x00\x11erl_abstract_codeh\x02d\x00\x04nonel\x00\x00\x00\x01d\x00\rno_debug_infoj\x00\x00Line\x00\x00\x00\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x01\x00\x00\x00\x00A\x00\x00\x00'
		chunks = c.parse(raw)
		self.assertSetEqual(set(chunks.keys()), set([b'AtU8', b'Code', b'StrT', b'ImpT', b'ExpT', b'LocT', b'Attr', b'CInf', b'Dbgi', b'Line']))
	def test_beam3(self):
		c = beam
		self.assertRaises(TerminatedError, lambda: c.parse(b'FOR1\x00\x00\x00\x0cBEAMAtU8\x00\x00\x002'))
	def test_beam_compressed1(self):
		c = beam
		self.assertEqual(c.parse(b'\x1f\x8b\x08\x08\x9f\xf3\xb0f\x02\xffc.beam\x00s\xf3\x0f2d```qru\xf4\x05\x00\x86\x81S6\x0c\x00\x00\x00'), {})
	def test_chunk_atom(self):
		c = Atom
		self.assertEqual(c.parse(b'\x00\x00\x00\x00'), [])
		self.assertEqual(c.parse(b'\x00\x00\x00\x01\x08burtovoy'),[u"burtovoy"])
		self.assertEqual(c.parse(b'\x00\x00\x00\x02\x08burtovoy\x08yegorsaf'), [u"burtovoy",u"yegorsaf"])
		self.assertEqual(c.parse(c.build([])), [])
		self.assertEqual(c.parse(c.build([u"burtovoy"])), [u"burtovoy"])
		self.assertEqual(c.parse(c.build([u"burtovoy",u"yegorsaf"])), [u"burtovoy",u"yegorsaf"])
		self.assertRaises(StreamError, c.parse, b'\x00\x00\xff\x00')
	def test_chunk_atu8(self):
		c = AtU8
		self.assertEqual(c.parse(b'\x00\x00\x00\x00'), [])
		self.assertEqual(c.parse(b'\x00\x00\x00\x01\x08burtovoy'),[u"burtovoy"])
		self.assertEqual(c.parse(b'\x00\x00\x00\x01\x10\xd0\x91\xd1\x83\xd1\x80\xd1\x82\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xb9'),[u"\u0411\u0443\u0440\u0442\u043e\u0432\u043e\u0439"])
	def test_chunk_attr(self):
		c = Attr
		self.assertEqual(c.parse(b'\x83\x64\x00\x08burtovoy'), u"burtovoy")
		self.assertEqual(c.parse(c.build(u"burtovoy")), u"burtovoy")
		self.assertEqual(c.parse(b'\x83\x6a'), [])
	def test_chunk_cinf(self):
		c = CInf
		self.assertEqual(c.parse(b'\x83\x64\x00\x08burtovoy'), u"burtovoy")
		self.assertEqual(c.parse(c.build(u"burtovoy")), u"burtovoy")
		self.assertEqual(c.parse(b'\x83\x6a'), [])
	def test_chunk_litt1(self):
		c = LitT
		littc = b'x\x9cc```d```j\xce\x02\x00\x01\x87\x00\xf1'
		litt = b'\x00\x00\x00\x0a' + littc + b'\x00\x00'
		self.assertEqual(c.parse(litt).entry[0], [])
	def test_chunk_litt2(self):
		c = LitT
		litt = b'\x00\x00\x03?x\x9cuR\xc1n\xd40\x10M\xb2mi\xab]T@THP4\xea\r\x84\x96\x13|\x01\x0b\x8a\xb4\x80T8\xf4f9\xce,\xf1\xaecG\xb6S\xef\nqZ\x89/\xe0\x02\'>\x80\x8f\xe1\x17\xf8\x0e.\xd8\xde\x84\x94\x03\x97\xf1\xf8yf\xde\x9b\x19\'Ir?I\x92\xcb\xad\xf0\xf6\xa0\xca\\Z\xd0\xd4\x1fG%2U7\xca \xcd\x02ZEtO5(\xa3\x97\xdax\x9cYM\xa5\x11\xd4"aT\x88\x82\xb2\x15\x91\xb4FB5\xb7\x1b\x9a.}\xd5\xd3m\xed\xed\xc9\xdd\xdf\xe3[_\xcf\x9e\x7f~\x9c\x8d\'\xbf\xbe\xff\xfc\xe1\xb1;\xf1ebqm\x9f\xd6T\xafJ\xe5d\x90\x11\xe1$z\xb6\xf3nD,\x05o\x1em\xab\x91\xcb>~Z\x06\xc9#7\x99\t\xbe\xe6z\xfaZ\x95\xad@wH\x08\x97\x0bE\xc8\x8e\xfca\x08\xfe\x7f\xc8 \xa2T\xac\xadQZj\xb9\n"\x1e\xc4\x89d\xee\xa4\xcf\xa5L\xab\xe9L^\xf9\xd6Ca\xe8\xde\x0f\xfb\xbe\xdd\xa4\x0e!\xfd5\xc4\xdc\x0e\xe4#\xc9\xc5`<\xba\xbf]%\xe9\xb1w\xee\xf5%\x16\xadd\x81\xd6\xed\xc7\x12!\xf5[T\xf5%_\x00\x97\xc6"-A-\x802\x86\xc6p\xf9\x01\xfeQ\x0b\x1b\xd5\x82S\xad(A\xf0\x15B\xad4B\xe8P\xd7\xbbwZ\xa8\xd6\x02\x85+*Z\x04\xa5;\xc0V\x08\x1aM+l,.\x01\xd7\x8d\x0e\x04J>\x81\xd6`\x0c8\xe7\xe7P\xa1hP\xf7J\xbc\xaeWq/i\x90\x98\xa1\x0c\xc7\xb3\xddl\xc1Q\x03\xe1\xe3p\x81%8n\xab@\xe4\xd5\x9a)\xbc\xab\x94\x0b\xda\x95\x14\x1b0\rz,\x0c>\x0e!u{v\xd3\xe0r\xd8\xf4\xf1\xb0\x9a\xd9<\xbf\xcc/\xc8\xecE\xfe\xfe\xed\x85\x07\xc6\x11>\xf8{\xbf\x19\xef~\xab/\xf3\xf9\x8c\x90\xeb\xc8<\x7f\xb3CN;\x9a\t-\x8c\xff\xb3\xcc\x12\xa6\xca\xc8w\x14cG\x82\x17!e\xdb\xf54\xfc\xdb\xa0\xeb\xfa4\x87\x14\xa3\xd9\x1f2\xc5\xe6\n\x00\x00\x00'
		self.assertEqual(len(c.parse(litt).entry), 27)