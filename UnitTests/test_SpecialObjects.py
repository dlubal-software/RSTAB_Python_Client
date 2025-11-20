import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from RSTAB.initModel import Model
from RSTAB.BasicObjects.material import Material
from RSTAB.BasicObjects.node import Node
from RSTAB.BasicObjects.crossSection import CrossSection
from RSTAB.BasicObjects.member import Member
from RSTAB.SpecialObjects.structureModification import StructureModification
from RSTAB.TypesForMembers.memberStiffnessModification import MemberStiffnessModification

if Model.clientModel is None:
    Model()

def test_special_objects():
    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    # Create Material
    Material(1, 'S235')

    # Create Nodes
    Node(1, 0.0, 0.0, 0.0)
    Node(2, 0.0, 2.0, 0.0)
    Node(3, 2.0, 2.0, 0.0)
    Node(4, 2.0, 0.0, 0.0)
    Node(5, 0.0, 4.0, 0.0)
    Node(6, 2.0, 4.0, 0.0)

    Node(7, 0.0, 0.0, 1)
    Node(8, 0.0, 2.0, 1)
    Node(9, 2.0, 2.0, 1)
    Node(10, 2.0, 0.0, 1)
    Node(11, 0.0, 4.0, 1)
    Node(12, 2.0, 4.0, 1)

    CrossSection()
    Member(1,4, 9, 0, 1)

    MemberStiffnessModification()

    modify = StructureModification.modify_stiffness
    modify['modify_stiffnesses_materials'] = True
    StructureModification(1, modify, [StructureModification.material_item])

    Model.clientModel.service.finish_modification()

    structure_modification = Model.clientModel.service.get_structure_modification(1)
    assert structure_modification.modify_stiffnesses_materials == True
    assert structure_modification.modify_stiffnesses_cross_sections == False
