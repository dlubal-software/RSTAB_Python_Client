#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from RSTAB.initModel import Model
from RSTAB.LoadCasesAndCombinations.loadCase import LoadCase
from RSTAB.LoadCasesAndCombinations.loadCasesAndCombinations import LoadCasesAndCombinations
from RSTAB.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RSTAB.LoadCasesAndCombinations.designSituation import DesignSituation
from RSTAB.LoadCasesAndCombinations.modalAnalysisSettings import ModalAnalysisSettings
from RSTAB.LoadCasesAndCombinations.spectralAnalysisSettings import SpectralAnalysisSettings
from RSTAB.LoadCasesAndCombinations.combinationWizard import CombinationWizard
from RSTAB.DynamicLoads.responseSpectrum import ResponseSpectrum
from RSTAB.LoadCasesAndCombinations.resultCombination import ResultCombination
from RSTAB.enums import DesignSituationType, InitialStateDefintionType
from RSTAB.enums import ResultCombinationType, OperatorType, ActionLoadType, ResultCombinationExtremeValueSign


if Model.clientModel is None:
    Model()

def test_design_situation():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    LoadCase()

    LoadCasesAndCombinations(params={"current_standard_for_combination_wizard": 6048,
                                      "combination_wizard_and_classification_active": True,
                                      "combination_wizard_active": True,
                                      "result_combinations_active": True,
                                      "result_combinations_parentheses_active": True,
                                      "result_combinations_consider_sub_results": True,
                                      "combination_name_according_to_action_category": True})

    StaticAnalysisSettings.SecondOrderPDelta(1, 'Second Order P Delta')

    StaticAnalysisSettings.GeometricallyLinear(2, "Analyse statique geometriquement lineaire")

    ModalAnalysisSettings(1, "Analyse Lanczos 300 Modes")

    SpectralAnalysisSettings(1, 'SRSS | SRSS')

    ResponseSpectrum(1, 'Responce Spect.', user_defined_spectrum=[[0, 0.66], [0.15, 1.66]])

    CombinationWizard(no=1, name = 'Analyse statique du second ordre',
                      static_analysis_settings = 1,
                      stability_analysis_setting = 0,
                      consider_imperfection_case = True,
                      generate_same_CO_without_IC = False,
                      initial_state_cases = [[1,InitialStateDefintionType.DEFINITION_TYPE_FINAL_STATE]],
                      structure_modification = 0)

    CombinationWizard.SetResultCombination(no = 3, name = 'Combinaisons de resultats',
                                           stability_analysis_setting = 0,
                                           consider_imperfection_case = True,
                                           generate_same_CO_without_IC = False,
                                           user_defined_action_combinations = False,
                                           favorable_permanent_actions = False,
                                           generate_subcombinations_of_type_superposition = False)

    ResultCombination(no = 1, design_situation = 4,
                      combination_type = ResultCombinationType.COMBINATION_TYPE_GENERAL,
                      combination_items = [[1, OperatorType.OPERATOR_NONE, 1.0, ActionLoadType.LOAD_TYPE_PERMANENT]],
                      generate_subcombinations = False,
                      srss_combination = [False, ResultCombinationExtremeValueSign.EXTREME_VALUE_SIGN_POSITIVE_OR_NEGATIVE],
                      name = 'Combinaison de resultats sismiques')

    DesignSituation(no = 1, design_situation_type = DesignSituationType.DESIGN_SITUATION_TYPE_STR_PERMANENT_AND_TRANSIENT_6_10, active = True, params = {'combination_wizard': 1})
    DesignSituation(no = 2, design_situation_type = DesignSituationType.DESIGN_SITUATION_TYPE_SLS_CHARACTERISTIC, active = True, params = {'combination_wizard': 1})
    DesignSituation(no = 3, design_situation_type = DesignSituationType.DESIGN_SITUATION_TYPE_SEISMIC_MASS, active = True, params = {'combination_wizard': 1})
    DesignSituation(no = 4, design_situation_type = DesignSituationType.DESIGN_SITUATION_TYPE_STR_SEISMIC, active = True, params = {'combination_wizard': 3})
    DesignSituation(no = 5, design_situation_type = DesignSituationType.DESIGN_SITUATION_TYPE_STR_ACCIDENTAL_PSI_2_1, active = True, params = {'combination_wizard': 1})

    Model.clientModel.service.finish_modification()
