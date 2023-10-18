import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir)
)
dirName = os.path.dirname(__file__)
sys.path.append(PROJECT_ROOT)

from RSTAB.initModel import Model, saveFile, closeModel
from RSTAB.BasicObjects.material import Material

if Model.clientModel is None:
    Model()

def test_SaveFile():

    if (os.path.isfile("/testResults/save.rs9")):
        os.remove("/testResults/save.rs9")

    Model(True, 'save.rs9')
    Model.clientModel.service.delete_all()

    Material(1, 'S235')

    saveFile(dirName + '/testResults/save.rs9')

    closeModel('save.rs9')

    assert os.path.isfile(dirName + "/testResults/save.rs9")
    #os.remove(dirName + '/testResults/save.rs9')
