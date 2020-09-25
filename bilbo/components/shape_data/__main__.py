"""shape module"""

from bilbo.libs.opts import Parser
from bilbo.importer import Importer
from bilbo.components.shape_data.shape_data import ShapeSection
from lxml import etree
from bilbo.utils.bilbo_logger import get_logger

args = Parser.parse_arguments()
verbosity = args.verbose
logger = get_logger(name=__name__, verbosity=args.verbose)

cfg_shape_data = args.cfgshapedata
input_ = args.input_file
str_ = args.str_input
is_file = True if args.input_file else False
tag = args.tag_separator
if str_:
    input_ = ''.join(('<TEI xmlns="http://www.tei-c.org/ns/1.0">', str_, '</TEI>'))

imp = Importer(input_)
doc = imp.parse_xml(tag, is_file)
logger.debug('Instantiate Bilbo')

shaped_data = ShapeSection(cfg_shape_data)
shaped_data.transform(doc)                           
for section in doc.sections:
    print(section.section_naked)
    for token in section.tokens:
        print('Token:{0}\t Label:{1} \t Xpath:{2}'.format(token.str_value, token.label, token.xpath))
