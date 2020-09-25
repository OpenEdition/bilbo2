""" @brief Gestion des options """

import sys
import argparse
import logging
from configparser import ConfigParser
logger = logging.getLogger()

class Parser(object):
    
    _parser = None
    _subparser = None
    _args = None

    @classmethod
    def _default_parser(cls, name):
        cls._parser = argparse.ArgumentParser(prog=name)
        return cls._parser

    @classmethod
    def get_parser(cls, name, help=None):
        if cls._parser is None:
            return cls._default_parser(name)
        elif cls._subparser is None:
            cls._subparser = cls._parser.add_subparsers(help='Bilbo components', dest="mode_name")
        return cls._subparser.add_parser(name)

    @classmethod
    def parse_arguments(cls):
        if cls._args is None:
            cls._args = cls._parser.parse_args()
        return cls._args

    @classmethod
    def getArgs(cls):
        pass

class BilboParser:
    _section_args = None

    @classmethod
    def factory(cls, type_args, section_args):
        if cls is BilboParser:
            cls._section_args = section_args
            return IniParser if type_args == 'ini' else DictParser

    @classmethod
    def getArgs(cls, args, opt, type_opt, pipe):
        section_pipe = cls._section_args if pipe is None else pipe
        if type_opt is None:
            return args.get(section_pipe, opt)
        if type_opt== 'lst':
            return [itm.strip() for itm in args.get(section_pipe, opt).split(",")]
        if type_opt== 'eval':
            return eval("[%s]" % args.get(section_pipe, opt))

class IniParser(BilboParser):
    @classmethod
    def getArgs(cls, cfg_file, opt, type_opt=None, pipe=None):
        """
        Gets arguments from config file

        :param cfgFile: config file
        :param opt: specify the option in the file
        """
        config = ConfigParser()
        config.read(cfg_file)
        return super(IniParser, cls).getArgs(config, opt, type_opt, pipe)

class DictParser(BilboParser):
    @classmethod
    def getArgs(cls, args, opt, type_opt=None, pipe=None):
        return super(DictParser, cls).getArgs(args, opt, type_opt, pipe)
