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
from blox.base import Tag, NamedTag

from blox.attributes import AbstractAttribute, Attribute, DirectAttribute, SetAttribute, BooleanAttribute

from blox.builder import Factory


factory = Factory('dom')


@factory.add()
class A(Tag):
    '''Defines a link that when clicked changes the current viewed page'''
    __slots__ = ()
    tag = "a"
    href = Attribute()
    media = Attribute()
    rel = Attribute()
    target = Attribute()
    type = Attribute()


@factory.add()
class Abr(Tag):
    '''Defines  an abbreviation or an acronym'''
    __slots__ = ()
    tag = "abr"


@factory.add()
class Address(Tag):
    '''Defines contact info for the author of a document or article'''
    __slots__ = ()
    tag = "address"


@factory.add()
class Area(Tag):
    '''Defines an area inside of an image map'''
    __slots__ = ()
    tag = 'area'
    alt = Attribute()
    coords = Attribute()
    href = Attribute()
    hreflang = Attribute()
    media = Attribute()
    rel = Attribute()
    shape = Attribute()
    target = Attribute()
    type = Attribute()


@factory.add()
class Article(Tag):
    '''Defines an independent, self-contained content'''
    __slots__ = ()
    tag = "article"


@factory.add()
class Aside(Tag):
    '''Defines content as being aside from the content it is placed in'''
    __slots__ = ()
    tag = "aside"


@factory.add()
class Audio(Tag):
    '''Defines sound, such as music or other audio streams'''
    __slots__ = ()
    tag = "audio"
    autoplay = BooleanAttribute()
    controls = BooleanAttribute()
    loop = BooleanAttribute()
    src = Attribute()

