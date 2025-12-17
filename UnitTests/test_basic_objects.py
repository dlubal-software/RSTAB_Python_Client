import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
from RSTAB.enums import SetType, MemberType
from RSTAB.initModel import Model
from RSTAB.BasicObjects.material import Material
from RSTAB.BasicObjects.crossSection import CrossSection
from RSTAB.BasicObjects.node import Node
from RSTAB.BasicObjects.member import Member
from RSTAB.BasicObjects.memberSet import MemberSet

if Model.clientModel is None:
    Model()

def test_material():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Material(1, 'S235')

    Model.clientModel.service.finish_modification()

    material = Model.clientModel.service.get_material(1)
    assert material.no == 1
    assert material.name == 'S235 | EN 1993-1-1:2005-05'

def test_node_init():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 2, 0, 0)

    node = Model.clientModel.service.get_node(1)

    Model.clientModel.service.finish_modification()

    assert node.no == 1
    assert node.coordinate_1 == 2

def test_section():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Material(1, 'S235')
    CrossSection(1, 'IPE 300')

    Model.clientModel.service.finish_modification()

    section = Model.clientModel.service.get_cross_section(1)

    assert section.no == 1
    assert section.name == 'IPE 300 | -- | British Steel'

def test_member_init():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')

    CrossSection(1, 'IPE 300', 1)

    Member(1,  1, 2, 0, 1, 1)

    Model.clientModel.service.finish_modification()

    member = Model.clientModel.service.get_member(1)

    assert member.analytical_length == 5
    assert member.cross_section_start == 1

def test_member_set():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)
    Node(3, 10, 0, 0)

    Material(1, 'S235')

    CrossSection(1, 'IPE 300', 1)

    Member(1, 1, 2, 0, 1, 1)
    Member(2, 2, 3, 0, 1, 1)

    MemberSet(1, '1 2', SetType.SET_TYPE_GROUP)

    Model.clientModel.service.finish_modification()

    member_set = Model.clientModel.service.get_member_set(1)

    assert member_set.members == '1 2'
    assert member_set.length == 10

def test_member_delete():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)
    Node(3, 10, 0, 0)

    Material(1, 'S235')

    CrossSection(1, 'IPE 300', 1)

    Member(1, 1, 2, 0, 1, 1)
    Member(2, 2, 3, 0, 1, 1)

    Member.DeleteMember('1')

    Model.clientModel.service.finish_modification()

    modelInfo = Model.clientModel.service.get_model_info()

    assert modelInfo.property_member_count == 1

def test_member_types():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 1, 0, 0)
    Node(3, 2, 0, 0)
    Node(4, 3, 0, 0)
    Node(5, 4, 0, 0)
    Node(6, 5, 0, 0)
    Node(7, 6, 0, 0)
    Node(8, 7, 0, 0)
    Node(9, 8, 0, 0)
    Node(10, 9, 0, 0)
    Node(11, 10, 0, 0)
    Node(12, 11, 0, 0)
    Node(13, 12, 0, 0)
    Node(14, 13, 0, 0)

    Material(1, 'S235')

    CrossSection(1, 'IPE 300', 1)

    Member.Beam(1, 1, 2)
    Member.Rigid(2, 2, 3)
    Member.Truss(3, 3, 4)
    Member.TrussOnlyN(4, 4, 5)
    Member.Tension(5, 5, 6)
    Member.Compression(6, 6, 7)
    Member.Buckling(7, 7, 8)
    Member.Cable(8, 8, 9)
    Member.DefinableStiffness(9, 9, 10)
    Member.CouplingRigidRigid(10, 10, 11)
    Member.CouplingRigidHinge(11, 11, 12)
    Member.CouplingHingeRigid(12, 12, 13)
    Member.CouplingHingeHinge(13, 13, 14)


    Model.clientModel.service.finish_modification()

    assert Model.clientModel.service.get_member(1).type == MemberType.TYPE_BEAM.name
    assert Model.clientModel.service.get_member(2).type == MemberType.TYPE_RIGID.name
    assert Model.clientModel.service.get_member(3).type == MemberType.TYPE_TRUSS.name
    assert Model.clientModel.service.get_member(4).type == MemberType.TYPE_TRUSS_ONLY_N.name
    assert Model.clientModel.service.get_member(5).type == MemberType.TYPE_TENSION.name
    assert Model.clientModel.service.get_member(6).type == MemberType.TYPE_COMPRESSION.name
    assert Model.clientModel.service.get_member(7).type == MemberType.TYPE_BUCKLING.name
    assert Model.clientModel.service.get_member(8).type == MemberType.TYPE_CABLE.name
    assert Model.clientModel.service.get_member(9).type == MemberType.TYPE_DEFINABLE_STIFFNESS.name
    assert Model.clientModel.service.get_member(10).type == MemberType.TYPE_COUPLING_RIGID_RIGID.name
    assert Model.clientModel.service.get_member(11).type == MemberType.TYPE_COUPLING_RIGID_HINGE.name
    assert Model.clientModel.service.get_member(12).type == MemberType.TYPE_COUPLING_HINGE_RIGID.name
    assert Model.clientModel.service.get_member(13).type == MemberType.TYPE_COUPLING_HINGE_HINGE.name
