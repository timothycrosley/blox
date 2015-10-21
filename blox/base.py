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
from connectable import Connectable

from io import StringIO


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


class AbstractTag(Blok):
    '''A Blok that renders a single tag'''
    __slots__ = ()
    tag = ""
    tag_self_closes = True

    def __init__(self, **properties):
        super().__init__()
        self.properties = {}
        self.properties.update(properties)

    @property
    def start_tag(self):
        '''Returns the elements HTML start tag'''
        if not self.tag:
            return ''

        properties = " ".join(('{0}="{1}"'.format(key, value) for key, value in self.properties.items() if value))
        return "<{0}{1}{2}{3}>".format(self.tag, " " if properties else "", properties,
                                         "/" if self.tag_self_closes else "")

    @property
    def end_tag(self):
        '''Returns the elements HTML end tag'''
        if self.tag_self_closes:
            return ''

        return "</{0}>".format(self.tag)

    def output(self, to=None, *args, **kwargs):
        '''Outputs to a stream (like a file or request)'''
        to.write(self.start_tag)
        if not self.tag_self_closes:
            to.write(self.end_tag)

class Tag(AbstractTag):
    __slots__ = ('properties', )

class TagWithChildren(Blox, AbstractTag):
    '''Defines a tag that can contain children'''
    __slots__ = ('properties', )
    tag = ""
    tag_self_closes = False

    def __init__(self, *blox, **properties):
        super().__init__()
        for blok in blox:
            self(blok)
        self.properties.update(properties)

    def output(self, to=None, *args, **kwargs):
        '''Outputs to a stream (like a file or request)'''
        to.write(self.start_tag)
        if not self.tag_self_closes:
            for blok in self.blox:
                blok.output(to=to, *args, **kwargs)
            to.write(self.end_tag)
