"""tests/test_base.py.

Tests the base blox to ensure they provide solid functionality for a Python dom representation
Copyright (C) 2015 Timothy Edmund Crosley

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

"""
import pytest

from blox.base import Blok, Invalid, Text, Blox, Tag, NamedTag, TagWithChildren
from io import StringIO


class TestBlok(object):
    testing = Blok
    expected_output = ''

    @classmethod
    def setup_class(cls):
        cls.blok = cls.testing()
        cls.modify(cls)

    def modify(self):
        '''Sub test classes can modify the blok here for testing, before all tests are ran'''
        pass

    def test_output(self):
        output = StringIO()
        self.blok.output(output)
        output.seek(0)
        assert output.read() == self.expected_output

    def test_render(self):
        output = StringIO()
        self.blok.output(output)
        output.seek(0)
        assert self.blok.render() == output.read()

    def test_str(self):
        str(self.blok) == self.blok.render(formatted=True)


class TestInvalid(TestBlok):
    testing = Invalid
    expected_output = '<h2>Invalid</h2>'


class TestText(TestBlok):
    testing = Text
    expected_output = 'test text'

    def modify(self):
        self.blok.value = 'test text'

    def test_change_text(self):
        assert self.blok.value == 'test text'
        self.blok('hi')
        assert self.blok.value == 'hi'


class TestBlox(TestBlok):
    testing = Blox
    expected_output = 'hi bacon'

    def modify(self):
        self.hi = Text('hi')
        self.bacon = Text(' bacon')
        self.blok += self.hi
        self.blok += self.bacon

    def test_list_like(self):
        assert self.hi in self.blok
        assert self.bacon in self.blok

        for_testing = Text('for testing')
        old_size = len(self.blok)
        self.blok += for_testing
        assert self.blok[old_size] == for_testing
        assert len(self.blok) == old_size + 1
        assert for_testing in self.blok
        self.blok -= for_testing
        assert not for_testing in self.blok

        self.blok += for_testing
        del self.blok[old_size]
        assert not for_testing in self.blok

        for blok in self.blok:
            assert isinstance(blok, Blok)


class TestTag(TestBlok):
    expected_output = '<testing />'
    class testing(Tag):
        tag = 'testing'


class TestTagWithChildren(TestBlox):
    expected_output = '<testing>hi bacon</testing>'
    class testing(TagWithChildren):
        tag = 'testing'
