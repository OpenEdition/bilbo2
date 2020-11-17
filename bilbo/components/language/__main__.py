"""language module"""

from bilbo.libs.opts import Parser
from bilbo.components.language.language import Language
from bilbo.importer import Importer
from bilbo.utils.bilbo_logger import get_logger

args = Parser.parse_arguments()
verbosity = args.verbose
logger = get_logger(name=__name__, verbosity=args.verbose)

cf = args.cfglanguage
input_ = args.input_file
str_ = args.str_input
is_file = True if args.input_file else False
tag = args.tag_separator
if str_:
    input_ = ''.join(('<TEI xmlns="http://www.tei-c.org/ns/1.0">', str_, '</TEI>'))

imp = Importer(input_)
doc = imp.parse_xml(tag, is_file)
logger.debug('Start detect lang')

lang = Language(cf)
lang.transform(doc, mode='tag')                           
for section in doc.sections:
    print('{0}\t - LANG : {1}'.format(section.section_naked, section.lang))
