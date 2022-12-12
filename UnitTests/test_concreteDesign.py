import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

import pytest
from RSTAB.enums import *
from RSTAB.initModel import Model, CheckIfMethodOrTypeExists, SetAddonStatus
from RSTAB.BasicObjects.member import Member
from RSTAB.BasicObjects.node import Node
from RSTAB.BasicObjects.section import Section
from RSTAB.BasicObjects.material import Material
from RSTAB.TypesforConcreteDesign.ConcreteDurability import ConcreteDurability
#from RSTAB.ConcreteDesign.ConcreteUltimateConfigurations import ConcreteUltimateConfiguration
#from RSTAB.ConcreteDesign.ConcreteServiceabilityConfigurations import ConcreteServiceabilityConfiguration
from RSTAB.TypesforConcreteDesign.ConcreteEffectiveLength import ConcreteEffectiveLength

if Model.clientModel is None:
    Model()

# TODO: US-8087
@pytest.mark.skipif(CheckIfMethodOrTypeExists(Model.clientModel,'ns0:concrete_durability', True), reason="ns0:concrete_durability not in RSTAB GM yet")
def test_concrete_design():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    SetAddonStatus(Model.clientModel, AddOn.concrete_design_active)

    Material(1, 'C30/37')
    Material(2, 'B550S(A)')
    Section()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Member(1, 1, 2, 0, 1, 1)

    # Concrete Ultimate Configuration
    # ConcreteUltimateConfiguration(1, 'ULS', '1')

    # Concrete Serviceability Configuration
    #ConcreteServiceabilityConfiguration(1, 'SLS', '1')

    # Concrete Effective Lengths
    ConcreteEffectiveLength()

    Model.clientModel.service.finish_modification()
