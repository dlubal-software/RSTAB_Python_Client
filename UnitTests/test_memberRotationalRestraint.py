import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from RSTAB.initModel import Model, SetAddonStatus
from RSTAB.enums import AddOn
from RSTAB.TypesForMembers.memberRotationalRestraint import MemberRotationalRestraint

if Model.clientModel is None:
    Model()

def test_memberRotationalRestraint():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    SetAddonStatus(Model.clientModel, AddOn.aluminum_design_active)
    SetAddonStatus(Model.clientModel, AddOn.timber_design_active)
    SetAddonStatus(Model.clientModel, AddOn.steel_design_active)

    MemberRotationalRestraint.Continuous(1, beam_spacing= 2.5)
    MemberRotationalRestraint.Discrete(2, purlin_spacing= 1.5)
    MemberRotationalRestraint.Manually(3, rotational_spring_stiffness= 2500)

    Model.clientModel.service.finish_modification()

    mrr1 = Model.clientModel.service.get_member_rotational_restraint(1)
    assert mrr1.no == 1
    assert mrr1.beam_spacing == 2.5

    mrr2 = Model.clientModel.service.get_member_rotational_restraint(2)
    assert mrr2.purlin_spacing == 1.5

    mrr3 = Model.clientModel.service.get_member_rotational_restraint(3)
    assert mrr3.type == 'TYPE_MANUALLY'
    assert mrr3.total_rotational_spring_stiffness == 2500
