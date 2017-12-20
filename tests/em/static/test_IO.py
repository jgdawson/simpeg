from SimPEG import DC
from SimPEG import (Maps, Utils, DataMisfit, Regularization,
                    Optimization, Inversion, InvProblem, Directives)
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import unittest

try:
    from pymatsolver import Pardiso as Solver
except ImportError:
    from SimPEG import SolverLU as Solver


class TestsIO_2D(unittest.TestCase):

    def setUp(self):
        showIt = True
        np.random.seed(1)
        # Initiate I/O class for DC
        self.IO = DC.IO()
        # Obtain ABMN locations

        xmin, xmax = 0., 200.
        ymin, ymax = 0., 0.
        zmin, zmax = 0, 0
        self.endl = np.array([[xmin, ymin, zmin], [xmax, ymax, zmax]])
        # Generate DC survey object

    def test_flat_dpdp(self, showIt=False):
        self.survey = DC.Utils.gen_DCIPsurvey(
            self.endl, "dipole-dipole", dim=2, a=10, b=10, n=10
        )
        self.survey.getABMN_locations()
        self.survey = self.IO.from_ambn_locations_to_survey(
            self.survey.a_locations, self.survey.b_locations,
            self.survey.m_locations, self.survey.n_locations,
            'dipole-dipole', data_type='volt'
        )

        self.IO.plotPseudoSection()
        if showIt:
            plt.show()
        mesh, actind = self.IO.setMesh()

    def test_topo_dpdp(self, showIt=True):
        self.survey = DC.Utils.gen_DCIPsurvey(
            self.endl, "dipole-dipole", dim=2, a=10, b=10, n=10
        )
        self.survey.getABMN_locations()
        self.survey = self.IO.from_ambn_locations_to_survey(
            self.survey.a_locations, self.survey.b_locations,
            self.survey.m_locations, self.survey.n_locations,
            'dipole-dipole', data_type='volt'
        )
        self.IO.plotPseudoSection()
        if showIt:
            plt.show()
        mesh, actind = self.IO.setMesh()
        topo, mesh1D = DC.Utils.genTopography(mesh, -10, 0, its=100)
        mesh, actind = self.IO.setMesh(topo=np.c_[mesh1D.vectorCCx, topo])
        self.survey.drapeTopo(mesh, actind, option="top")
        if showIt:
            mesh.plotImage(actind)
            plt.plot(
                self.survey.electrode_locations[:, 0],
                self.survey.electrode_locations[:, 1], 'k.'
                )
            plt.show()

if __name__ == '__main__':
    unittest.main()