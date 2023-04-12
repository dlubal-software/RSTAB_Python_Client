#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)
sys.path.append(dirName + r'/..')

from RSTAB.initModel import Model, SetAddonStatus
from RSTAB.enums import *
from RSTAB.TypesForMembers.memberRotationalRestraint import MemberRotationalRestraint

if __name__ == '__main__':

    Model(True, 'Demo')

    Model.clientModel.service.begin_modification()

    SetAddonStatus(Model.clientModel, AddOn.aluminum_design_active)
    SetAddonStatus(Model.clientModel, AddOn.steel_design_active)
    SetAddonStatus(Model.clientModel, AddOn.timber_design_active)

    MemberRotationalRestraint.Continuous(1, '', '', 'S235', 'GOST C (-) 10-899-0.6 (b: 1) | GOST 24045-94 | --')
    MemberRotationalRestraint.Discrete(2, '', '', 'S235', 'IPE 100')
    MemberRotationalRestraint.Manually(3, '', '', 1500)

    Model.clientModel.service.finish_modification()