import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

import pytest
from RSTAB.enums import NodalSupportType, NodalSupportNonlinearity, NodalSupportDiagramType, SupportPartialActivityAlongType, \
    SupportPartialActivityAroundType, SupportStiffnessDiagramDependOn, NodalSupportStiffnessDiagramType
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

def test_nodalsupportnonlinearity():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Material(1, 'S235')

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)
    Node(3, 10, 0, 0)

    NodalSupport.Nonlinearity(1, "1", 1, [1.0, 2.0, inf, inf, 3, inf], [NodalSupportNonlinearity.NONLINEARITY_TYPE_DIAGRAM, [True, NodalSupportDiagramType.DIAGRAM_ENDING_TYPE_CONTINUOUS], [[0.5, 1], [1, 2], [2, 3]]], \
                              [NodalSupportNonlinearity.NONLINEARITY_TYPE_DIAGRAM, [False, NodalSupportDiagramType.DIAGRAM_ENDING_TYPE_FAILURE, NodalSupportDiagramType.DIAGRAM_ENDING_TYPE_YIELDING], [[-1, -1.5], [-0.5, -1], [0, 0], [1, 1], [2, 2.5]]], \
                                rotational_y_nonlinearity= [NodalSupportNonlinearity.NONLINEARITY_TYPE_DIAGRAM, [True, NodalSupportDiagramType.DIAGRAM_ENDING_TYPE_STOP], [[1,0.5], [2, 1], [3, 3]]], name='Nonlinear')

    NodalSupport.Nonlinearity(2, '2', 1, [100.0, 200.0, 0.1, 400, 300, 0.2], [NodalSupportNonlinearity.NONLINEARITY_TYPE_PARTIAL_ACTIVITY, [SupportPartialActivityAlongType.PARTIAL_ACTIVITY_TYPE_FAILURE], [SupportPartialActivityAlongType.PARTIAL_ACTIVITY_TYPE_COMPLETE, 1]], \
                              [NodalSupportNonlinearity.NONLINEARITY_TYPE_PARTIAL_ACTIVITY, [SupportPartialActivityAlongType.PARTIAL_ACTIVITY_TYPE_FIXED, 0.0, 2], [SupportPartialActivityAlongType.PARTIAL_ACTIVITY_TYPE_COMPLETE, 3]], \
                              [NodalSupportNonlinearity.NONLINEARITY_TYPE_FAILURE_IF_NEGATIVE], [NodalSupportNonlinearity.NONLINEARITY_TYPE_PARTIAL_ACTIVITY, [SupportPartialActivityAroundType.PARTIAL_ACTIVITY_TYPE_FIXED, 0.0, 150], [SupportPartialActivityAroundType.PARTIAL_ACTIVITY_TYPE_FAILURE]], \
                              [NodalSupportNonlinearity.NONLINEARITY_TYPE_FAILURE_ALL_IF_POSITIVE], [NodalSupportNonlinearity.NONLINEARITY_TYPE_NONE], "Nonlinearity2")

    #NodalSupport.Nonlinearity(3, '3', 1, [1,2,3,4,5,6], [NodalSupportNonlinearity.NONLINEARITY_TYPE_FRICTION_DIRECTION_1, 10], [NodalSupportNonlinearity.NONLINEARITY_TYPE_FRICTION_DIRECTION_1_2, 20], [NodalSupportNonlinearity.NONLINEARITY_TYPE_FRICTION_DIRECTION_1_PLUS_2, 30, 40], \
    #                          [NodalSupportNonlinearity.NONLINEARITY_TYPE_STIFFNESS_DIAGRAM, [SupportStiffnessDiagramDependOn.STIFFNESS_DIAGRAM_DEPENDS_ON_PX, True, NodalSupportStiffnessDiagramType.STIFFNESS_DIAGRAM_ENDING_TYPE_YIELDING], [[1,1],[2,3],[3,4]]], \
    #                          [NodalSupportNonlinearity.NONLINEARITY_TYPE_STIFFNESS_DIAGRAM, [SupportStiffnessDiagramDependOn.STIFFNESS_DIAGRAM_DEPENDS_ON_PZ, False, NodalSupportStiffnessDiagramType.STIFFNESS_DIAGRAM_ENDING_TYPE_FAILURE, NodalSupportStiffnessDiagramType.STIFFNESS_DIAGRAM_ENDING_TYPE_CONTINUOUS], [[-2,-3],[-1.5,1],[0,0],[1,2],[2,5]]], \
    #                          [NodalSupportNonlinearity.NONLINEARITY_TYPE_STIFFNESS_DIAGRAM, [SupportStiffnessDiagramDependOn.STIFFNESS_DIAGRAM_DEPENDS_ON_P, True, NodalSupportStiffnessDiagramType.STIFFNESS_DIAGRAM_ENDING_TYPE_CONTINUOUS], [[0,1],[10,2],[15,4]]], 'Nonlinearity3')

    Model.clientModel.service.finish_modification()

    nsn = Model.clientModel.service.get_nodal_support(1)
    assert nsn.name == 'Nonlinear'
    assert nsn.spring_x_nonlinearity == 'NONLINEARITY_TYPE_DIAGRAM'
    assert nsn.diagram_along_y_table[0][0].row['displacement'] == -1
    assert nsn.rotational_restraint_y == 3

    nsn2 = Model.clientModel.service.get_nodal_support(2)
    assert nsn2.name == 'Nonlinearity2'
    assert nsn2.partial_activity_around_x_negative_type == 'PARTIAL_ACTIVITY_TYPE_COMPLETE'

    #nsn3 = Model.clientModel.service.get_nodal_support(3)
    #assert nsn3.name == 'Nonlinearity3'
    #assert nsn3.spring_z_nonlinearity == 'NONLINEARITY_TYPE_FRICTION_DIRECTION_1_PLUS_2'
    #assert nsn3.stiffness_diagram_around_y_symmetric == False
    #assert nsn3.stiffness_diagram_around_z_table[0][2].row['force'] == 15
