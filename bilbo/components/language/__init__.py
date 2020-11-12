"""Check and detect language"""

from bilbo.libs.opts import Parser

MODENAME = __name__.split('.')[-1]

parser = Parser.get_parser(name=MODENAME, help="Language")
parser.add_argument('--input_file', '-i', type=str, metavar="input file to shape")
parser.add_argument('--tag_separator', '-t', type=str, default="bibl", metavar="This tag separator extract needed sections")
parser.add_argument('--cfglanguage', '-cf', type=str, metavar="FILE")
parser.add_argument('--str_input', '-s', type=str, metavar="input string to detect language")
parser.add_argument('--verbose', '-v', action='count', default=0)
