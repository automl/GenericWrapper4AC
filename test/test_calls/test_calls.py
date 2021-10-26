import tempfile
import unittest
import sys
import os
import copy

from examples.MiniSAT.MiniSATWrapper import MiniSATWrapper
from examples.SGD.SGDWrapper import SGDWrapper
from examples.dummy_wrapper.dummy_wrapper import DummyWrapper
from genericWrapper4AC.data.data import Data


class TestCalls(unittest.TestCase):

    def setUp(self):
        self.runsolver = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "test_binaries", "runsolver")

    def test_minisat_old(self):

        wrapper = MiniSATWrapper()

        sys.argv = "examples/MiniSAT/SATCSSCWrapper.py examples/MiniSAT/gzip_vc1071.cnf SAT 10 0 42 -rnd-freq 0 -var-decay 0.001 -cla-decay 0.001 -gc-frac 0.000001 -rfirst 1000"
        sys.argv += " --runsolver-path " + self.runsolver
        sys.argv = sys.argv.split(" ")

        wrapper.main(exit=False)

        self.assertEqual(wrapper.data.status, "SUCCESS")
        self.assertGreater(2, wrapper.data.time)
        self.assertEqual(wrapper.data.seed, 42)
        self.assertEqual(wrapper.data.runlength, 0)
        self.assertFalse(wrapper.data.new_format)
        
    def test_minisat_new(self):

        wrapper = MiniSATWrapper()

        sys.argv = "python examples/MiniSAT/SATCSSCWrapper.py --instance examples/MiniSAT/gzip_vc1071.cnf --cutoff 10 --seed 42 --config -rnd-freq 0 -var-decay 0.001 -cla-decay 0.001 -gc-frac 0.000001 -rfirst 1000"
        sys.argv += " --runsolver-path " + self.runsolver
        sys.argv = sys.argv.split(" ")

        wrapper.main(exit=False)

        self.assertEqual(wrapper.data.status, "SUCCESS")
        self.assertGreater(2, wrapper.data.time)
        self.assertEqual(wrapper.data.seed, 42)
        # important hack for irace that cost and time is equal
        # if cost was not set
        self.assertEqual(wrapper.data.cost, wrapper.data.time)
        self.assertIsNone(wrapper.data.runlength)
        self.assertTrue(wrapper.data.new_format)
        
    def test_sgd_old(self):

        wrapper = SGDWrapper()

        sys.argv = "examples/SGD/SGDWrapper.py train 0 5 0 9 -learning_rate constant -eta0 1 -loss hinge -penalty l2 -alpha 0.0001 -learning_rate optimal -eta0 0.0 -n_iter 2"
        sys.argv += " --runsolver-path " + self.runsolver
        sys.argv = sys.argv.split(" ")

        wrapper.main(exit=False)

        self.assertEqual(wrapper.data.status, "SUCCESS")
        self.assertGreater(2, wrapper.data.time)
        self.assertGreater(1, wrapper.data.cost)
        # the irace hack should not change the results 
        # for set cost values
        self.assertNotEqual(wrapper.data.cost, wrapper.data.time)
        self.assertEqual(wrapper.data.seed, 9)
        self.assertEqual(wrapper.data.runlength, 0)
        self.assertFalse(wrapper.data.new_format)

    def test_sgd_new(self):

        wrapper = SGDWrapper()

        sys.argv = "examples/SGD/SGDWrapper.py --instance train --seed 9 --config -learning_rate constant -eta0 1 -loss hinge -penalty l2 -alpha 0.0001 -learning_rate optimal -eta0 0.0 -n_iter 2"
        sys.argv += " --runsolver-path " + self.runsolver
        sys.argv = sys.argv.split(" ")

        wrapper.main(exit=False)

        self.assertEqual(wrapper.data.status, "SUCCESS")
        self.assertGreater(2, wrapper.data.time)
        self.assertGreater(1, wrapper.data.cost)
        # the irace hack should not change the results 
        # for set cost values
        self.assertNotEqual(wrapper.data.cost, wrapper.data.time)
        self.assertEqual(wrapper.data.seed, 9)
        self.assertTrue(wrapper.data.new_format)

    def test_dummy(self):
        wrapper = DummyWrapper()

        d = self.get_data(status="SUCCESS", exit_code=0, new_format=False)

        sys.argv = f"examples/dummy_wrapper/dummy_wrapper.py {d.instance} {d.specifics} {d.cutoff} 0 {d.seed} -cost {d.cost} -runtime {d.time}"
        sys.argv += " --runsolver-path " + self.runsolver
        sys.argv = sys.argv.split(" ")

        wrapper.main(exit=False)

        self.assert_equal_data(d, wrapper.data)

    def test_tmp_dir(self):
        wrapper = DummyWrapper()

        d = self.get_data()

        with tempfile.TemporaryDirectory(prefix="GenericWrapper4AC_test_") as tmp_dir:
            missing_dir_path = os.path.join(tmp_dir, "default")
            sys.argv = f"examples/dummy_wrapper/dummy_wrapper.py --temp-file-dir {missing_dir_path} {d.instance} {d.specifics} {d.cutoff} 0 {d.seed} -cost {d.cost} -runtime {d.time}"
            sys.argv += " --runsolver-path " + self.runsolver
            sys.argv = sys.argv.split(" ")

            wrapper.main(exit=False)

        d.status = "ABORT"
        d.exit_code = 1
        d.time = d.cutoff
        d.cost = Data().cost
        self.assert_equal_data(d, wrapper.data)

    @staticmethod
    def get_data(**kwargs):
        d = Data()
        d.instance = "cost+time"
        d.specifics = "abc"
        d.cutoff = 10
        d.seed = 0
        d.cost = 1.1
        d.time = 1.2
        for k, v in kwargs.items():
            setattr(d, k, v)
        return d

    def assert_equal_data(self, expected, actual):
        self.assertEqual(expected.status, actual.status)
        self.assertEqual(expected.exit_code, actual.exit_code)
        self.assertEqual(expected.instance, actual.instance)
        self.assertEqual(expected.specifics, actual.specifics)
        self.assertEqual(expected.cutoff, actual.cutoff)
        self.assertEqual(expected.seed, actual.seed)
        self.assertEqual(expected.cost, actual.cost)
        self.assertEqual(expected.time, actual.time)
        self.assertEqual(expected.new_format, actual.new_format)
