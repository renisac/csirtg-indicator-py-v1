from .plugin import Plugin
import time
import os
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

OUTPUT_PATH = os.getenv('CSIRTG_INDICATOR_BIND_PATH', '/etc/namedb')


def get_lines(data, filename=OUTPUT_PATH):
    output = StringIO()
    output.write("// generated by: {} at {}\n".format('csirtg-indicator', time.strftime('%Y-%M-%dT%H:%m:%S %Z')))

    for i in data:
        if i.itype is not 'fqdn':
            continue

        output.write('zone "{}" {{type master; file "{}";}};'.format(i.indicator, filename))
        yield output.getvalue()

        if isinstance(output, StringIO):
            output.truncate(0)


class Bind(Plugin):

    def __init__(self, *args, **kwargs):
        super(Bind, self).__init__(*args, **kwargs)

        self.output = kwargs.get('output', OUTPUT_PATH)

    def __repr__(self):
        text = [
            '// generated by: {} at {}'.format('csirtg-indicator', time.strftime('%Y-%M-%dT%H:%m:%S %Z'))
        ]
        for i in self.data:
            if i.itype is not 'fqdn':
                pass

            text.append('zone "{}" {{type master; file "{}";}};'.format(i.indicator, self.output))

        return '\n'.join(text)
