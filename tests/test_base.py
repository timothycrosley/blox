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

    def __init__(self):
        self.blok = self.testing()

    def test_output(self):
        self.blok.output(StringIO())

    def test_render(self):
        output = StringIO()
        self.blok.output(output)
        assert self.blok.render() == str(output)

    def test_str(self):
        str(self.blok) == self.blok.render(formatted=True)


class TestInvalid(TestBlok):
    testing = Invalid

    def test_output(self):
        output = StringIO()
        self.blok.output(output)
        assert str(output) == '<h2>Invalid</h2>'


class TestText(TestBlok):
    testing = Text

    def test_set_value(self):
        self.blok.value = 'test text'
        assert self.blok.value == 'test text'


class TestBlox(TestBlok):
    testing = Blox

    def test_with_children(self):
        self.blok += Text('hi')
        self.blok += Text(' bacon')
        assert self.blok.render() == 'hi bacon'


class TestTag(TestBlok):
    class testing(Tag):
        tag = 'testing'

    def test_tag_render(self):
        assert self.blok.render() == "<testing />"


class TestTagWithChildren(TestBlox):
    class testing(TagWithChildren):
        tag = 'testing'

    def test_with_children(self):
        self.blok += Text('hi')
        self.blok += Text(' bacon')
        assert self.blok.render() == '<testing>hi bacon</testing>'
