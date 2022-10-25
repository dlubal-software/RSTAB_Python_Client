import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
from RSTAB.enums import *
from RSTAB.initModel import Model
from RSTAB.BasicObjects.material import Material
from RSTAB.BasicObjects.section import Section
from RSTAB.BasicObjects.node import Node
from RSTAB.BasicObjects.member import Member
from RSTAB.LoadCasesAndCombinations.loadCase import LoadCase
from RSTAB.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RSTAB.Loads.memberLoad import MemberLoad
from RSTAB.Loads.nodalLoad import NodalLoad

if Model.clientModel is None:
    Model()

def test_nodal_load_init():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 2, 0, 0)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    NodalLoad(1, 1, '1', LoadDirectionType.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W, 5000)

    Model.clientModel.service.finish_modification()

    nodal_load = Model.clientModel.service.get_nodal_load(1, 1)

    assert nodal_load.no == 1
    assert nodal_load.force_magnitude == 5000

def test_nodal_load_force():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 2, 0, 0)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    NodalLoad.Force(1, 1, '1', LoadDirectionType.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W, 5000)
    Model.clientModel.service.finish_modification()

    nodal_load = Model.clientModel.service.get_nodal_load(1, 1)

    assert nodal_load.no == 1
    assert nodal_load.force_magnitude == 5000

def test_nodal_load_moment():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 2, 0, 0)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    NodalLoad.Moment(1, 1, '1', LoadDirectionType.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W, 5000)

    Model.clientModel.service.finish_modification()

    nodal_load = Model.clientModel.service.get_nodal_load(1, 1)

    assert nodal_load.no == 1
    assert nodal_load.moment_magnitude == 5000

def test_nodal_load_components():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 2, 0, 0)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    NodalLoad.Components(1, 1, '1', [5000, 0, 0, 0, 6000, 0])

    Model.clientModel.service.finish_modification()

    nodal_load = Model.clientModel.service.get_nodal_load(1, 1)

    assert nodal_load.components_moment_y == 6000
    assert nodal_load.components_force_x  == 5000

def test_nodal_load_mass():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 2, 0, 0)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    NodalLoad.Mass(1, 1, '1', False,[5000])

    Model.clientModel.service.finish_modification()

    nodal_load = Model.clientModel.service.get_nodal_load(1, 1)

    assert nodal_load.no == 1
    assert nodal_load.mass_global == 5000

### Member Load Unit Tests ###

def test_member_load_init():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')
    Section(1, 'IPE 300', 1)
    Member(1,  1, 2, 0, 1, 1)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    MemberLoad(1, 1, '1', LoadDirectionType.LOAD_DIRECTION_LOCAL_Z, 4000)

    Model.clientModel.service.finish_modification()

    member_load = Model.clientModel.service.get_member_load(1, 1)

    assert member_load.no == 1
    assert member_load.magnitude == 4000

def test_member_load_force():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')
    Section(1, 'IPE 300', 1)
    Member(1,  1, 2, 0, 1, 1)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    MemberLoad.Force(1, 1, '1', MemberLoadDistribution.LOAD_DISTRIBUTION_UNIFORM, MemberLoadDirection.LOAD_DIRECTION_LOCAL_Z, [6000])

    Model.clientModel.service.finish_modification()

    member_load = Model.clientModel.service.get_member_load(1, 1)

    assert member_load.no == 1
    assert member_load.magnitude == 6000

def test_member_load_moment():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')
    Section(1, 'IPE 300', 1)
    Member(1,  1, 2, 0, 1, 1)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    MemberLoad.Moment(1, 1, '1', MemberLoadDistribution.LOAD_DISTRIBUTION_UNIFORM, MemberLoadDirection.LOAD_DIRECTION_LOCAL_Z, [3000])

    Model.clientModel.service.finish_modification()

    member_load = Model.clientModel.service.get_member_load(1, 1)

    assert member_load.no == 1
    assert member_load.magnitude == 3000

def test_member_load_mass():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')
    Section(1, 'IPE 300', 1)
    Member(1,  1, 2, 0, 1, 1)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    MemberLoad.Mass(1, 1, '1', False, mass_components=[5000])
    Model.clientModel.service.finish_modification()

    member_load = Model.clientModel.service.get_member_load(1, 1)

    assert member_load.no == 1
    assert member_load.mass_global == 5000

def test_member_load_temperature():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')
    Section(1, 'IPE 300', 1)
    Member(1,  1, 2, 0, 1, 1)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    MemberLoad.Temperature(1, 1, '1', MemberLoadDistribution.LOAD_DISTRIBUTION_UNIFORM, MemberLoadDirection.LOAD_DIRECTION_LOCAL_Z, [0.497, 0.596])

    Model.clientModel.service.finish_modification()

    member_load = Model.clientModel.service.get_member_load(1, 1)

    assert member_load.magnitude_t_b  == 0.497
    assert member_load.magnitude_t_t  == 0.596

