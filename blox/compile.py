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
from blox.base import Blox, Text, UnsafeText
from blox.all import factory

SCRIPT_TEMPLATE = """# WARNING: DON'T EDIT AUTO-GENERATED

from blox.base import Blox, Text, UnsafeText

elementsExpanded = False
%(cache_elements)s
%(static_elements)s


class Template(Blox):
    __slots__ = %(accessors)s


def build(factory):
    template = Template()

    global elementsExpanded
    if not elementsExpanded:
        products = factory.products
        %(defineElements)s
        elementsExpanded = True
    %(buildTemplate)s

    return template"""


class CompiledTemplate(object):
    __slots__ = ('exec_namespace', 'factory')

    def __init__(self, exec_namespace, factory):
        self.exec_namespace = exec_namespace
        self.factory = factory

    def build(self, factory=None):
        """
            Returns a Node representation of the template using the specified factory.
        """
        factory = factory or self.factory
        return self.exec_namespace['build'](factory)

    @classmethod
    def create(self, template, factory=factory):
        """
            Compiles a template in the current python runtime into optimized python bytecode using compile and exec
            returns a CompiledTemplate instance.
        """
        code = compile(to_python(template, factory), '<string>', 'exec')
        name_space = {}
        exec(code, name_space)
        return CompiledTemplate(name_space, factory)

def to_python(template, factory=factory, indent=0, indentation='    '):
    python = []
    elements_used = set()
    accessors_used = set()
    cache_elements = set()
    static_elements = set()
    instance = 0
    parent_node = "template"

    def _render(template):
        if not template:
            return

        instance += 1
        new_node = "element" + str(instance)
        if type(template) in (str, unicode):
            python.append("\n%s%s = %s.add(" % (indented, newNode, parent_node))
            python.append('Text("' + template + '"), ensureUnique=False)')


    (accessor, id, name, create, properties, children) = (template.accessor, template.id, template.name,
                                                          template.create, template.properties, template.childElements)
    elements_used.add(create)
    element = factory.products[create]
    create = create.replace("-", "_")
    if create in ("and", "or", "with", "if", "del", "template"):
        create = "_" + create

    accessor = accessor or id
    if accessor:
        accessor = accessor.replace("-", "_")

    isCached = False
    if create.endswith("cacheelement"):
        cache_elements.add(newNode)
        isCached = True
        python += "\n%s%s = globals()['%s']" % (indented, newNode, newNode)
        python += "\n%sif not %s.rendered():" % (indented, newNode)
        python += "\n%s%s = CacheElement()" % (indented + INDENT, newNode)
        python += "\n%sglobals()['%s'] = %s" % (indented + INDENT, newNode, newNode)
    elif create in ("static", "display-static") and parent_node != "template":
        html = CompiledTemplate.create(template, factory).build(factory).toHTML()
        static_elements.add('%s = StraightHTML(html="""%s""")' % (newNode, html))
        python += "\n%s%s.add(%s, ensureUnique=False)" % (indented, parent_node, newNode)
        return (python, instance)
    else:
        python += '\n%s%s = %s(id=%s, name=%s, parent=%s)' % (indented, newNode, create.lower(), repr(id),
                                                              repr(name), parent_node)
    for name, value in properties:
        if value is not None and name in element.properties:
            propertyDict = element.properties[name]
            propertyActions = propertyDict['action'].split('.')
            propertyAction = propertyActions.pop(-1)
            if propertyActions:
                propertyActions = "." + ".".join(propertyActions)
            else:
                propertyActions = ""
            propertyName = propertyDict.get('name', name)

            if propertyAction == "classAttribute":
                python += "\n%s%s%s.%s = %s" % (indented, newNode, propertyActions, propertyName, repr(value))
            elif propertyAction == "attribute":
                python += "\n%s%s%s.attributes[%s] = %s" % (indented, newNode, propertyActions, repr(propertyName),
                                                            repr(value))
            elif propertyAction == "javascriptEvent":
                python += "\n%s%s%s.addJavascriptEvent(%s, %s)" % (indented, newNode, propertyActions,
                                                                   repr(propertyName), repr(value))
            elif propertyAction == "call":
                if value:
                    python += "\n%s%s%s.%s()" % (indented, newNode, propertyActions, propertyName)
            elif propertyAction == "send":
                python += "\n%s%s%s.%s(%s, %s)" % (indented, newNode, propertyActions,
                                                                   propertyName, repr(name), repr(value))
            elif propertyAction == "addClassesFromString":
                python += "\n%s%s%s.addClasses(%s)" % (indented, newNode, propertyActions,
                                                       repr(tuple(value.split(" "))))
            elif propertyAction == "setStyleFromString":
                python += "\n%s%s%s.style.update(%s)" % (indented, newNode, propertyActions,
                                                         repr(StyleDict.fromString(value)))
            else:
                python += "\n%s%s%s.%s(%s)" % (indented, newNode, propertyActions, propertyAction, repr(value))

    if accessor:
        accessors_used.add(accessor)
        python += "\n%stemplate.%s = %s" % (indented, accessor, newNode)

    if children:
        if isCached:
            childAccessors = set()
            childIndent = indent + 1
        else:
            childAccessors = accessors_used
            childIndent = indent
        for node in children:
            (childPython, instance) = __createPythonFromTemplate(node, factory, newNode, instance, elements_used,
                                                            childAccessors, cache_elements, static_elements, childIndent)
            python += childPython
        if isCached:
            if childAccessors:
                accessors_used.update(childAccessors)
                python += "\n%selse:" % indented
                for accessor in childAccessors:
                    python += "\n%stemplate.%s = %s" % (indented + INDENT, accessor, newNode)


    python += "\n%s%s.add(%s, ensureUnique=False)" % (indented, parent_node, newNode)
    if parent_node == "template":
        defineElements = ""
        for elementName in elements_used:
            variableName = elementName.replace("-", "_")
            if variableName in ("and", "or", "with", "if", "del", "template"):
                variableName = "_" + variableName
            defineElements += "globals()['%s'] = products['%s']\n%s" % (variableName, elementName, INDENT * 2)

        cacheDefinitions = ""
        for elementName in cache_elements:
            cacheDefinitions += "%s = CacheElement()\n" % elementName

        return SCRIPT_TEMPLATE % {'accessors':tuple(accessors_used), 'buildTemplate':python,
                                  'defineElements':defineElements, 'cache_elements':cacheDefinitions,
                                  'static_elements':"\n".join(static_elements)}


    return (python, instance)
