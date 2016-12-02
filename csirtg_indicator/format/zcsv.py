import csv
from csirtg_indicator.constants import PYVERSION
from csirtg_indicator import Indicator

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from .plugin import Plugin

if PYVERSION > 2:
    basestring = (str, bytes)

class Csv(Plugin):

    def __repr__(self):
        output = StringIO()
        
        csvWriter = csv.DictWriter(output, self.cols, quoting=csv.QUOTE_ALL)
        csvWriter.writeheader()

        for i in reversed(self.data):
            if isinstance(i, Indicator):
                i = i.__dict__()

            r = dict()
            for c in self.cols:
                y = i.get(c, u'')
                if type(y) is list:
                    y = u','.join(y)

                if PYVERSION < 3:
                    r[c] = y
                    if isinstance(r[c], basestring):
                        r[c] = unicode(r[c]).replace('\n', r'\\n')
                        r[c] = r[c].encode('utf-8', 'ignore')
                else:
                    r[c] = y
                    if isinstance(r[c], basestring):
                        r[c] = r[c].replace('\n', r'\\n')
                
            csvWriter.writerow(r)
        
        return output.getvalue().strip('\r\n')