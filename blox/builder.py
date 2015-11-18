'''blox/builder.py

The Node Building Factory provides a mechanism for building any element the factory has knowledge of
simply by defining their names (as a string) and their main attributes.

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
from blox.base import Invalid


class Factory(object):
    '''Defines a Blok factory that can be used to build new Blox based on only the name and attributes of the Blok'''
    __slots__ = ('name', 'default', 'products')

    def __init__(self, name="", default=Invalid):
        self.products = {}
        self.name = name
        self.default = default

    def add(self, name=None):
        '''Returns back a class decorator that enables registering Blox to this factory'''
        def decorator(blok):
            self.products[(name or blok.__name__).lower()] = blok
            return blok
        return decorator

    def __call__(self, blok_name, **properties):
        '''Builds and returns a Blok object'''
        return self.products.get(blok_name.lower(), None)(**properties)


class Composite(Factory):
    '''Enables combining multiple Factory into a single one that contains all Elements of both'''

    def __init__(self, factories):
        super().__init__()
        for factory in factories:
            self.products.update(factory.products)
            if factory.name:
                for blok_name, product in factory.products.items():
                    self.products[factory.name.lower() + "-" + blok_name] = product
