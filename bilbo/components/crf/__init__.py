"""CRF module (train / tag / evaluate)"""

from bilbo.libs.opts import Parser

MODENAME = __name__.split('.')[-1]

parser = Parser.get_parser(name=MODENAME, help="Crf")
parser.add_argument('--cfgcrf', '-cf', type=str, metavar="Config crf")
parser.add_argument('--model', '-M', type=str, metavar="model file")
parser.add_argument('--input', '-i', type=str, metavar="fichier d'input")
parser.add_argument('--train', '-T', action='store_true')
parser.add_argument('--tag', '-t', action='store_true')
parser.add_argument('--evaluate', '-e', action='store_true')
parser.add_argument('--verbose', '-v', action='count', default=0)
