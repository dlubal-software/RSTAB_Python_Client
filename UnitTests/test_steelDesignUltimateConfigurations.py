import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir)
)
sys.path.append(PROJECT_ROOT)

from RSTAB.enums import AddOn, NodalSupportType
from RSTAB.initModel import Model, SetAddonStatus
from RSTAB.BasicObjects.material import Material
from RSTAB.BasicObjects.crossSection import CrossSection
from RSTAB.BasicObjects.node import Node
from RSTAB.BasicObjects.member import Member
from RSTAB.TypesForNodes.nodalSupport import NodalSupport
from RSTAB.SteelDesign.steelUltimateConfigurations import SteelDesignUltimateConfigurations

if Model.clientModel is None:
    Model()

def test_SteelDesignUltimateConfigurations():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    SetAddonStatus(Model.clientModel, addOn=AddOn.steel_design_active, status=True)

    Material(1, 'S235')

    CrossSection(1, 'IPE 200')

    Node(1, 0.0, 0.0, 0.0)
    Node(2, 5, 0.0, 0.0)

    Member(1, 1, 2, 0.0, 1, 1)

    NodalSupport(1, '1', NodalSupportType.FIXED)

    SteelDesignUltimateConfigurations(1, name="myConfig")

    Model.clientModel.service.finish_modification()

    config = Model.clientModel.service.get_steel_design_uls_configuration(1)

    assert config.name == "myConfig"
    assert config.assigned_to_all_members == True

