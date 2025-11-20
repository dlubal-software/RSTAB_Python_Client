import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir)
)
sys.path.append(PROJECT_ROOT)
from RSTAB.initModel import Model
from RSTAB.connectionGlobals import url
from RSTAB.Tools.GetObjectNumbersByType import GetAllObjects
from tools import getPathToRunningRSTAB
import pytest

if Model.clientModel is None:
    Model()

@pytest.mark.skipif(url != 'http://127.0.0.1', reason="This test fails on remote PC due to incorrect file path. \
                    Althought it is easy to change, it would not be easy to update on every remote computer.\
                    It is not necessary to evaluate Client as functional. Localy this tests still gets executed.")
def test_GetAllObjects():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.run_script(os.path.join(getPathToRunningRSTAB(), 'scripts\\internal\\Demos\\Demo-002 Cantilever Beams.js'))

    objects, imports = GetAllObjects()

    assert len(imports) == 13
    assert len(objects) == 20
