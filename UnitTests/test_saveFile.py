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

    savePath = "/testResults/save.rs9"
    filePath = dirName + savePath

    if (os.path.isfile(filePath)):
        os.remove(filePath)

    Model(True, 'save.rs9')
    Model.clientModel.service.delete_all()

    Material(1, 'S235')

    saveFile(filePath)

    closeModel('save.rs9')

    assert os.path.isfile(filePath)