def test_member_load_temperature_change():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')
    Section(1, 'IPE 300', 1)
    Member(1,  1, 2, 0, 1, 1)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    MemberLoad.TemperatureChange(1, 1, '1', MemberLoadDistribution.LOAD_DISTRIBUTION_UNIFORM, MemberLoadDirection.LOAD_DIRECTION_LOCAL_Z, [0.5, 0.6])

    Model.clientModel.service.finish_modification()

    member_load = Model.clientModel.service.get_member_load(1, 1)

    assert member_load.magnitude_delta_t   == 0.5
    assert member_load.magnitude_t_c   == 0.6

def test_member_load_axial_strain():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')
    Section(1, 'IPE 300', 1)
    Member(1,  1, 2, 0, 1, 1)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    MemberLoad.AxialStrain(1, 1, '1', MemberLoadDistribution.LOAD_DISTRIBUTION_UNIFORM, MemberLoadDirection.LOAD_DIRECTION_LOCAL_X, [0.5])

    Model.clientModel.service.finish_modification()

    member_load = Model.clientModel.service.get_member_load(1, 1)

    assert member_load.magnitude == 0.5
    assert member_load.load_type == "LOAD_TYPE_AXIAL_STRAIN"

def test_member_load_axial_displacement():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')
    Section(1, 'IPE 300', 1)
    Member(1,  1, 2, 0, 1, 1)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    MemberLoad.AxialDisplacement(1, 1, '1', MemberLoadDirection.LOAD_DIRECTION_LOCAL_X, 50)

    Model.clientModel.service.finish_modification()

    member_load = Model.clientModel.service.get_member_load(1, 1)

    assert member_load.no == 1
    assert member_load.magnitude == 50

def test_member_load_precamber():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')
    Section(1, 'IPE 300', 1)
    Member(1,  1, 2, 0, 1, 1)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    MemberLoad.Precamber(1, 1, '1', MemberLoadDistribution.LOAD_DISTRIBUTION_UNIFORM, MemberLoadDirection.LOAD_DIRECTION_LOCAL_Z, [5])

    Model.clientModel.service.finish_modification()

    member_load = Model.clientModel.service.get_member_load(1, 1)

    assert member_load.no == 1
    assert member_load.magnitude == 5

def test_member_load_initial_prestress():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')
    Section(1, 'IPE 300', 1)
    Member(1,  1, 2, 0, 1, 1)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    MemberLoad.InitialPrestress(1, 1, '1', MemberLoadDirection.LOAD_DIRECTION_LOCAL_X, 50)

    Model.clientModel.service.finish_modification()

    member_load = Model.clientModel.service.get_member_load(1, 1)

    assert member_load.no == 1
    assert member_load.magnitude == 50

def test_member_load_displacement():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')
    Section(1, 'IPE 300', 1)
    Member(1,  1, 2, 0, 1, 1)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    MemberLoad.Displacement(1, 1, '1', MemberLoadDistribution.LOAD_DISTRIBUTION_UNIFORM, MemberLoadDirection.LOAD_DIRECTION_LOCAL_Z, [60])

    Model.clientModel.service.finish_modification()

    member_load = Model.clientModel.service.get_member_load(1, 1)

    assert member_load.no == 1
    assert member_load.magnitude == 60

def test_member_load_rotation():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')
    Section(1, 'IPE 300', 1)
    Member(1,  1, 2, 0, 1, 1)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    MemberLoad.Rotation(1, 1, '1', MemberLoadDistribution.LOAD_DISTRIBUTION_UNIFORM, MemberLoadDirection.LOAD_DIRECTION_LOCAL_Z, [0.6])

    Model.clientModel.service.finish_modification()

    member_load = Model.clientModel.service.get_member_load(1, 1)

    assert member_load.no == 1
    assert member_load.magnitude == 0.6

def test_member_load_pipecontentfull():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')
    Section(1, 'CHS 100x4', 1)
    Member(1,  1, 2, 0, 1, 1)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    MemberLoad.PipeContentFull(1, 1, '1', MemberLoadDirectionOrientation.LOAD_DIRECTION_FORWARD, 50)

    Model.clientModel.service.finish_modification()

    member_load = Model.clientModel.service.get_member_load(1, 1)

    assert member_load.no == 1
    assert member_load.magnitude == 50

def test_member_load_pipecontentpartial():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')
    Section(1, 'CHS 100x4', 1)
    Member(1,  1, 2, 0, 1, 1)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    MemberLoad.PipeContentPartial(1, 1, '1', MemberLoadDirectionOrientation.LOAD_DIRECTION_FORWARD, 50, 50)

    Model.clientModel.service.finish_modification()

    member_load = Model.clientModel.service.get_member_load(1, 1)

    assert member_load.no == 1
    assert member_load.magnitude == 50

def test_member_load_pipeinternalpressure():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Material(1, 'S235')
    Section(1, 'CHS 100x4', 1)
    Member(1,  1, 2, 0, 1, 1)

    StaticAnalysisSettings(1, 'Linear', StaticAnalysisType.GEOMETRICALLY_LINEAR)
    LoadCase(1, 'DEAD')

    MemberLoad.PipeInternalPressure(1, 1, '1', 50)

    Model.clientModel.service.finish_modification()

    member_load = Model.clientModel.service.get_member_load(1, 1)

    assert member_load.no == 1
    assert member_load.magnitude == 50
