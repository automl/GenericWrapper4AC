#!/usr/bin/env python2.7
# encoding: utf-8

'''
SATCSSCWrapper -- target algorithm wrapper for SAT solvers

@author:     Marius Lindauer
@copyright:  2016 Ml4AAD. All rights reserved.
@license:    BSD
@contact:    lindauer@informatik.uni-freiburg.de
'''

import sys
import re
import os
import imp
import logging
from subprocess import Popen, PIPE

from genericWrapper4AC.generic_wrapper import AbstractWrapper

class SatWrapper(AbstractWrapper):
    '''
        General wrapper for a SAT solver
    '''
    
    def __init__(self):
        '''
            Constructor
        '''
        logging.basicConfig()
        AbstractWrapper.__init__(self)
        
        self.parser.add_argument("--script", dest="cssc_script", required=True, help="simple cssc script with only \"get_command_line_cmd(runargs, config)\"")
        self.parser.add_argument("--sol-file", dest="solubility_file", default=None, help="File with \"<instance> {SATISFIABLE|UNSATISFIABLE|UNKNOWN}\" ")
        self.parser.add_argument("--sat-checker", dest="sat_checker", default=None, help="binary of SAT checker")

        self.__instance = ""
        self.__cmd = ""
        
        self._FAILED_FILE = "failed_runs.txt"  # in self._tmp_dir
        
        self.inst_specific = None
        
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
                      "seed" : <seed>,
                      "tmp" : directory for temporary files (only available if --temp-file-dir-algo was used)
                    }
            config: a mapping from parameter name to parameter value
        Returns:
            A command call list to execute the target algorithm.
        '''
        
        self.inst_specific = runargs["specifics"]
        
        ext_script = self.args.cssc_script
        if not os.path.isfile(ext_script):
            self._ta_status = "ABORT"
            self._ta_misc = "cssc script is missing - should have been at %s." % (ext_script)
            self._exit_code = 1
            sys.exit(1)
        
        loaded_script = imp.load_source("cssc", ext_script)
        
        
        cmd = loaded_script.get_command_line_cmd(runargs, config)

        # remember instance and cmd to verify the result later on
        self.__instance = runargs["instance"] 
        self.__cmd = cmd

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
        data = str(filepointer.read())
        resultMap = {}
        
        if re.search('UNSATISFIABLE', data):
            resultMap['status'] = 'UNSAT'
            
            # verify UNSAT via external knowledge
            if self.inst_specific in ["SAT", "UNSAT"] and  self.inst_specific == "SAT":
                resultMap['status'] = 'CRASHED'
                resultMap['misc'] = "Instance is SAT but UNSAT was reported"
            elif not self.args.solubility_file:
                resultMap['misc'] = "solubility file was not given; could not verify UNSAT" 
            elif not os.path.isfile(self.args.solubility_file):
                resultMap['misc'] = "have not found %s; could not verify UNSAT" % (self.args.solubility_file)
            elif not self._verify_UNSAT():
                resultMap['status'] = 'CRASHED'
                resultMap['misc'] = "Instance is SAT but UNSAT was reported"
                # save command line call
                failed_file = os.path.join(self._tmp_dir, self._FAILED_FILE) 
                with open(failed_file, "a") as fp:
                    fp.write(self.__cmd + "\n")
                    fp.flush()
            if(self._specifics == "SATISFIABLE" or self._specifics == "10"):
                resultMap['status'] = 'CRASHED'
                resultMap['misc'] = "SOLVER BUG: instance is SATISFIABLE but solver claimed it is UNSATISFIABLE"
        elif re.search('SATISFIABLE', data):
            resultMap['status'] = 'SAT'
               
            # look for model
            model = None
            for line in data.split("\n"):
                if line.startswith("v "):
                    model = map(int, line.split(" ")[1:-1])
                    break

            # verify SAT
            if self.inst_specific in ["SAT", "UNSAT"] and  self.inst_specific == "UNSAT":
                resultMap['status'] = 'CRASHED'
                resultMap['misc'] = "Instance is UNSAT but SAT was reported"
            elif not self.args.sat_checker:
                resultMap['misc'] = "SAT checker was not given; could not verify SAT"
            elif not os.path.isfile(self.args.sat_checker):
                resultMap['misc'] = "have not found %s; could not verify SAT" % (self.args.sat_checker)
            elif model is None:
                resultMap['misc'] = "print of solution was probably incomplete because of runsolver SIGTERM/SIGKILL"
                resultMap['status'] = 'TIMEOUT'
            elif not self._verify_SAT(model, filepointer):
                # fix: race condiction between SIGTERM of runsolver and print of solution
                if self._ta_status == "TIMEOUT":
                    resultMap['status'] = 'TIMEOUT'
                    resultMap['misc'] = 'print of solution was probably incomplete because of runsolver SIGTERM/SIGKILL'
                else:
                    resultMap['status'] = 'CRASHED'
                    resultMap['misc'] = "SOLVER BUG: solver returned a wrong model"
                    # save command line call
                    failed_file = os.path.join(self._tmp_dir, self._FAILED_FILE) 
                    with open(failed_file, "a") as fp:
                        fp.write(self.__cmd + "\n")
                        fp.flush()
         
            if(self._specifics == "UNSATISFIABLE" or self._specifics == "20"):
                resultMap['status'] = 'CRASHED'
                resultMap['misc'] = "SOLVER BUG: instance is UNSATISFIABLE but solver claimed it is SATISFIABLE"
            
        elif re.search('s UNKNOWN', data):
            resultMap['status'] = 'TIMEOUT'
            resultMap['misc'] = "Found s UNKNOWN line - interpreting as TIMEOUT"
        elif re.search('INDETERMINATE', data):
            resultMap['status'] = 'TIMEOUT'
            resultMap['misc'] = "Found INDETERMINATE line - interpreting as TIMEOUT"
        
        return resultMap
    
    def _verify_SAT(self, model, solver_output):
        '''
            verifies the model for self.__instance 
            Args:
                model : list with literals
                solver_output: filepointer to solver output
            Returns:
                True if model was correct
                False if model was not correct
        '''
        cmd = [self.args.sat_checker, self.__instance, solver_output.name]
        io = Popen(cmd, stdout=PIPE)
        out_, err_ = io.communicate()
        for line in out_.split("\n"):
            if "Solution verified" in line:
                self.logger.debug("Solution verified")
                return True
            elif "Wrong solution" in line:
                return False
        return True  # should never happen

    def _verify_UNSAT(self):
        '''
            looks in <self.args.solubility_file> whether it is already known that the instance is UNSAT
            Returns:
                False if the instance is known as SAT
                True otherwise
        '''
        
        with open(self.args.solubility_file) as fp:
            for line in fp:
                if line.startswith(self.__instance):
                    line = line.strip("\n")
                    status = line.split(" ")[1]
                    if status == "SATISFIABLE":
                        return False
                    else:
                        return True
        return True
        

if __name__ == "__main__":
    wrapper = SatCSSCWrapper()
    wrapper.main()    
