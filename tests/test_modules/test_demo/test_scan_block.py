import shutil
import tempfile
import unittest

from scanpointgenerator import LineGenerator, CompoundGenerator

from malcolm.modules.demo.blocks import detector_block, motion_block, scan_block
from malcolm.core import Process
from malcolm.modules.scanning.util import DatasetType


class TestScanBlock(unittest.TestCase):

    def setUp(self):
        self.p = Process("proc")
        for c in detector_block("DETMRI", config_dir="/tmp") + \
                motion_block("MOTORSMRI", config_dir="/tmp") + \
                scan_block("SCANMRI", det="DETMRI", motors="MOTORSMRI",
                           config_dir="/tmp"):
            self.p.add_controller(c)
        self.p.start()
        self.b = self.p.block_view("SCANMRI")
        self.bd = self.p.block_view("DETMRI")
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        self.p.stop(timeout=2)
        shutil.rmtree(self.tmpdir)

    def prepare_half_run(self):
        linex = LineGenerator('x', 'mm', 0, 2, 3, alternate=True)
        liney = LineGenerator('y', 'mm', 0, 2, 2)
        compound = CompoundGenerator([liney, linex], [], [], 0.1)
        self.b.configure(
            compound, self.tmpdir, axesToMove=["x"],
            fileTemplate="my-%s.h5")

    def test_configure(self):
        self.prepare_half_run()
        assert list(self.b.datasets.value.rows()) == [
            ['DET.data', 'my-DET.h5', DatasetType.PRIMARY, 4, '/entry/data',
             '/entry/uid'],
            ['DET.sum', 'my-DET.h5', DatasetType.SECONDARY, 4, '/entry/sum',
             '/entry/uid']
        ]
        for b in (self.b, self.bd):
            assert b.completedSteps.value == 0
            assert b.configuredSteps.value == 3
            assert b.totalSteps.value == 6

    def test_run(self):
        self.prepare_half_run()
        assert self.b.state.value == "Armed"
        self.b.run()
        for b in (self.b, self.bd):
            assert b.completedSteps.value == 3
            assert b.configuredSteps.value == 6
            assert b.totalSteps.value == 6
            assert b.state.value == "Armed"
        self.b.run()
        for b in (self.b, self.bd):
            assert b.completedSteps.value == 6
            assert b.configuredSteps.value == 6
            assert b.totalSteps.value == 6
            assert b.state.value == "Finished"
        self.b.reset()
        for b in (self.b, self.bd):
            assert b.state.value == "Ready"