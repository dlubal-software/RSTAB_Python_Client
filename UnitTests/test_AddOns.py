import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
from RSTAB.enums import AddOn
from RSTAB.initModel import Model, SetAddonStatus, GetAddonStatus

if Model.clientModel is None:
    Model()

def test_AddOns():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()
    SetAddonStatus(Model.clientModel, AddOn.structure_stability_active, True)
    SetAddonStatus(Model.clientModel, AddOn.concrete_design_active, True)
    SetAddonStatus(Model.clientModel, AddOn.modal_active, True)
    #SetAddonStatus(Model.clientModel, AddOn.building_model_active, True)               :   Add-Ons greyed out in RFEM GUI. Assumedly still WIP
    SetAddonStatus(Model.clientModel, AddOn.stress_analysis_active, True)
    SetAddonStatus(Model.clientModel, AddOn.steel_design_active, True)
    SetAddonStatus(Model.clientModel, AddOn.timber_design_active, True)
    SetAddonStatus(Model.clientModel, AddOn.aluminum_design_active, True)
    #SetAddonStatus(Model.clientModel, AddOn.timber_joints_active, True)                :   Add-Ons greyed out in RFEM GUI. Assumedly still WIP
    #SetAddonStatus(Model.clientModel, AddOn.craneway_design_active, True)              :   Add-Ons greyed out in RFEM GUI. Assumedly still WIP
    #SetAddonStatus(Model.clientModel, AddOn.material_nonlinear_analysis_active, True)  :   Add-Ons greyed out in RFEM GUI. Assumedly still WIP
    #SetAddonStatus(Model.clientModel, AddOn.construction_stages_active, True)          :   Add-Ons greyed out in RFEM GUI. Assumedly still WIP
    #SetAddonStatus(Model.clientModel, AddOn.time_dependent_active, True)
    #SetAddonStatus(Model.clientModel, AddOn.form_finding_active, True)
    #SetAddonStatus(Model.clientModel, AddOn.influence_lines_areas_active, True)        :   Add-Ons greyed out in RFEM GUI. Assumedly still WIP
    SetAddonStatus(Model.clientModel, AddOn.torsional_warping_active, True)
    SetAddonStatus(Model.clientModel, AddOn.cost_estimation_active, True)
    #SetAddonStatus(Model.clientModel, AddOn.time_history_active, True)                 :   Add-Ons greyed out in RFEM GUI. Assumedly still WIP
    #SetAddonStatus(Model.clientModel, AddOn.pushover_active, True)                     :   Add-Ons greyed out in RFEM GUI. Assumedly still WIP
    #SetAddonStatus(Model.clientModel, AddOn.harmonic_response_active, True)            :   Add-Ons greyed out in RFEM GUI. Assumedly still WIP
    # SetAddonStatus(Model.clientModel, AddOn.geotechnical_analysis_active, True)
	#SetAddonStatus(Model.clientModel, AddOn.tower_wizard_active, True)                 :   Add-Ons greyed out in RFEM GUI. Assumedly still WIP
	#SetAddonStatus(Model.clientModel, AddOn.tower_equipment_wizard_active, True)       :   Add-Ons greyed out in RFEM GUI. Assumedly still WIP
	#SetAddonStatus(Model.clientModel, AddOn.piping_active, True)                       :   Add-Ons greyed out in RFEM GUI. Assumedly still WIP
	#SetAddonStatus(Model.clientModel, AddOn.air_cushions_active, True)                 :   Add-Ons greyed out in RFEM GUI. Assumedly still WIP

    Model.clientModel.service.finish_modification()

    assert GetAddonStatus(Model.clientModel, AddOn.structure_stability_active)
    assert GetAddonStatus(Model.clientModel, AddOn.concrete_design_active)
    assert GetAddonStatus(Model.clientModel, AddOn.modal_active)
    assert GetAddonStatus(Model.clientModel, AddOn.stress_analysis_active)
    assert GetAddonStatus(Model.clientModel, AddOn.steel_design_active)
    assert GetAddonStatus(Model.clientModel, AddOn.timber_design_active)
    assert GetAddonStatus(Model.clientModel, AddOn.aluminum_design_active)
    assert GetAddonStatus(Model.clientModel, AddOn.torsional_warping_active)
    assert GetAddonStatus(Model.clientModel, AddOn.cost_estimation_active)
