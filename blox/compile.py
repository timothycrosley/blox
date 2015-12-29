'''blox/compile.py

Creates an optimized programattically generated template from an html file

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
import json
from blox.base import Blox, Text, UnsafeText
from blox.all import factory
from xml.dom import minidom
from lxml.etree import HTMLParser, parse, fromstring

parser = HTMLParser()
SCRIPT_TEMPLATE = """# WARNING: DON'T EDIT AUTO-GENERATED

from blox.base import Blox, Text, UnsafeText


class Template(Blox):
{indent}__slots__ = tuple({accessors})


def build(factory):
{indent}template = Template()
{indent}{build_steps}
{indent}return template
"""


def from_file(file_object):
    return parse(file_object, parser=parser).getroot()


def from_filename(file_name):
    return from_file(open(file_name))


def from_string(html):
    return fromstring(html)


def to_python(dom, factory=factory, indent='    '):
    current = [0]
    def increment(element_name=''):
        current[0] += 1
        return ('{0}{1}'.format(element_name, current[0]), factory.get(element_name))

    lines = []
    accessors = []
    def compile_node(node, parent='template'):
        blok_name, blok = increment(node.tag)
        lines.append("{0} = {1}(factory('{2}'))".format(blok_name, parent, node.tag))

        text = (node.text or "").strip().replace('"', '\\"')
        if text:
            if hasattr(blok, 'text'):
                lines.append('{0}.text = "{1}"'.format(blok_name, text))
            else:
                lines.append('{0}(Text("{1}"))'.format(blok_name, text))

        for attribute_name, attribute_value in node.items():
            lines.append('{0}["{1}"] = "{2}"'.format(blok_name, attribute_name.replace('"', '\\"'),
                                                     attribute_value.replace('"', '\\"')))
            if attribute_name == 'accessor':
                accessors.append(attribute_value)
                lines.apppend('{0}.{1} = {2}'.format(parent, attribute_value, blok_name))

        for child_node in node:
            if child_node.tag in getattr(blok, 'blok_attributes', {}):
                attached_child = "{0}.{1}".format(blok_name, blok.blok_attributes[child_node.tag].name)
                for nested_child_node in child_node:
                    compile_node(nested_child_node, parent=attached_child)
            else:
                compile_node(child_node, parent=blok_name)

            tail = (child_node.tail or "").strip().replace('"', '\\"')
            if tail:
                lines.append('{0}(Text("{1}"))'.format(blok_name, tail))
    compile_node(dom)
    return SCRIPT_TEMPLATE.format(accessors=json.dumps(accessors),
                                  build_steps="\n{indent}".join(lines).format(indent=indent),
                                  indent=indent)
