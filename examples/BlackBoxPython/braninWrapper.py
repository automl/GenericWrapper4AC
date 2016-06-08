#!/usr/bin/env python2.7
# encoding: utf-8

'''
braninWrapper -- target algorithm warpper for branin test function

@author:     Marius Lindauer
@copyright:  2016 ML4AAD. All rights reserved.
@license:    BSD
@contact:    lindauer@informatik.uni-freiburg.de
'''

import sys
import re
import math
import logging

from abstractBlackBoxWrapper import AbstractBlackBoxWrapper

class BraninWrapper(AbstractBlackBoxWrapper):
    '''
        Simple wrapper for a blackbox function (in this case the Branin function)
    '''

    def __init__(self):
        '''
            Constructor
        '''
        logging.basicConfig()
        AbstractBlackBoxWrapper.__init__(self)
        
    def get_value(self, config):
        '''
        Gets the configuration dictionary and returns fthe unction value.
        Args:
            config: a mapping from parameter name (str) to parameter value (str)
        Returns:
            function value
        '''
        return self._get_branin_value(x1=float(config["x1"]), x2=float(config["x2"]))
    
    def _get_branin_value(self, x1, x2):
        '''
            Evaluates the Branin test function with arguments x1 and x2.
            You can replace this with your own function to minimize.
        '''
        return math.pow(x2 - (5.1 / (4 * math.pi * math.pi)) *x1*x1 + (5 / (math.pi)) *x1 -6,2) + 10*(1- (1 / (8 * math.pi))) * math.cos(x1) + 10

if __name__ == "__main__":
    wrapper = BraninWrapper()
    wrapper.main()    
