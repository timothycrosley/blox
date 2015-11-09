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

class AbstractAttribute(object):
    '''Defines the abstract Blok attribute concept'''
    __slots__ = ('name', 'signal')

    def __init__(self, signal=False):
        self.signal = signal

    def from_string(obj, value):
        return value


class DirectAttribute(AbstractAttribute):
    '''Defines an attribute that is responsible for its own rendering, and modifies object attribute'''
    __slots__ = ('object_attribute', 'type')

    def __init__(self, signal=False, type=str):
        super().__init__(signal)
        self.type = type

    def __get__(self, obj, cls):
        if not hasattr(obj, self.object_attribute):
            setattr(obj, self.object_attribute, self.type())

        return getattr(obj, self.object_attribute)

    def from_string(obj, value):
        return self.type(value)

    def __set__(self, obj, value):
        return setattr(obj, self.object_attribute, value)

    def __delete__(self, obj):
        delattr(obj, self.object_attribute)

    def render_value(self, obj):
        return str(getattr(obj, self.object_attribute))

    def render(self, obj):
        if hasattr(obj, self.object_attribute):
            return '{0}="{1}"'.format(self.name, self.render_value(obj))


class ListAttribute(DirectAttribute):
    '''Defines an attribute that is exposed from Python as a list'''
    __slots__ = ()
    list_type = list

    def __init__(self, signal=False, object_attribute=None):
        super().__init__(signal=signal, type=self.list_type, object_attribute=object_attribute)

    def render_value(self, obj):
        return " ".join(str(value) for value in list)


class SetAttribute(ListAttribute):
    '''Defines an attribute that is exposed from Python as a set'''
    __slots__ = ()
    list_type = set


class Attribute(AbstractAttribute):
    '''Defines a basic Blok attribute that is rendered by the framework and stores its data in a .attributes dict'''
    __slots__ = ()

    def __get__(self, obj, cls):
        return obj.attributes[self.name]

    def __set__(self, obj, value):
        if self.signal and not self.name in attributes or obj.attributes[self.name] != value:
            obj.emit(self.signal, value)
        obj.attributes[self.name] = value

    def __delete__(self, obj):
        obj.attributes.pop(self.name, None)


class AttributeTransform(object):
    '''Defines an attribute that transforms values for Python and HTML use'''
    __slots__ = ('to_python', 'to_html')

    def __init__(self, signal=None, to_python=None, to_html=str):
        super().__init__(signal)
        self.to_python = to_python
        self.to_html = to_html

    def __get__(self, obj, cls):
        value = super().__get__(obj, cls)
        return self.to_python(value) if self.to_python else value

    def __set__(self, obj, value):
        super().__set__(obj, self.to_html(value) if self.to_html else value)

    def from_string(self, value):
        return self.to_python(value)


class BooleanAttribute(AttributeTransform):
    '''Defines a boolean attribute'''
    __slots__ = ('default', )

    def __init__(self, signal=None, default=False):
        super().__init__(signal, self.as_boolean, self.as_string)
        self.default = default

    def as_boolean(self, value):
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        return self.default

    def as_string(self, value):
        return str(value or self.default).lower()


class IntegerAttribute(AttributeTransform):

    def __init__(self, signal=None):
        super().__init__(signal, int)
