'''blox/base.py

The base for all blox

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
import re

from connectable import Connectable
from blox.attributes import Attribute

from io import StringIO

UNDERSCORE = (re.compile('(.)([A-Z][a-z]+)'), re.compile('([a-z0-9])([A-Z])'))


class Blok(Connectable):
    '''Defines the base blox blok object which can render itself and be instanciated'''
    __slots__ = ()

    def output(self, to=None, *args, **kwargs):
        '''Outputs to a stream (like a file or request)'''
        to.write('')

    def render(self, *args, **kwargs):
        '''Renders as a str'''
        render_to = StringIO()
        self.output(render_to, *args, **kwargs)
        return render_to.getvalue()


class Invalid(Blok):
    '''Defines how the lack of a vaild Blok should be rendered'''
    __slots__ = ()

    def output(self, to=None, *args, **kwargs):
        to.write('<h2>Invalid</h2>')


class Text(Blok):
    '''Defines the most basic text block'''
    __slots__ = ('_value', )
    signals = ('value_changed', )

    def __init__(self, value=''):
        super().__init__()
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def setValue(self, value):
        if value != self._value:
            self.emit('value_changed', value)
            self._value = value

    def output(self, to=None, *args, **kwargs):
        '''Outputs the set text'''
        to.write(self._value)


class Blox(Blok):
    '''A Block that can contain child blocks'''
    __slots__ = ('blox', )

    def __init__(self, *blox):
        super().__init__()
        self.blox = []
        for blok in blox:
            self(blok)

    def __call__(self, blok):
        '''Adds a nested blok to this blok'''
        self.blox.append(blok)
        return blok

    def __iter__(self):
        return self.blox.__iter__()

    def __contains__(self, blok):
        return blok in self.bloks

    def __getitem__(self, index):
        return self.blox[index]

    def __setitem__(self, index, value):
        if type(index) == int:
            self.blox.__setitem__(index, value)
        else:
            self.attributes[index] = value

    def __delitem__(self, index):
        return self.blox.__delitem__(index)

    def __str__(self):
        return self.render(formatted=True)

    def __isub__(self, blok):
        self.blox.remove(blok)
        return self

    def __iadd__(self, blok):
        self(blok)
        return self

    def __len__(self):
        return len(self.blox)

    def output(self, to=None, *args, **kwargs):
        '''Outputs to a stream (like a file or request)'''
        for blok in self.blox:
            blok.output(to=to, *args, **kwargs)


class TagAttributes(type):
    '''A meta class to automatically register signals for tag attributes'''

    def __new__(cls, name, parents, dct):
        cls.signals += tuple(attribute.signal for attribute in dir(cls) if
                             isinstance(attribute, Attribute) and attribute.signal)
        if not cls.tag:
            cls._tag =  UNDERSCORE[1].sub(r'\1_\2', UNDERSCORE[0].sub(r'\1_\2', cls.__name__)).lower()
        else:
            cls._tag = cls.tag

        return super(TagAttributes, cls).__new__(cls, name, parents, dct)


class AbstractTag(Blok, metaclass=TagAttributes):
    '''A Blok that renders a single tag'''
    __slots__ = ()
    tag = None
    tag_self_closes = True

    def __init__(self, **attributes):
        super().__init__()
        self.attributes = {}
        self.attributes.update(attributes)

    @property
    def start_tag(self):
        '''Returns the elements HTML start tag'''
        attributes = " ".join(('{0}="{1}"'.format(key, value) for key, value in self.attributes.items() if value))
        return "<{0}{1}{2}{3}>".format(self._tag, " " if attributes else "", attributes,
                                         "/" if self.tag_self_closes else "")

    @property
    def end_tag(self):
        '''Returns the elements HTML end tag'''
        if self.tag_self_closes:
            return ''

        return "</{0}>".format(self._tag)

    def output(self, to=None, *args, **kwargs):
        '''Outputs to a stream (like a file or request)'''
        to.write(self.start_tag)
        if not self.tag_self_closes:
            to.write(self.end_tag)


class Tag(AbstractTag):
    '''A Blok that renders a single tag'''
    __slots__ = ('attributes', )


class TagWithChildren(Blox, AbstractTag):
    '''Defines a tag that can contain children'''
    __slots__ = ('attributes', )
    tag = ""
    tag_self_closes = False

    def __init__(self, *blox, **attributes):
        super().__init__()
        for blok in blox:
            self(blok)
        self.attributes.update(attributes)

    def output(self, to=None, *args, **kwargs):
        '''Outputs to a stream (like a file or request)'''
        to.write(self.start_tag)
        if not self.tag_self_closes:
            for blok in self.blox:
                blok.output(to=to, *args, **kwargs)
            to.write(self.end_tag)
