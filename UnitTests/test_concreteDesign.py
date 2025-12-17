import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
               os.path.dirname(__file__),
               os.pardir)
)
sys.path.append(PROJECT_ROOT)

from RSTAB.enums import *
from RSTAB.initModel import Model, SetAddonStatus
from RSTAB.BasicObjects.member import Member
from RSTAB.BasicObjects.node import Node
from RSTAB.BasicObjects.crossSection import CrossSection
from RSTAB.BasicObjects.material import Material
from RSTAB.TypesforConcreteDesign.ConcreteDurability import ConcreteDurability
from RSTAB.TypesforConcreteDesign.ConcreteEffectiveLength import ConcreteEffectiveLength

if Model.clientModel is None:
    Model()

def test_concrete_design():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    SetAddonStatus(Model.clientModel, AddOn.concrete_design_active)

    Material(1, 'C30/37')
    Material(2, 'B550S(A)')
    CrossSection()

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)

    Member(1, 1, 2, 0, 1, 1)

    # Concrete Durabilities
    ConcreteDurability(1, "XC 1", '1', '', [True, False, False, False], [], [False, False, False], [], [DurabilityStructuralClassType.STANDARD, False, False, False, False], [False], [False], [DurabilityAllowanceDeviationType.STANDARD, False])

    ConcreteDurability(2, "XC 2", '1', '', [False, True, True, True], [DurabilityCorrosionCarbonation.CORROSION_INDUCED_BY_CARBONATION_TYPE_DRY_OR_PERMANENTLY_WET, DurabilityCorrosionChlorides.CORROSION_INDUCED_BY_CHLORIDES_TYPE_MODERATE_HUMIDITY, DurabilityCorrosionSeaWater.CORROSION_INDUCED_BY_CHLORIDES_FROM_SEA_WATER_TYPE_AIRBORNE_SALT], [False, False, False], [], [DurabilityStructuralClassType.STANDARD, False, False, False, False], [False], [False], [DurabilityAllowanceDeviationType.STANDARD, False])

    ConcreteDurability(3, "XC 3", '1', '', [True, False, False, False], [], [True, True, True], [DurabilityFreezeThawAttack.FREEZE_THAW_ATTACK_TYPE_MODERATE_SATURATION_NO_DEICING, DurabilityChemicalAttack.CHEMICAL_ATTACK_TYPE_SLIGHTLY_AGGRESSIVE, DurabilityCorrosionWear.CONCRETE_CORROSION_INDUCED_BY_WEAR_TYPE_MODERATE], [DurabilityStructuralClassType.STANDARD, False, False, False, False], [False], [False], [DurabilityAllowanceDeviationType.STANDARD, False])

    ConcreteDurability(4, "XC 4", '1', '', [True, False, False, False], [], [False, False, False], [], [DurabilityStructuralClassType.STANDARD, True, True, True, True], [False], [False], [DurabilityAllowanceDeviationType.STANDARD, False])

    ConcreteDurability(5, "XC 5", '1', '', [True, False, False, False], [], [False, False, False], [], [DurabilityStructuralClassType.DEFINED, DurabilityStructuralClass.S4], [False], [False], [DurabilityAllowanceDeviationType.STANDARD, False])

    ConcreteDurability(6, "XC 6", '1', '', [True, False, False, False], [], [False, False, False], [], [DurabilityStructuralClassType.STANDARD, False, False, False, False], [True, DurabilityStainlessSteelType.STANDARD], [False], [DurabilityAllowanceDeviationType.STANDARD, False])

    ConcreteDurability(7, "XC 7", '1', '', [True, False, False, False], [], [False, False, False], [], [DurabilityStructuralClassType.STANDARD, False, False, False, False], [True, DurabilityStainlessSteelType.DEFINED, 0.012], [False], [DurabilityAllowanceDeviationType.STANDARD, False])

    ConcreteDurability(8, "XC 8", '1', '', [True, False, False, False], [], [False, False, False], [], [DurabilityStructuralClassType.STANDARD, False, False, False, False], [True, DurabilityStainlessSteelType.DEFINED, 0.012], [True, DurabilityAdditionalProtectionType.STANDARD], [DurabilityAllowanceDeviationType.STANDARD, False])

    ConcreteDurability(9, "XC 9", '1', '', [True, False, False, False], [], [False, False, False], [], [DurabilityStructuralClassType.STANDARD, False, False, False, False], [True, DurabilityStainlessSteelType.DEFINED, 0.012], [True, DurabilityAdditionalProtectionType.DEFINED, 0.02], [DurabilityAllowanceDeviationType.STANDARD, False])

    ConcreteDurability(10, "XC 10", '1', '', [True, False, False, False], [], [False, False, False], [], [DurabilityStructuralClassType.STANDARD, False, False, False, False], [True, DurabilityStainlessSteelType.DEFINED, 0.012], [True, DurabilityAdditionalProtectionType.DEFINED, 0.02], [DurabilityAllowanceDeviationType.STANDARD, True, DurabilityConcreteCast.AGAINST_PREPARED_GROUND])

    ConcreteDurability(11, "XC 11", '1', '',[True, False, False, False], [], [False, False, False], [], [DurabilityStructuralClassType.STANDARD, False, False, False, False], [True, DurabilityStainlessSteelType.DEFINED, 0.012], [True, DurabilityAdditionalProtectionType.DEFINED, 0.02], [DurabilityAllowanceDeviationType.DEFINED, 0.008])

    # Concrete Effective Lengths
    ConcreteEffectiveLength()

    Model.clientModel.service.finish_modification()

    cd = Model.clientModel.service.get_concrete_durability(1)
    assert cd.no == 1
    assert cd.user_defined_name_enabled == True
    assert cd.name == "XC 1"
    assert cd.members == ""
    assert cd.member_sets == ""
    assert cd.no_risk_of_corrosion_or_attack_enabled == True
    assert cd.no_risk_of_corrosion_or_attack == "VERY_DRY"
    assert cd.freeze_thaw_attack_enabled == False
    assert cd.chemical_attack_enabled == False
    assert cd.concrete_corrosion_induced_by_wear_enabled == False
    assert cd.structural_class_type == "STANDARD"
    assert cd.increase_design_working_life_from_50_to_100_years_enabled == False
    assert cd.position_of_reinforcement_not_affected_by_construction_process_enabled == False
    assert cd.special_quality_control_of_production_enabled == False
    assert cd.air_entrainment_of_more_than_4_percent_enabled == False
    assert cd.stainless_steel_enabled == False
    assert cd.additional_protection_enabled == False
    assert cd.allowance_of_deviation_type == "STANDARD"
    assert cd.concrete_cast_enabled == False
