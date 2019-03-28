from __future__ import print_function
import os
import sys
if sys.version_info >= (3,):
    import pickle
else:
    import cPickle as pickle
import numpy as np
from bioen import optimize
import pytest


# relative tolerance for value comparison
#tol = 1.e-14
tol = 5.e-14
tol_min = 1.e-1

verbose = False
create_reference_values = False


filenames = [
    "./data/data_deer_test_forces_M808xN10.pkl",
    "./data/data_forces_M64xN64.pkl"
]


def available_tests():
    exp = {}

    if (optimize.util.library_gsl()):
        exp['GSL'] = { 'bfgs2':{}  }

    if (optimize.util.library_lbfgs()):
        exp['LBFGS'] = { 'lbfgs':{} }

    return exp


def run_test_error_forces(file_name=filenames[0], caching=False):

    print("=" * 80)

    if (create_reference_values):
        os.environ["OMP_NUM_THREADS"] = "1"

    if "OMP_NUM_THREADS" in os.environ:
        print(" OPENMP NUM. THREADS = ", os.environ["OMP_NUM_THREADS"])

    exp = available_tests()

    # load exp. data from file
    with open(file_name, 'rb') as ifile:
        [forces_init, w0, y, yTilde, YTilde, theta] = pickle.load(ifile)

    for minimizer in exp:
        for algorithm in exp[minimizer]:

            params = optimize.minimize.Parameters(minimizer)
            params['cache_ytilde_transposed'] = caching
            params['use_c_functions'] = True
            params['algorithm'] = algorithm
            params['verbose'] = verbose


            if params['minimizer'] == "gsl":
                #  Force an error by defining a wrong parameter
                params['algorithm'] = "TEST_INVALID"
                #params['params']['step_size'] = -1.00001

                # print (params['params'])
            elif params['minimizer'] == "lbfgs":
                #  Force an error by defining a wrong parameter
                params['params']['delta'] = -1.

            if verbose:
                print("-" * 80)
                print("", params)

            with pytest.raises(RuntimeError) as excinfo:
                wopt, yopt, forces, fmin_ini, fmin_fin, chiSqr, S = \
                    optimize.forces.find_optimum(forces_init, w0, y, yTilde, YTilde, theta, params)

            print(excinfo.value)
            assert('return code' in str(excinfo.value))



def test_error_opt_forces():
    """Entry point for py.test."""
    print("")
    optimize.minimize.set_fast_openmp_flag(0)
    for file_name in filenames:
        caching = ["False"]
        run_test_error_forces(file_name=file_name, caching=caching)