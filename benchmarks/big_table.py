"""benchmarks/big_table.py

Benchmarks blox to see how quickly it can build a large 10x1000 HTML table
Copyright (C) 2015 Timothy Edmund Crosley

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

"""
import time
from contextlib import contextmanager

benchmarks = {}
TABLE = [dict(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10) for _ in list(range(1000))]


@contextmanager
def benchmark(framework):
    start = time.time()
    yield
    benchmarks[framework] = time.time() - start


def benchmark_blox():
    from blox.base import Text
    from blox.dom import Table, TR, TD

    table = Table()
    with benchmark('Blox'):
        for row in TABLE:
            table_row = table(TR())
            for column in row.values():
                table_row(TD(Text(column)))
        print(table.render())


def benchmark_jinja2():
    from jinja2 import Template

    template = Template("""
    <table>
        {% for row in table_data %}
        <tr>
            {% for column in row.values() %}
                <td>
                    {{ column }}
                </td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table
    """)
    with benchmark('Jinja2'):
        print(template.render(table_data=TABLE))


def benchmark_django():
    from django.template import Context, Template
    from django.core.management import settings

    settings.configure({})

    from django.conf import settings
    settings.TEMPLATES = ()
    settings.TEMPLATE_DIRS = ()
    settings.ALLOWED_INCLUDE_ROOTS = False
    settings.TEMPLATE_CONTEXT_PROCESSORS = ()
    settings.TEMPLATE_DEBUG = False
    settings.TEMPLATE_LOADERS = ()
    settings.TEMPLATE_STRING_IF_INVALID = False
    settings.DEBUG = False
    settings.FILE_CHARSET = 'utf8'
    settings.LOGGING_CONFIG = {}
    settings.LOGGING = {}
    settings.INSTALLED_APPS = ()
    settings.USE_L10N = True
    settings.USE_I18N = True
    settings.LANGUAGE_CODE = 'en'
    settings.FORMAT_MODULE_PATH = ()
    settings.LOCALE_PATHS = ''
    settings.USE_THOUSAND_SEPARATOR = False

    import django
    django.setup()

    template = Template("""
    <table>
        {% for row in table_data %}
        <tr>
            {% for column in row.values %}
                <td>
                    {{ column }}
                </td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table
    """)

    with benchmark('Django Templates'):
        context = Context({"table_data": TABLE})
        template.render(context)


benchmark_blox()
benchmark_jinja2()
benchmark_django()
for framework_name, time in benchmarks.items():
    print('{0} Total Time: {1}'.format(framework_name, time))
