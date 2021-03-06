"""tests/test_blox.py.

Tests the Python3 implementation of blox

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
from blox.document import Document
from blox.text import Text

from .test_base import TestContainer


class TestDocument(TestContainer):
    '''Test to ensure blox works as expected'''
    testing = Document
    expected_output = '<!DOCTYPE html><html><body>hi bacon</body></html>'

    def test_autogeneration(self):
        document = Document()
        assert document.render() == '<!DOCTYPE html><html></html>'

        document.head
        assert document.render() == '<!DOCTYPE html><html><head></head></html>'
        document.body
        assert document.render() == '<!DOCTYPE html><html><head></head><body></body></html>'

        document += Text('Hi')
        assert document.render() == '<!DOCTYPE html><html><head></head><body>Hi</body></html>'
