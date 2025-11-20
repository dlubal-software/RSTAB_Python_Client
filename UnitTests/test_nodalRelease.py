import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir)
)
sys.path.append(PROJECT_ROOT)

from RSTAB.dataTypes import inf
from RSTAB.initModel import Model
from RSTAB.enums import NodalReleaseReleaseLocation
from RSTAB.BasicObjects.material import Material
from RSTAB.BasicObjects.crossSection import CrossSection
from RSTAB.BasicObjects.node import Node
from RSTAB.BasicObjects.member import Member
from RSTAB.TypesForSpecialObjects.nodalReleaseType import NodalReleaseType
from RSTAB.SpecialObjects.nodalRelease import NodalRelease

if Model.clientModel is None:
    Model()

def test_NodalRelease():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Material(1)
    CrossSection(1, 'IPE 120')

    Node(1,0,0,0)
    Node(2,10,0,0)
    Node(3,10,10,0)
    Node(4,0,10,0)
    Node(5,0,0,-10)
    Node(6,10,0,-10)
    Node(7,10,10,-10)
    Node(8,0,10,-10)

    Member(1, 1, 2)
    Member(2, 2, 3)
    Member(3, 3, 4)
    Member(4, 4, 1)

    Member(5, 5, 6)
    Member(6, 6, 7)
    Member(7, 7, 8)
    Member(8, 8, 5)

    Member(9, 1, 5)
    Member(10, 2, 6)
    Member(11, 3, 7)
    Member(12, 4, 8)

    NodalReleaseType(1, [0, inf, inf, 0])
    NodalReleaseType(2, [0, 0, 0, 0])

    NodalRelease(1, '1', 1, NodalReleaseReleaseLocation.RELEASE_LOCATION_ORIGIN, '1 4')
    NodalRelease(2, '2 3', 2, NodalReleaseReleaseLocation.RELEASE_LOCATION_RELEASED, '2 3 11')

    Model.clientModel.service.finish_modification()

    nr1 = Model.clientModel.service.get_nodal_release(1)
    assert nr1.nodal_release_type == 1
    assert nr1.release_location == "RELEASE_LOCATION_ORIGIN"

    nr2 = Model.clientModel.service.get_nodal_release(2)
    assert nr2.nodes == '2 3'
    assert nr2.release_location == "RELEASE_LOCATION_RELEASED"
