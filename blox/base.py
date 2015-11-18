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
from itertools import chain

from connectable import Connectable
from blox.attributes import AbstractAttribute, Attribute, RenderedDirect, SetAttribute, BooleanAttribute, IntegerAttribute, DirectAttribute

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
    def value(self, value):
        if value != self._value:
            self.emit('value_changed', value)
            self._value = value

    def output(self, to=None, *args, **kwargs):
        '''Outputs the set text'''
        to.write(self._value)

    def __call__(self, text):
        '''Updates the text value'''
        self.value = text
        return self


class Blox(Blok):
    '''A Block that can contain child blocks'''
    __slots__ = ('_blox', )

    def __init__(self, *blox):
        super().__init__()
        for blok in blox:
            self(blok)

    @property
    def blox(self):
        '''Lazily creates and returns the list of child blox'''
        if not hasattr(self, '_blox'):
            self._blox = []
        return self._blox

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
        self.blox.__setitem__(index, value)

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

    def __new__(metaclass, name, parents, class_dict, *kargs, **kwargs):
        '''Updates a tag class to automatically register all signals'''
        attributes = {name: attribute for name, attribute in class_dict.items() if isinstance(attribute,
                                                                                              AbstractAttribute)}
        if attributes:
            if hasattr(parents[0], 'attribute_descriptors'):
                full_attributes = parents[0].attribute_descriptors.copy()
                full_attributes.update(attributes)
                attributes = full_attributes

            render_attributes = []
            direct_attributes = []
            for attribute_name, attribute in attributes.items():
                if not hasattr(attribute, 'name'):
                    attribute.name = attribute_name
                if isinstance(attribute, DirectAttribute):
                    direct_attributes.append(attribute)
                    if hasattr(attribute, 'render'):
                        render_attributes.append(attribute)
                    if not hasattr(attribute, 'object_attribute'):
                        attribute.object_attribute = '_{0}'.format(attribute_name)
            if direct_attributes and not name == 'AbstractTag' and '__slots__' in class_dict:
                class_dict['__slots__'] += tuple(attribute.object_attribute for attribute in direct_attributes)

            if render_attributes:
                if hasattr(parents[0], 'render_attributes'):
                    render_attributes = list(parents[0].render_attributes) + render_attributes
                class_dict['render_attributes'] = set(render_attributes)

            class_dict['attribute_descriptors'] = attributes
            attribute_signals = (attribute.signal for attribute in attributes.values() if getattr(attribute, 'signal'))
            if attribute_signals:
                class_dict['signals'] = class_dict.get('signals', ()) + tuple(attribute_signals)

        return super(TagAttributes, metaclass).__new__(metaclass, name, parents, class_dict, *kargs, **kwargs)


class AbstractTag(Blok, metaclass=TagAttributes):
    '''A Blok that renders a single tag'''
    __slots__ = ()
    tag_self_closes = True
    tag = ""
    id = RenderedDirect()
    classes = SetAttribute()
    accesskey = Attribute()
    contenteditable = BooleanAttribute(default=True)
    contextmenu = Attribute()
    dir = Attribute()
    draggable = BooleanAttribute()
    dropzone = Attribute()
    hidden = BooleanAttribute()
    lang = Attribute()
    spellcheck = BooleanAttribute()
    style = Attribute()
    tabindex = IntegerAttribute()
    translate = BooleanAttribute(true_string="yes", false_string="no")

    def __init__(self, **attributes):
        super().__init__()
        for name, value in attributes.items():
            setattr(self, name, value)

    @property
    def attributes(self):
        '''Lazily creates and returns a tags attributes'''
        if not hasattr(self, '_attributes'):
            self._attributes = {}

        return self._attributes


    @property
    def start_tag(self):
        '''Returns the elements HTML start tag'''
        direct_attributes = (attribute.render(self) for attribute in self.render_attributes)
        attributes = ()
        if hasattr(self, '_attributes'):
            attributes = ('{0}="{1}"'.format(key, value) for key, value in self.attributes.items() if value)

        rendered_attributes = " ".join(filter(bool, chain(direct_attributes, attributes)))
        return '<{0}{1}{2}{3}>'.format(self.tag, ' ' if rendered_attributes else '',
                                       rendered_attributes, '/' if self.tag_self_closes else "")

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

    def __contains__(self, attribute):
        return blok in self.attribute

    def __getitem__(self, attribute):
        return self.attributes[attribute]

    def __setitem__(self, attribute, value):
        self.attributes[attribute] = value

    def __delitem__(self, attribute):
        del self.attributes[attribute]


class Tag(AbstractTag):
    '''A Blok that renders a single tag'''
    __slots__ = ('_attributes', '_id', '_classes')


class NamedTag(Tag):
    '''A Tag with an attached name'''
    __slots__ = ('_name', )
    name = RenderedDirect()


class TagWithChildren(Blox, AbstractTag):
    '''Defines a tag that can contain children'''
    __slots__ = ('_attributes', '_id', '_classes')
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

    def __contains__(self, attribute_or_blok):
        if type(attribute_or_blok) == int:
            return Blox.__contains__(self, attribute_or_blok)
        else:
            return AbstractTag.__contains__(self, attribute_or_blok)

    def __getitem__(self, attribute_or_blok):
        if type(attribute_or_blok) == int:
            return Blox.__getitem__(self, attribute_or_blok)
        else:
            return AbstractTag.__getitem__(self, attribute_or_blok)

    def __setitem__(self, attribute_or_blok, value):
        if type(attribute_or_blok) == int:
            return Blox.__setitem__(self, attribute_or_blok, value)
        else:
            return AbstractTag.__setitem__(self, attribute_or_blok, value)

    def __delitem__(self, attribute_or_blok):
        if type(attribute_or_blok) == int:
            return Blox.__delitem__(self, attribute_or_blok)
        else:
            return AbstractTag.__delitem__(self, attribute_or_blok)
