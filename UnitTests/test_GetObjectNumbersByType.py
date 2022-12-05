import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir)
)
sys.path.append(PROJECT_ROOT)
from RSTAB.enums import ObjectTypes
from RSTAB.initModel import Model
from RSTAB.BasicObjects.node import Node
from RSTAB.Tools.GetObjectNumbersByType import GetObjectNumbersByType

if Model.clientModel is None:
    Model()

def test_GetObjectNumbersByType():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)
    Node(3, 0, 5, 0)

    Model.clientModel.service.finish_modification()

    assert GetObjectNumbersByType(ObjectTypes.E_OBJECT_TYPE_NODE) == [1, 2, 3]
