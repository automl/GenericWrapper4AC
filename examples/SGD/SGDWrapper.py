#!/usr/bin/env python2.7
# encoding: utf-8

'''
abstractBlackBoxWrapper -- abstract call for black box wrapper; get_value() is not implemented

@author:     Marius Lindauer, Chris Fawcett, Alex Fréchette, Frank Hutter
@copyright:  2014 AClib. All rights reserved.
@license:    GPL
@contact:    lindauer@informatik.uni-freiburg.de, fawcettc@cs.ubc.ca, afrechet@cs.ubc.ca, fh@informatik.uni-freiburg.de

example call (in aclib folder structure):
python src/generic_wrapper/braninWrapper.py --internal True dummy_instance "" 0.0 2147483647 1234 -x1  3.141592 -x2 2.275
'''

import sys
import re
import math
import logging

from genericWrapper4AC.generic_wrapper import AbstractWrapper

class SGDWrapper(AbstractWrapper):
    '''
        Simple wrapper for a SAT solver (Spear)
    '''
    
    def __init__(self):
        logging.basicConfig()
        AbstractWrapper.__init__(self)
        
        self._return_value = None
    
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
        cmd = "python examples/SGD/sgd_ta.py %s random_state %d " %(runargs["instance"], runargs["seed"])
        cmd += " ".join(["%s %s" %(name[1:], value) for name, value in config.items()]) 
        
        return cmd 
    
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
        
        self.logger.debug("reading solver results from %s" % (filepointer.name))
        try:
            out_ = str(filepointer.read().decode('UTF-8')).replace("\n","")
            print(out_)
            return_value = float(out_) # assumption that the SGD script will only print the accuracy value
            resultMap = {'status' : 'SUCCESS',
             'quality' : return_value
             }
        except ValueError:
            resultMap = {'status' : 'CRASHED',
             'quality' : 0
             }

        return resultMap

        
if __name__ == "__main__":
    wrapper = SGDWrapper()
    wrapper.main()    
