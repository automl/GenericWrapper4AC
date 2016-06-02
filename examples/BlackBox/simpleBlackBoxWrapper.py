#!/usr/bin/env python2.7
# encoding: utf-8

'''
SimpleBlackBoxWrapper -- template for an AClib target algorithm warpper
abstract methods for generation of callstring and parsing of solver output 
@author:     Marius Lindauer, Chris Fawcett, Alex Fréchette, Frank Hutter
@copyright:  2014 AClib. All rights reserved.
@license:    GPL
@contact:    lindauer@informatik.uni-freiburg.de, fawcettc@cs.ubc.ca, afrechet@cs.ubc.ca, fh@informatik.uni-freiburg.de

example call (in aclib folder structure):
python src/generic_wrapper/simpleBlackBoxWrapper.py --internal True --script src/generic_wrapper/simple_wrappers/braninSimpleWrapper.py dummy_instance "" 0.0 2147483647 1234 -x1  3.141592 -x2 5
'''

import sys
import os
import imp
import re
import math

from genericWrapper import AbstractWrapper

class SimpleBlackBoxWrapper(AbstractWrapper):
    '''
        Simple wrapper for a SAT solver (Spear)
    '''
    
    def __init__(self):
        AbstractWrapper.__init__(self)
        
        self.parser.add_argument("--script", dest="script", required=True, help="simple script with only \"get_command_line_cmd(runargs, config)\" and \"process_results(self, filepointer, exit_code)\"")
        
        self.__loaded_script = None
       
    def get_command_line_args(self, runargs, config):
        '''
        Returns the command line call string to execute the target algorithm (here: Spear).
        Args:
            runargs: a map of several optional arguments for the execution of the target algorithm.
                    {
                      "instance": <instance>,
                      "specifics" : <extra data associated with the instance>,
                      "cutoff" : <runtime cutoff>,
                      "runlength" : <runlength cutoff>,
                      "seed" : <seed>
                    }
            config: a mapping from parameter name to parameter value
        Returns:
            A command call list to execute the target algorithm.
        '''
        ext_script = self.args.script
        if not os.path.isfile(ext_script):
            self._ta_status = "ABORT"
            self._ta_misc = "script is missing - should have been at %s." % (ext_script)
            self._exit_code = 1
            sys.exit(1)
        
        config = dict((name[1:], value) for name, value in config.items()) # remove leading "-" at parameter names
        self.__loaded_script = imp.load_source("misc", ext_script)
        self._return_value = self.__loaded_script.get_value(config)

        return ""
    
    def process_results(self, filepointer, exit_code):
        '''
        Parse a results file to extract the run's status (SUCCESS/CRASHED/etc) and other optional results.
    
        Args:
            filepointer: a pointer to the file containing the solver execution standard out.
            exit_code : exit code of target algorithm
        Returns:
            A map containing the standard AClib run results. The current standard result map as of AClib 2.06 is:
            {
                "status" : <"SAT"/"UNSAT"/"TIMEOUT"/"CRASHED"/"ABORT">,
                "runtime" : <runtime of target algrithm>,
                "quality" : <a domain specific measure of the quality of the solution [optional]>,
                "misc" : <a (comma-less) string that will be associated with the run [optional]>
            }
            ATTENTION: The return values will overwrite the measured results of the runsolver (if runsolver was used). 
        '''
        resultMap = {'status' : 'SUCCESS',
                     'quality' : self._return_value
                     }
        return resultMap
    
    
if __name__ == "__main__":
    wrapper = SimpleBlackBoxWrapper()
    wrapper.main()    
