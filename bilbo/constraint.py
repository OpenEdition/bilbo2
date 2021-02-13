""" XML converter """
#-*- coding: utf-8 -*-
from lxml import etree
import os
import subprocess


class Rule(object):
    """
    XML converter class
    """

    def __init__(self, constraint):
        self.constraint = constraint

    def check(self, instance):
        if self.constraint is None:
            return True
        return self._check_on_instance(instance)
            
    def _check_on_instance(self, instance):
        for s in self.constraint.get((type(instance).__name__).lower, list()):
            for k, v in s.items():
                if (v != getattr(instance,k)):
                    return False
        return True
