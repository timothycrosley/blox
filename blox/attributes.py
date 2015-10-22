'''blox/attributes.py

Defines how Blox handles the setting of and definition of attributes

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

class Attribute(object):
    '''Defines the most basic Blok attribute object'''
    __slots__ = ('name', )

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, cls):
        return obj.attributes[self.name]

    def __set__(self, obj, value):
        obj.attributes[self.name] = value

     def __delete__(self, obj):
         obj.attributes.pop(self.name, None)


class AttributeTransform(object):
    '''Defines the base Blok attribute object'''
    __slots__ = ('to_python', 'to_html')

    def __init__(self, name, to_python=None, to_html=star):
        super().__init__(name)
        self.to_python = to_python
        self.to_html = to_html

    def __get__(self, obj, cls):
        value = super().__get__(obj, cls)
        return self.to_python(value) if self.to_python else value

    def __set__(self, obj, value):
        super().__set__(obj, self.to_html(value) if self.to_html else value)
