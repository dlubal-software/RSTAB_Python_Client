import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

import pytest
from RSTAB.enums import NodalSupportType
from RSTAB.initModel import Model
from RSTAB.BasicObjects.material import Material
from RSTAB.BasicObjects.node import Node
from RSTAB.TypesForNodes.nodalSupport import NodalSupport
from RSTAB.TypesForNodes.nodalSupport import NodalSupport
from RSTAB.dataTypes import inf


if Model.clientModel is None:
    Model()

def test_typesForNodes():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Material(1, 'S235')

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)
    Node(3, 5, 5, 0)
    Node(4, 0, 5, 0)
    Node(5,2.5,2.5,-2.5)

    NodalSupport(1, '1 2', [inf, inf, inf, 0.0, 0.0, inf])
    NodalSupport(2, '3', NodalSupportType.FIXED)
    NodalSupport(3, '4', NodalSupportType.ROLLER_IN_X)
    with pytest.raises(ValueError):
        NodalSupport(4, '5', [inf, inf, inf, 0.0])

    Model.clientModel.service.finish_modification()

    nodalSupport = Model.clientModel.service.get_nodal_support(1)
    assert nodalSupport.spring_x == inf
    assert nodalSupport.spring_y == inf
    assert nodalSupport.spring_z == inf
    assert nodalSupport.rotational_restraint_x == 0
    assert nodalSupport.rotational_restraint_y == 0
    assert nodalSupport.rotational_restraint_z == inf

    nodalSupport = Model.clientModel.service.get_nodal_support(2)
    assert nodalSupport.spring_x == inf
    assert nodalSupport.spring_y == inf
    assert nodalSupport.spring_z == inf
    assert nodalSupport.rotational_restraint_x == inf
    assert nodalSupport.rotational_restraint_y == inf
    assert nodalSupport.rotational_restraint_z == inf

    nodalSupport = Model.clientModel.service.get_nodal_support(3)
    assert nodalSupport.spring_x == 0
    assert nodalSupport.spring_y == inf
    assert nodalSupport.spring_z == inf
    assert nodalSupport.rotational_restraint_x == 0
    assert nodalSupport.rotational_restraint_y == 0
    assert nodalSupport.rotational_restraint_z == inf
