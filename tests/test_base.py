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
from io import StringIO

import pytest

from blox.base import Blok, Blox, Invalid, NamedTag, Tag, TagWithChildren, Container
from blox.text import Text, UnsafeText


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

    def test_special_characters(self):
        self.blok('<hi')
        assert self.blok.render() == '<hi'


class TestUnsafeText(TestText):
    testing = UnsafeText

    def test_special_characters(self):
        self.blok('<hi')
        assert self.blok.render() == '&lt;hi'


class TestContainer(TestBlok):
    testing = Container
    expected_output = 'hi bacon'

    @classmethod
    def setup_class(cls):
        cls.hi = Text('hi')
        cls.blok = cls.testing(cls.hi)
        cls.modify(cls)

    def modify(self):
        self.bacon = Text(' bacon')
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

    def test_insert(self):
        additional_text = Text('more_text')
        self.blok(additional_text, 0)
        assert additional_text in self.blok

    def test_set_item(self):
        additional_text = Text('more_text')
        self.blok[0] = additional_text
        assert additional_text in self.blok
        assert self.blok[0] == additional_text


class TestTag(TestBlok):
    expected_output = '<testing />'
    class testing(Tag):
        tag = 'testing'


class TestTagWithChildren(TestContainer):
    expected_output = '<testing>hi bacon</testing>'
    class testing(TagWithChildren):
        tag = 'testing'
