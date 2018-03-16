import unittest
import sys
import os

import genericWrapper4AC
from genericWrapper4AC.generic_wrapper import AbstractWrapper
from genericWrapper4AC.data.data import Data


class TestRessourceLimits(unittest.TestCase):

    def test_memlimit(self):

        wrapper = AbstractWrapper()

        data = Data()

        wrapper.data = data
        data.tmp_dir = "."
        data.runsolver = os.path.join(genericWrapper4AC.__path__[
            0], "binaries", "runsolver")
        data.mem_limit = 50  # mb
        data.cutoff = 100000

        target_cmd = "python test/test_resources/mem_str.py"

        wrapper.call_target(target_cmd)

        wrapper.read_runsolver_output()

        wrapper._watcher_file.close()
        wrapper._solver_file.close()
        os.remove(wrapper._watcher_file.name)
        os.remove(wrapper._solver_file.name)

        self.assertEqual(wrapper.data.status, "TIMEOUT")
        self.assertEqual(wrapper.data.additional, " memory limit was exceeded")

    def test_timelimit(self):

        wrapper = AbstractWrapper()

        data = Data()

        wrapper.data = data
        data.tmp_dir = "."
        data.runsolver = os.path.join(genericWrapper4AC.__path__[
            0], "binaries", "runsolver")
        data.mem_limit = 500  # mb
        data.cutoff = 1

        target_cmd = "python test/test_resources/pi.py"

        wrapper.call_target(target_cmd)

        wrapper.read_runsolver_output()

        self.assertEqual(wrapper.data.status, "TIMEOUT")
        self.assertNotEqual(wrapper.data.additional,
                            " memory limit was exceeded")

        wrapper._watcher_file.close()
        wrapper._solver_file.close()
        os.remove(wrapper._watcher_file.name)
        os.remove(wrapper._solver_file.name)

    def test_nolimit(self):

        wrapper = AbstractWrapper()

        data = Data()

        wrapper.data = data
        data.tmp_dir = "."
        data.runsolver = os.path.join(genericWrapper4AC.__path__[
            0], "binaries", "runsolver")
        data.mem_limit = 500  # mb
        data.cutoff = 5

        target_cmd = "time"

        wrapper.call_target(target_cmd)

        wrapper.read_runsolver_output()

        # since there was no timeout/memout
        # the status is still on its default: CRASHED
        self.assertEqual(wrapper.data.status, "CRASHED")
        self.assertNotEqual(wrapper.data.additional,
                            " memory limit was exceeded")

        wrapper._watcher_file.close()
        wrapper._solver_file.close()
        os.remove(wrapper._watcher_file.name)
        os.remove(wrapper._solver_file.name)
