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


class Blok(Connectable):
    '''Defines the base blox blok object which can render itself and be instanciated'''
    __slots__ = ()

    def __init__(self, *blox, **properties):
        for blok in blox:
            self(blok)

    def __call__(self, blok):
        '''Adding nested bloks to the base blok is not supported'''
        raise NotImplemented('This Blok does not support having children added to it')

    def render(self, formatted=False, *args, **kwargs):
        '''Renders this blok'''
        return ''


class Node(Blok):
    '''Defines the base HTML node blok based on a blok'''
    __slots__ = ('blox', )

    def __init__(self, *blox, **properties):
        self.blox = []
        self.attributes = {}
        super().__init__(*blox, **properties)

    def __call__(self, blok):
        '''Adds a nested blok to this blok'''
        self.blox.append(blok)

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


