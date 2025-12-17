import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir)
)
sys.path.append(PROJECT_ROOT)

from RSTAB.enums import NodalSupportType, NodalLoadDirection, AddOn, LoadWizardType, InitialStateDefintionType
from RSTAB.initModel import Model, SetAddonStatus
from RSTAB.BasicObjects.node import Node
from RSTAB.TypesForNodes.nodalSupport import NodalSupport
from RSTAB.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RSTAB.LoadCasesAndCombinations.loadCase import LoadCase
from RSTAB.LoadCasesAndCombinations.loadCasesAndCombinations import LoadCasesAndCombinations
from RSTAB.LoadCasesAndCombinations.stabilityAnalysisSettings import StabilityAnalysisSettings
from RSTAB.Loads.nodalLoad import NodalLoad

from RSTAB.LoadCasesAndCombinations.combinationWizard import CombinationWizard

if Model.clientModel is None:
    Model()

def test_combinationWizard():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    SetAddonStatus(Model.clientModel, addOn = AddOn.structure_stability_active, status = True)

    #Setting up the model to test the combination wizard
    Node(1, 0.0, 0.0, 0.0)
    Node(2, 5, 0.0, 0.0)

    NodalSupport(1, '1', NodalSupportType.FIXED)

    #setting up the loading of the model, with differnet loading cases and calculatiion settings
    StaticAnalysisSettings.GeometricallyLinear(1, "Linear")
    LoadCasesAndCombinations({
                    "current_standard_for_combination_wizard": 6207,
                    "combination_wizard_and_classification_active": True,
                    "combination_wizard_active": True,
                    "result_combinations_active": False,
                    "result_combinations_parentheses_active": False,
                    "result_combinations_consider_sub_results": False,
                    "combination_name_according_to_action_category": False
                 },
                 model= Model)

    LoadCase(1, 'Self-Weight', [True, 0.0, 0.0,1.0])
    NodalLoad(1, 1, '2', NodalLoadDirection.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W, 1000)

    StabilityAnalysisSettings()
    #setting up the combination wizard for load combinations
    CombinationWizard(1, 'Wizard 1', 1, 1, False, False, [[1, InitialStateDefintionType.DEFINITION_TYPE_FINAL_STATE]], None, True, True, True)

    #going through each setting of the combination wizard

    config = Model.clientModel.service.get_combination_wizard(1)

    assert config.no == 1
    assert config.name == 'Wizard 1'
    assert config.generate_combinations == LoadWizardType.GENERATE_LOAD_COMBINATIONS.name
    assert config.static_analysis_settings == 1
    assert config.has_stability_analysis == True
    assert config.stability_analysis_settings == 1

    CombinationWizard.SetResultCombination(2, 'Wizard 2', None, None, False, False, False, False, 'This is wizard no. 2',)

    Model.clientModel.service.finish_modification()

    config = Model.clientModel.service.get_combination_wizard(2)
    assert config.no == 2
    assert config.generate_combinations == LoadWizardType.GENERATE_RESULT_COMBINATIONS.name
    assert config.generate_subcombinations_of_type_superposition == False
    assert config.user_defined_action_combinations == False
    assert config.comment == 'This is wizard no. 2'
