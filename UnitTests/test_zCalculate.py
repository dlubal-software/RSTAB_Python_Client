import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
from RSTAB.enums import OptimizeOnType, Optimizer
from RSTAB.initModel import Model, client
from RSTAB.Calculate.optimizationSettings import OptimizationSettings

if Model.clientModel is None:
    Model()

# CAUTION:
# These tests needs to be executed last because they change global settings

def test_optimization_settings():

    OptimizationSettings(True, 11, OptimizeOnType.E_OPTIMIZE_ON_TYPE_MIN_COST,
                         Optimizer.E_OPTIMIZER_TYPE_PERCENTS_OF_RANDOM_MUTATIONS,
                         0.3)
    opt_sett = OptimizationSettings.get()
    assert opt_sett.general_optimization_active
    assert opt_sett.general_keep_best_number_model_mutations == 11
    assert opt_sett.general_optimize_on == OptimizeOnType.E_OPTIMIZE_ON_TYPE_MIN_COST.name
    assert opt_sett.general_optimizer == Optimizer.E_OPTIMIZER_TYPE_PERCENTS_OF_RANDOM_MUTATIONS.name
    assert opt_sett.general_number_random_mutations == 0.3

    opt_sett.general_keep_best_number_model_mutations = 15
    OptimizationSettings.set(opt_sett)

    # Testing model is closed at the end of the testing session to enable easier and cleaned restart of the unit tests.
    client.service.close_model(0, False)
