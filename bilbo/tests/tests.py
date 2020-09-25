import unittest
from bilbo.libs.opts import Parser
from os.path import dirname, abspath


BILBO_HOME = dirname(abspath(__file__))

if __name__=="__main__":
    args = Parser.parse_arguments()
    testsuite = unittest.TestLoader().discover(BILBO_HOME)
    if args.reports:
        try:
            import xmlrunner
            testrunner = xmlrunner.XMLTestRunner(output='tests_report', descriptions=True)
            test_results = testrunner.run(testsuite)
        except ImportError:
            print('\n\You should install xmlrunner!\n\n', file=sys.stderr)
    else:
        unittest.TextTestRunner(verbosity=2).run(testsuite)

