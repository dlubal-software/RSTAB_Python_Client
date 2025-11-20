import sys
import os
import pytest
from suds import WebFault

PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
from RSTAB.initModel import Model
from RSTAB.connectionGlobals import url
from RSTAB.enums import CaseObjectType
from RSTAB.Results.resultTables import ResultTables
from tools import getPathToRunningRSTAB

if Model.clientModel is None:
    Model()

@pytest.mark.skipif(url != 'http://127.0.0.1', reason="This test fails on remote PC due to incorrect file path. \
                    Althought it is easy to change, it would not be easy to update on every remote computer.\
                    It is not necessary to evaluate Client as functional. Localy this tests still gets executed.")
def test_result_tables():
    Model.clientModel.service.delete_all()
    Model.clientModel.service.run_script(os.path.join(getPathToRunningRSTAB(), 'scripts\\internal\\Demos\\Demo-001 Hall.js'))
    Model.clientModel.service.calculate_all(False)

    assert Model.clientModel.service.has_any_results()

    # CO1
    assert ResultTables.MembersGlobalDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 3)
    assert ResultTables.MembersInternalForces(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 2)
    assert ResultTables.MembersInternalForcesByCrossSection(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 2)
    assert ResultTables.MembersLocalDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 4)
    assert ResultTables.MembersLocalDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_COMBINATION, 1, 1)

    #LC1
    assert ResultTables.MembersStrains(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 1,1)
    assert ResultTables.NodesDeformations(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 1, 20)
    assert ResultTables.NodesSupportForces(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 1, 16)
    assert ResultTables.Summary(CaseObjectType.E_OBJECT_TYPE_LOAD_CASE, 1)
