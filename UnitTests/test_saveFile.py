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

    savePath = r"\testResults\save.rs9"
    filepath = dirName + savePath

    if (os.path.isfile(savePath)):
        os.remove(savePath)

    Model(True, 'save.rs9')
    Model.clientModel.service.delete_all()

    Material(1, 'S235')

    saveFile(filepath)

    closeModel('save.rs9')

    assert os.path.isfile(filepath)
    os.remove(filepath)

