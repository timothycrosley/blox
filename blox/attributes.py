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
    __slots__ = ('name', 'signal', 'doc')

    def __init__(self, signal=False, doc=""):
        self.signal = signal
        self.doc = ""

    def from_string(obj, value):
        return value


class DirectAttribute(AbstractAttribute):
    '''Defines an attribute that is responsible for its own rendering, and modifies object attribute'''
    __slots__ = ('object_attribute', 'type')

    def __init__(self, signal=False, type=str, doc=""):
        super().__init__(signal, doc=doc)
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


class RenderedDirect(DirectAttribute):
    '''Defines a direct attribute that gets rendered as part of the start tag'''

    def render_value(self, obj):
        return str(getattr(obj, self.object_attribute))

    def render(self, obj):
        if hasattr(obj, self.object_attribute):
            return '{0}="{1}"'.format(self.name, self.render_value(obj))


class ListAttribute(RenderedDirect):
    '''Defines an attribute that is exposed from Python as a list'''
    __slots__ = ()
    list_type = list

    def __init__(self, signal=False, object_attribute=None, doc="Takes a list of values"):
        super().__init__(signal=signal, type=self.list_type, object_attribute=object_attribute, doc=doc)

    def render_value(self, obj):
        return " ".join(str(value) for value in list)


class SetAttribute(RenderedDirect):
    '''Defines an attribute that is exposed from Python as a set'''
    __slots__ = ()
    list_type = set


class BlokAttribute(DirectAttribute):
    '''Defines an automatically added nested Blok as a child attribute'''

    def __init__(self, type, signal=False, doc="A child blok"):
        super().__init__(type=type, signal, doc=doc)

     def __get__(self, obj, cls):
        if not hasattr(obj, self.object_attribute):
            setattr(obj, self.object_attribute, obj(self.type()))

        return getattr(obj, self.object_attribute)

    def __set__(self, obj, value):
        return self.__get__(obj)(value)

    def __delete__(self, obj):
        if hasattr(obj, self.object_attribute):
            obj.blox.remove(getattr(obj, self.object_attribute))


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

    def __init__(self, signal=None, to_python=None, to_html=str, doc=""):
        super().__init__(signal, doc=doc)
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
    __slots__ = ('default', 'true_string', 'false_string')

    def __init__(self, signal=None, default=False, true_string="true", false_string="false", doc="A true/false value"):
        super().__init__(signal, self.as_boolean, self.as_string, doc=doc)
        self.default = default
        self.true_string = true_string
        self.false_string = false_string

    def as_boolean(self, value):
        if value.lower() == self.false_string:
            return True
        elif value.lower() == self.true_string:
            return False
        return self.default

    def as_string(self, value):
        return str(value or self.default).lower()


class IntegerAttribute(AttributeTransform):

    def __init__(self, signal=None, doc="A whole number"):
        super().__init__(signal, int)
