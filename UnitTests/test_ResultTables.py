import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
from RSTAB.initModel import Model, CheckIfMethodOrTypeExists
from RSTAB.enums import CaseObjectType
from RSTAB.Results.resultTables import ResultTables, GetMaxValue, GetMinValue
import pytest

if Model.clientModel is None:
    Model()

@pytest.mark.skipif(CheckIfMethodOrTypeExists(Model.clientModel, 'has_results', True), reason="has_results not in RSTAB GM yet")
def test_result_tables():
    Model.clientModel.service.delete_all()
    Model.clientModel.service.run_script('..\\scripts\\internal\\Demos\\Demo-001 Hall.js')
    Model.clientModel.service.calculate_all(False)

    assert Model.clientModel.service.has_any_results()

    # CO1

    assert ResultTables.MembersGlobalDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 3)
    assert ResultTables.MembersInternalForces(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 2)
    assert not ResultTables.MembersInternalForcesBySection(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 2)
    assert ResultTables.MembersLocalDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 4)
    assert ResultTables.MembersLocalDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 1)

    #LC1
    assert ResultTables.MembersStrains(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 1,1)
    assert ResultTables.NodesDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 1, 20)
    assert ResultTables.NodesSupportForces(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 1, 16)
    assert ResultTables.Summary(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 1)
