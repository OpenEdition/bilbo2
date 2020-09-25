from bilbo.libs.opts import Parser

parser = Parser.get_parser(name="tests")
parser.add_argument('--reports', '-r', action="store_true", default=False)
