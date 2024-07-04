import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

# Import the relevant Libraries
from RSTAB.enums import ObjectTypes
from RSTAB.initModel import CheckIfMethodOrTypeExists, Model
from RSTAB.BasicObjects.material import Material
from RSTAB.BasicObjects.section import Section
from RSTAB.BasicObjects.node import Node
from RSTAB.BasicObjects.member import Member
from RSTAB.Tools.centreOfGravityAndObjectInfo import ObjectsInfo
from math import sqrt
import pytest

if Model.clientModel is None:
    Model()

# pytestmark sets same parameters (in this case skipif) to all functions in the module or class
# TODO: US-8142
# pytestmark = pytest.mark.skipif(CheckIfMethodOrTypeExists(Model.clientModel,'ns0:array_of_get_center_of_gravity_and_objects_info_elements_type', True),
#              reason="ns0:array_of_get_center_of_gravity_and_objects_info_elements_type not in RSTAB GM yet")

def test_center_of_gravity():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    x1, y1, z1, = 0, 0, 0
    x2, y2, z2 = 4, 10, -6
    Node(1, x1, y1, z1)
    Node(2, x2, y2, z2)
    Material(1, 'S235')
    Section()
    Member(1, start_node_no= 1, end_node_no= 2)

    Model.clientModel.service.finish_modification()

    CoG_X = (x2 - x1) / 2
    CoG_Y = (y2 - y1) / 2
    CoG_Z = (z2 - z1) / 2

    cog = ObjectsInfo.CenterofGravity([[ObjectTypes.E_OBJECT_TYPE_MEMBER, 1]])

    assert cog['Center of gravity coordinate X'] == CoG_X
    assert cog['Center of gravity coordinate Y'] == CoG_Y
    assert cog['Center of gravity coordinate Z'] == CoG_Z

def test_member_information():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    x1, y1, z1, = 0, 0, 0
    x2, y2, z2 = 4, 10, -6
    Node(1, x1, y1, z1)
    Node(2, x2, y2, z2)
    Material(1, 'S235')
    Section()
    Member(1, start_node_no= 1, end_node_no= 2)

    Model.clientModel.service.finish_modification()

    L = sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    A = 53.80 / (100 * 100)
    V = L * A
    M = (V * 7850) / 1000

    info = ObjectsInfo.MembersInfo([[ObjectTypes.E_OBJECT_TYPE_MEMBER, 1]])

    assert info['Length of members'] == round(L,3)
    assert info['Volume'] == round(V,3)
    assert info['Mass'] == round(M,3)

