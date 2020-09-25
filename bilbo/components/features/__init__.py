"""Features generation module"""

from bilbo.libs.opts import Parser

MODENAME = __name__.split('.')[-1]

parser = Parser.get_parser(name=MODENAME, help="Features")
parser.add_argument('--cfgfeatures', '-cf', type=str, metavar="Config features")
parser.add_argument('--sentence', '-s', type=str, metavar="string input value")
parser.add_argument('--input', '-i', type=str, metavar="Input XML document")
parser.add_argument('--tagname', '-t', type=str, default='bibl', \
                        metavar="bibl / note")
parser.add_argument('--verbose', '-v', action='count', default=0)
