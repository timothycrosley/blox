'''blox/dom.py

Defines the basic HTML DOM elements as blox

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
from blox.base import Tag, NamedTag

from blox.attributes import AbstractAttribute, Attribute, DirectAttribute, SetAttribute, BooleanAttribute

from blox.builder import Factory


factory = Factory('dom')


@factory.add()
class A(Tag):
    '''Defines a link that when clicked changes the current viewed page'''
    __slots__ = ()
    tag = "a"
    href = Attribute()
    media = Attribute()
    rel = Attribute()
    target = Attribute()
    type = Attribute()


@factory.add()
class Abr(Tag):
    '''Defines  an abbreviation or an acronym'''
    __slots__ = ()
    tag = "abr"


@factory.add()
class Address(Tag):
    '''Defines contact info for the author of a document or article'''
    __slots__ = ()
    tag = "address"


@factory.add()
class Area(Tag):
    '''Defines an area inside of an image map'''
    __slots__ = ()
    tag = 'area'
    alt = Attribute()
    coords = Attribute()
    href = Attribute()
    hreflang = Attribute()
    media = Attribute()
    rel = Attribute()
    shape = Attribute()
    target = Attribute()
    type = Attribute()


@factory.add()
class Article(Tag):
    '''Defines an independent, self-contained content'''
    __slots__ = ()
    tag = "article"


@factory.add()
class Aside(Tag):
    '''Defines content as being aside from the content it is placed in'''
    __slots__ = ()
    tag = "aside"


@factory.add()
class Audio(Tag):
    '''Defines sound, such as music or other audio streams'''
    __slots__ = ()
    tag = "audio"
    autoplay = BooleanAttribute()
    controls = BooleanAttribute()
    loop = BooleanAttribute()
    src = Attribute()


@factory.add()
class B(Tag):
    '''Defines bold text
        NOTE: avoid using this element, when possible use elements that describe the content
              instead of the appearance
    '''
    __slots__ = ()
    tag = "b"


@factory.add()
class Base(Tag):
    '''Defines the base URL for all relative URLs in a document'''
    __slots__ = ()
    tag = 'base'
    href = Attribute()
    target = Attribute


@factory.add()
class BDI(Tag):
    """
        Defines a part of text that should be formatted in a different direction
        from the other text outside it
    """
    __slots__ = ()
    tag = "bdi"


@factory.add()
class BDO(Tag):
    """
        Defines an override of the current text-direction
    """
    __slots__ = ()
    tag = "bdo"
    properties = Tag.properties.copy()
    properties['dir'] = {'action':'attribute'}


@factory.add()
class BlockQuote(Tag):
    """
        Defines a section that is quoted from another source
    """
    __slots__ = ()
    tag = "blockquote"
    properties = Tag.properties.copy()
    properties['cite'] = {'action':'attribute'}


@factory.add()
class Body(Tag):
    """
        Defines the document's body - which contains all the visible parts of an HTML document
    """
    __slots__ = ()
    tag = "body"


@factory.add()
class Br(Tag):
    """
        Defines a single line break
    """
    __slots__ = ()
    tag = "br"
    tag_self_closes = True
    allowsChildren = False


@factory.add()
class Button(Tag):
    """
        Defines a click-able button
    """
    __slots__ = ()
    tag = "button"
    properties = Tag.properties.copy()
    properties['autofocus'] = {'action':'attribute', 'type':'bool'}
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['form'] = {'action':'attribute'}
    properties['formaction'] = {'action':'attribute'}
    properties['formenctype'] = {'action':'attribute'}
    properties['formnovalidate'] = {'action':'attribute', 'type':'bool'}
    properties['formtarget'] = {'action':'attribute'}
    properties['type'] = {'action':'attribute'}
    properties['value'] = {'action':'attribute'}


@factory.add()
class Canvas(Tag):
    """
        Defines an area of the screen to draw graphic on the fly
    """
    __slots__ = ()
    tag = "canvas"
    allowsChildren = False
    properties = Tag.properties.copy()
    properties['height'] = {'action':'attribute', 'type':'int'}
    properties['width'] = {'action':'attribute', 'type':'int'}


@factory.add()
class Caption(Tag):
    """
        Defines a table caption
    """
    __slots__ = ()
    tag = "caption"


@factory.add()
class Cite(Tag):
    """
        Defines the title of a work
    """
    __slots__ = ()
    tag = "cite"


@factory.add()
class Code(Tag):
    """
        Defines a piece of programming code
    """
    __slots__ = ()
    tag = "code"


@factory.add()
class Col(Tag):
    """
        Defines a table column
    """
    __slots__ = ()
    tag = "col"
    properties = Tag.properties.copy()
    properties['span'] = {'action':'attribute', 'type':'int'}


@factory.add()
class ColGroup(Tag):
    """
        Defines a group of one or more columns in a table
    """
    __slots__ = ()
    tag = "colgroup"
    properties = Tag.properties.copy()
    properties['span'] = {'action':'attribute', 'type':'int'}


@factory.add()
class Command(Tag):
    """
        Defines a click-able command button
    """
    __slots__ = ()
    tag = "command"
    properties = Tag.properties.copy()
    properties['checked'] = {'action':'attribute', 'type':'bool'}
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['icon'] = {'action':'attribute'}
    properties['label'] = {'action':'attribute'}
    properties['radiogroup'] = {'action':'attribute'}
    properties['type'] = {'action':'attribute'}


@factory.add()
class DataList(Tag):
    """
        Defines a list of pre-defined options for input controls
    """
    __slots__ = ()
    tag = "datalist"


@factory.add()
class DD(Tag):
    """
        Defines a description of an item in a definition list
    """
    __slots__ = ()
    tag = "dd"


@factory.add()
class Del(Tag):
    """
        Defines text that has been deleted from a document
    """
    __slots__ = ()
    tag = "del"
    properties = Tag.properties.copy()
    properties['cite'] = {'action':'attribute'}
    properties['datetime'] = {'action':'attribute'}


@factory.add()
class Details(Tag):
    """
        Defines collapse-able details
    """
    __slots__ = ()
    tag = "details"
    properties = Tag.properties.copy()
    properties['open'] = {'action':'attribute'}


@factory.add()
class Dfn(Tag):
    """
        Defines a definition term
    """
    __slots__ = ()
    tag = "dfn"


@factory.add()
class Div(Tag):
    """
        Defines a section of a document
    """
    __slots__ = ()
    tag = "div"


@factory.add()
class DL(Tag):
    """
        Defines a definition list
    """
    __slots__ = ()
    tag = "dl"


@factory.add()
class DT(Tag):
    """
        Defines a term (an item) in a definition list
    """
    __slots__ = ()
    tag = "dt"


@factory.add()
class Em(Tag):
    """
        Defines emphasized text
    """
    __slots__ = ()
    tag = "em"


@factory.add()
class Embed(Tag):
    """
        Defines a container for an external (non-HTML) application
    """
    __slots__ = ()
    tag = "embed"
    properties = Tag.properties.copy()
    properties['height'] = {'action':'attribute'}
    properties['src'] = {'action':'attribute'}
    properties['types'] = {'action':'attribute'}
    properties['width'] = {'action':'attribute', 'type':'int'}


@factory.add()
class FieldSet(Tag):
    """
        Defines a group of related elements in a form
    """
    __slots__ = ()
    tag = "fieldset"
    properties = Tag.properties.copy()
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['form'] = {'action':'attribute'}


@factory.add()
class FigCaption(Tag):
    """
        Defines a caption for a figure element
    """
    __slots__ = ()
    tag = "figcaption"


@factory.add()
class Figure(Tag):
    """
        Defines self-contained figure content
    """
    __slots__ = ()
    tag = "figure"


@factory.add()
class Footer(Tag):
    """
        Defines a footer for a document or section
    """
    __slots__ = ()
    tag = "footer"


@factory.add()
class Form(Tag):
    """
        Defines a form for user input
    """
    __slots__ = ()
    tag = "form"
    properties = Tag.properties.copy()
    properties['accept'] = {'action':'attribute'}
    properties['accept-charset'] = {'action':'attribute'}
    properties['action'] = {'action':'attribute'}
    properties['autocomplete'] = {'action':'attribute', 'type':'bool'}
    properties['enctype'] = {'action':'attribute'}
    properties['method'] = {'action':'attribute'}
    properties['name'] = {'action':'attribute'}
    properties['novalidate'] = {'action':'attribute'}
    properties['target'] = {'action':'attribute'}


@factory.add()
class H(Tag):
    """
        Defines the abstract concept of an HTML header
    """
    __slots__ = ()


@factory.add()
class H1(H):
    """
        Defines the most important heading
    """
    __slots__ = ()
    tag = "h1"


@factory.add()
class H2(H):
    """
        Defines the 2nd most important heading
    """
    __slots__ = ()
    tag = "h2"


@factory.add()
class H3(H):
    """
        Defines the 3rd most important heading
    """
    __slots__ = ()
    tag = "h3"


@factory.add()
class H4(H):
    """
        Defines the 4th most important heading
    """
    __slots__ = ()
    tag = "h4"


@factory.add()
class H5(H):
    """
        Defines the 5th most important heading
    """
    __slots__ = ()
    tag = "h5"


@factory.add()
class H6(H):
    """
        Defines the least important heading
    """
    __slots__ = ()
    tag = "h6"


@factory.add()
class Head(Tag):
    """
        Defines information about the document
    """
    __slots__ = ()
    tag = "head"


@factory.add()
class Header(Tag):
    """
        Defines a header for a document or section
    """
    __slots__ = ()
    tag = "header"


@factory.add()
class HGroup(Tag):
    """
        Defines a grouping of multiple header elements
    """
    __slots__ = ()
    tag = "hgroup"


@factory.add()
class HR(Tag):
    """
        Defines a thematic change in the content horizontally
    """
    __slots__ = ()
    tag = "hr"
    tag_self_closes = True
    allowsChildren = False


@factory.add()
class HTML(Tag):
    """
        Defines the root of an HTML document
    """
    __slots__ = ()
    tag = "html"
    properties = Tag.properties.copy()
    properties['manifest'] = {'action':'attribute'}


@factory.add()
class I(Tag):
    """
        Defines text that is in an alternate voice or mood
        NOTE: avoid using this element, when possible use elements that describe the content
              instead of the appearance
    """
    __slots__ = ()
    tag = "i"


@factory.add()
class IFrame(Tag):
    """
        Defines an inline frame
    """
    __slots__ = ()
    tag = "iframe"
    properties = Tag.properties.copy()
    properties['sandbox'] = {'action':'attribute'}
    properties['seamless'] = {'action':'attribute', 'type':'bool'}
    properties['src'] = {'action':'attribute'}
    properties['srcdoc'] = {'action':'attribute'}
    properties['width'] = {'action':'attribute', 'type':'int'}
    properties['frameborder'] = {'action':'attribute'}


@factory.add()
class Img(Tag):
    """
        Defines an image
    """
    __slots__ = ()
    tag = "img"
    tag_self_closes = True
    allowsChildren = False
    properties = Tag.properties.copy()
    properties['src'] = {'action':'setImage'}
    properties['alt'] = {'action':'attribute'}
    properties['crossorigin'] = {'action':'attribute'}
    properties['ismap'] = {'action':'attribute', 'type':'bool'}
    properties['width'] = {'action':'attribute', 'type':'int'}
    properties['height'] = {'action':'attribute', 'type':'int'}

    def setImage(self, image):
        self.attributes['src'] = Settings.STATIC_URL + image

    def image(self):
        return self.attributes['src'].replace(Settings.STATIC_URL, "")


@factory.add()
class Input(Tag):
    """
        Defines an input control
    """
    __slots__ = ()
    tag = "input"
    tag_self_closes = True
    allowsChildren = False
    properties = Tag.properties.copy()
    properties['accept'] = {'action':'attribute'}
    properties['alt'] = {'action':'attribute'}
    properties['autocomplete'] = {'action':'attribute', 'type':'bool'}
    properties['autofocus'] = {'action':'attribute', 'type':'bool'}
    properties['checked'] = {'action':'attribute', 'type':'bool'}
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['form'] = {'action':'attribute'}
    properties['formaction'] = {'action':'attribute'}
    properties['formenctype'] = {'action':'attribute'}
    properties['formmethod'] = {'action':'attribute'}
    properties['formnovalidate'] = {'action':'attribute'}
    properties['formtarget'] = {'action':'attribute'}
    properties['height'] = {'action':'attribute', 'type':'int'}
    properties['list'] = {'action':'attribute'}
    properties['max'] = {'action':'attribute'}
    properties['maxlength'] = {'action':'attribute', 'type':'int'}
    properties['min'] = {'action':'attribute'}
    properties['multiple'] = {'action':'attribute', 'type':'bool'}
    properties['pattern'] = {'action':'attribute'}
    properties['placeholder'] = {'action':'attribute'}
    properties['readonly'] = {'action':'attribute', 'type':'bool'}
    properties['required'] = {'action':'attribute', 'type':'bool'}
    properties['size'] = {'action':'attribute', 'type':'int'}
    properties['src'] = {'action':'attribute'}
    properties['step'] = {'action':'attribute', 'type':'int'}
    properties['type'] = {'action':'attribute'}
    properties['value'] = {'action':'attribute'}
    properties['width'] = {'action':'attribute', 'type':'int'}


@factory.add()
class Ins(Tag):
    """
        Defines text that has been inserted into a document
    """
    __slots__ = ()
    tag = "ins"
    properties = Tag.properties.copy()
    properties['cite'] = {'action':'attribute'}
    properties['datetime'] = {'action':'attribute'}


@factory.add()
class Kbd(Tag):
    """
        Defines keyboard input
    """
    __slots__ = ()
    tag = "kbd"


@factory.add()
class KeyGen(Tag):
    """
        Defines a key-pair generator field
    """
    __slots__ = ()
    tag = "keygen"
    properties = Tag.properties.copy()
    properties['autofocus'] = {'action':'attribute', 'type':'bool'}
    properties['challenge'] = {'action':'attribute', 'type':'bool'}
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['form'] = {'action':'attribute'}
    properties['keytype'] = {'action':'attribute'}
    properties['name'] = {'action':'attribute'}


@factory.add()
class Label(Tag):
    """
        Defines a label for an input element
    """
    __slots__ = ()
    tag = "label"
    properties = Tag.properties.copy()
    properties['for'] = {'action':'attribute'}
    properties['form'] = {'action':'attribute'}


@factory.add()
class Legend(Tag):
    """
        Defines a caption for a fieldset, figure or details element
    """
    __slots__ = ()
    tag = "legend"


@factory.add()
class LI(Tag):
    """
        Defines a list item
    """
    __slots__ = ()
    tag = "li"
    properties = Tag.properties.copy()
    properties['value'] = {'action':'attribute', 'type':'int'}


@factory.add()
class Link(Tag):
    """
        Defines the relationship between a document an external resource
    """
    __slots__ = ()
    tag = "link"
    tag_self_closes = True
    allowsChildren = False
    properties = Tag.properties.copy()
    properties['charset'] = {'action':'attribute'}
    properties['src'] = {'action':'setSource'}
    properties['href'] = {'action':'setHref'}
    properties['hreflang'] = {'action':'attribute'}
    properties['media'] = {'action':'attribute'}
    properties['rel'] = {'action':'attribute'}
    properties['type'] = {'action':'attribute'}
    properties['sizes'] = {'action':'attribute'}

    def setHref(self, href):
        self.attributes['href'] = Settings.STATIC_URL + href

    def href(self):
        return self.attributes['href'].replace(Settings.STATIC_URL, "")

    def setSource(self, source):
        self.attributes['src'] = Settings.STATIC_URL + source

    def source(self, source):
        return self.attributes['src'].replace(Settings.STATIC_URL, "")


@factory.add()
class Map(Tag):
    """
        Defines a client side image map
    """
    __slots__ = ()
    tag = "map"


@factory.add()
class Mark(Tag):
    """
        Defines marked / highlighted text
    """
    __slots__ = ()
    tag = "mark"


@factory.add()
class Meta(Tag):
    """
        Defines metadata about an HTML document
    """
    __slots__ = ()
    tag = "meta"
    tag_self_closes = True
    allowsChildren = False
    properties = Tag.properties.copy()
    properties['charset'] = {'action':'attribute'}
    properties['content'] = {'action':'attribute'}
    properties['http-equiv'] = {'action':'attribute'}


@factory.add()
class Meter(Tag):
    """
        Defines a scalar measurement within a known range
    """
    __slots__ = ()
    tag = "meter"
    properties = Tag.properties.copy()
    properties['form'] = {'action':'attribute'}
    properties['high'] = {'action':'attribute', 'type':'int'}
    properties['low'] = {'action':'attribute', 'type':'int'}
    properties['max'] = {'action':'attribute', 'type':'int'}
    properties['min'] = {'action':'attribute', 'type':'int'}
    properties['optimum'] = {'action':'attribute', 'type':'int'}
    properties['value'] = {'action':'attribute', 'type':'int'}


@factory.add()
class Nav(Tag):
    """
        Defines navigation links
    """
    __slots__ = ()
    tag = "nav"


@factory.add()
class NoScript(Tag):
    """
        Defines alternate content for users that do not support client side scripts
    """
    __slots__ = ()
    tag = "noscript"


@factory.add()
class Object(Tag):
    """
        Defines an embedded object
    """
    __slots__ = ()
    tag = "object"
    properties = Tag.properties.copy()
    properties['form'] = {'action':'attribute'}
    properties['height'] = {'action':'attribute', 'type':'int'}
    properties['type'] = {'action':'attribute'}
    properties['usemap'] = {'action':'attribute'}
    properties['width'] = {'action':'attribute', 'type':'int'}


@factory.add()
class OL(Tag):
    """
        Defines an ordered list
    """
    __slots__ = ()
    tag = "ol"
    properties = Tag.properties.copy()
    properties['reversed'] = {'action':'attribute', 'type':'bool'}
    properties['start'] = {'action':'attribute', 'type':'int'}
    properties['type'] = {'action':'attribute'}


@factory.add()
class OptGroup(Tag):
    """
        Defines a group of related options in a drop-down list
    """
    __slots__ = ()
    tag = "optgroup"
    properties = Tag.properties.copy()
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['label'] = {'action':'attribute'}


@factory.add()
class Option(Tag):
    """
        Defines an option in a drop-down list
    """
    __slots__ = ()
    tag = "option"
    properties = Tag.properties.copy()
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['label'] = {'action':'attribute'}
    properties['selected'] = {'action':'attribute', 'type':'bool'}
    properties['value'] = {'action':'attribute'}


@factory.add()
class Output(Tag):
    """
        Defines the result of a calculation
    """
    __slots__ = ()
    tag = "output"
    properties = Tag.properties.copy()
    properties['for'] = {'action':'attribute'}
    properties['form'] = {'action':'attribute'}


@factory.add()
class P(Tag):
    """
        Defines a paragraph
    """
    __slots__ = ()
    tag = "p"


@factory.add()
class Param(Tag):
    """
        Defines a parameter for an object
    """
    __slots__ = ()
    tag = "param"
    tag_self_closes = True
    allowsChildren = False
    properties = Tag.properties.copy()
    properties['value'] = {'action':'attribute'}


@factory.add()
class Pre(Tag):
    """
        Defines pre formatted text
    """
    __slots__ = ()
    tag = "pre"


@factory.add()
class Progress(Tag):
    """
        Defines the progress of a task
    """
    __slots__ = ()
    tag = "progress"
    properties = Tag.properties.copy()
    properties['max'] = {'action':'attribute', 'type':'int'}
    properties['value'] = {'action':'attribute', 'type':'int'}


@factory.add()
class Q(Tag):
    """
        Defines a short quotation
    """
    __slots__ = ()
    tag = "q"
    properties = Tag.properties.copy()
    properties['cite'] = {'action':'attribute'}


@factory.add()
class RP(Tag):
    """
        Defines what to show in browsers that do not support ruby annotations
    """
    __slots__ = ()
    tag = "rp"


@factory.add()
class RT(Tag):
    """
        Defines an explanation / pronunciation of characters (for East Asian typography)
    """
    __slots__ = ()
    tag = "rt"


@factory.add()
class Ruby(Tag):
    """
        Defines ruby annotations (for East Asian typography)
    """
    __slots__ = ()
    tag = "ruby"


@factory.add()
class S(Tag):
    """
        Defines text that is no longer correct
    """
    __slots__ = ()
    tag = "s"


@factory.add()
class Samp(Tag):
    """
        Defines sample output from a computer program
    """
    __slots__ = ()
    tag = "samp"


@factory.add()
class Script(Tag):
    """
        Defines a client-side script
    """
    __slots__ = ()
    tag = "script"
    properties = Tag.properties.copy()
    properties['async'] = {'action':'attribute', 'type':'bool'}
    properties['defer'] = {'action':'attribute', 'type':'bool'}
    properties['type'] = {'action':'attribute'}
    properties['charset'] = {'action':'attribute'}
    properties['src'] = {'action':'setScriptFile'}

    def setScriptFile(self, scriptFile):
        self.attributes['src'] = Settings.STATIC_URL + scriptFile

    def scriptFile(self):
        return self.attributes['src'].replace(Settings.STATIC_URL, "")


@factory.add()
class Section(Tag):
    """
        Defines a section of the document
    """
    __slots__ = ()
    tag = "section"


@factory.add()
class Select(Tag):
    """
        Defines a drop-down list
    """
    __slots__ = ()
    tag = "select"
    properties = Tag.properties.copy()
    properties['autofocus'] = {'action':'attribute', 'type':'bool'}
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['form'] = {'action':'attribute'}
    properties['multiple'] = {'action':'attribute', 'type':'bool'}
    properties['size'] = {'action':'attribute', 'type':'int'}


@factory.add()
class Small(Tag):
    """
        Defines smaller text
        NOTE: avoid using this element, when possible use elements that describe the content
              instead of the appearance
    """
    __slots__ = ()
    tag = "small"


@factory.add()
class Source(Tag):
    """
        Defines multiple media resources for media elements
    """
    __slots__ = ()
    tag = "source"
    properties = Tag.properties.copy()
    properties['media'] = {'action':'attribute'}
    properties['src'] = {'action':'attribute'}
    properties['type'] = {'action':'attribute'}


@factory.add()
class Span(Tag):
    """
        Defines a section in a document
    """
    __slots__ = ()
    tag = "span"


@factory.add()
class Strong(Tag):
    """
        Defines important text
    """
    __slots__ = ()
    tag = "strong"


@factory.add()
class Style(Tag):
    """
        Defines style information for a document
    """
    __slots__ = ()
    tag = "style"
    properties = Tag.properties.copy()
    properties['media'] = {'action':'attribute'}
    properties['scoped'] = {'action':'attribute', 'type':'bool'}
    properties['type'] = {'action':'attribute'}


@factory.add()
class Sub(Tag):
    """
        Defines sub-scripted text
    """
    __slots__ = ()
    tag = "sub"


@factory.add()
class Summary(Tag):
    """
        Defines a visible heading for a details element
    """
    __slots__ = ()
    tag = "summary"


@factory.add()
class Sup(Tag):
    """
        Defines super-scripted text
    """
    __slots__ = ()
    tag = "sup"


@factory.add()
class Table(Tag):
    """
        Defines a table - should be used for tables of data only (not for layout)
    """
    __slots__ = ()
    tag = "table"
    properties = Tag.properties.copy()
    properties['border'] = {'action':'attribute', 'type':'bool'}


@factory.add()
class TBody(Tag):
    """
        Defines a group of content within a table
    """
    __slots__ = ()
    tag = "tbody"


@factory.add()
class TD(Tag):
    """
        Defines a table cell
    """
    __slots__ = ()
    tag = "td"
    properties = Tag.properties.copy()
    properties['colspan'] = {'action':'attribute', 'type':'number'}
    properties['headers'] = {'action':'attribute'}
    properties['rowspan'] = {'action':'attribute', 'type':'number'}


@factory.add()
class TextArea(Tag):
    """
        Defines multi-line text input
    """
    __slots__ = ()
    tag = "textarea"
    properties = Tag.properties.copy()
    properties['autofocus'] = {'action':'attribute', 'type':'bool'}
    properties['cols'] = {'action':'attribute', 'type':'int'}
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['form'] = {'action':'attribute'}
    properties['maxlength'] = {'action':'attribute', 'type':'int'}
    properties['placeholder'] = {'action':'attribute'}
    properties['readonly'] = {'action':'attribute', 'type':'bool'}
    properties['required'] = {'action':'attribute', 'type':'bool'}
    properties['rows'] = {'action':'attribute', 'type':'int'}
    properties['wrap'] = {'action':'attribute'}


@factory.add()
class TFoot(Tag):
    """
        Defines the footer of a table
    """
    __slots__ = ()
    tag = "tfoot"


@factory.add()
class TH(Tag):
    """
        Defines the header cell within a table
    """
    __slots__ = ()
    tag = "th"
    properties = Tag.properties.copy()
    properties['colspan'] = {'action':'attribute', 'type':'int'}
    properties['headers'] = {'action':'attribute'}
    properties['rowspan'] = {'action':'attribute', 'type':'int'}
    properties['scope'] = {'action':'attribute'}


@factory.add()
class THead(Tag):
    """
        Defines header content within a table
    """
    __slots__ = ()
    tag = "thead"


@factory.add()
class Time(Tag):
    """
        Defines a date / time
    """
    __slots__ = ()
    tag = "time"
    properties = Tag.properties.copy()
    properties['datetime'] = {'action':'attribute'}
    properties['pubdate'] = {'action':'attribute'}


@factory.add()
class Title(Tag):
    """
        Defines the title of a document
    """
    __slots__ = ()
    tag = "title"


@factory.add()
class TR(Tag):
    """
        Defines a table row
    """
    __slots__ = ()
    tag = "tr"


@factory.add()
class Track(Tag):
    """
        Defines text tracks for media elements
    """
    __slots__ = ()
    tag = "track"
    properties = Tag.properties.copy()
    properties['default'] = {'action':'attribute', 'type':'bool'}
    properties['kind'] = {'action':'attribute'}
    properties['label'] = {'action':'attribute'}
    properties['src'] = {'action':'attribute'}
    properties['srclang'] = {'action':'attribute'}


@factory.add()
class U(Tag):
    """
        Defines text that should be stylistically different from normal text
        NOTE: avoid using this element, when possible use elements that describe the content
              instead of the appearance
    """
    __slots__ = ()
    tag = "u"


@factory.add()
class UL(Tag):
    """
        Defines an unordered list
    """
    __slots__ = ()
    tag = "ul"


@factory.add()
class Var(Tag):
    """
        Defines a variable
    """
    __slots__ = ()
    tag = "var"


@factory.add()
class Video(Tag):
    """
        Defines a video or movie
    """
    __slots__ = ()
    tag = "video"
    properties = Tag.properties.copy()
    properties['autoplay'] = {'action':'attribute', 'type':'bool'}
    properties['controls'] = {'action':'attribute', 'type':'bool'}
    properties['height'] = {'action':'attribute', 'type':'int'}
    properties['loop'] = {'action':'attribute', 'type':'bool'}
    properties['muted'] = {'action':'attribute', 'type':'bool'}
    properties['poster'] = {'action':'attribute'}
    properties['preload'] = {'action':'attribute'}
    properties['src'] = {'action':'attribute'}
    properties['width'] = {'action':'attribute', 'type':'int'}


@factory.add()
class Wbr(Tag):
    """
        Defines a possible line-break
    """
    __slots__ = ()
    tag = "wbr"


