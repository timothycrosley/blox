'''blox/dom.py

Defines the basic HTML DOM elements as blox

Copyright (C) 2015  Timothy Edmund Crosley

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

'''
from blox.attributes import (AbstractAttribute, Attribute, BlokAttribute, BooleanAttribute,
                             IntegerAttribute, NestedAttribute, RenderedDirect, SetAttribute)
from blox.base import Blok, Blox, NamedTag, Tag, TagWithChildren, Text
from blox.builder import Factory
from blox.dom import HTML, DocType

factory = Factory("Document")


@factory.add('document', 'html')
class Document(Blox):
    '''Defines the basic concept of full HTML document/page'''
    __slots__ = ()
    doc_type = BlokAttribute(DocType, init=True, position=0)
    html = BlokAttribute(HTML, position=1, init=True)
    head = NestedAttribute('html.head')
    title = NestedAttribute('html.head.title.text')
    body = NestedAttribute('html.body')

    @property
    def blox_container(self):
        return self.html.body

    def __setitem__(self, index, value):
        return self.html.__setitem__(index, value)

    def __getitem__(self, index, value):
        return self.html.__getitem__(index, value)