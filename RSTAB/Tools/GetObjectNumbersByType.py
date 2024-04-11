from RSTAB.initModel import Model, ConvertStrToListOfInt, GetAllAddonStatuses
from RSTAB.enums import ObjectTypes
from suds.sax.text import Text
import sys

class GetObjectNumbersByType:

    def __new__(cls,
                ObjectType = ObjectTypes.E_OBJECT_TYPE_NODE,
                model = Model):

        """
        Returns a sorted list which contains object numbers in RSTAB tables.
        ObjectNumberList = [1, 2, ... ] or [[1,2], [2,2]]

        Args:
            ObjectType (enum): Object type enum
            model (RSTAB Class, optional): Model to be edited
        Returns:
            ObjectNumberList (list): Sorted list of object numbers or list of lists if there is parent number (e.g. nodal_load).
        """

        ObjectNumber = model.clientModel.service.get_all_object_numbers_by_type(ObjectType.name)
        ObjectNumberList = []

        if len(ObjectNumber):
            for i in range(len(ObjectNumber.item)):
                # this is used when requesting objects in loads (E_OBJECT_TYPE_NODAL_LOAD, E_OBJECT_TYPE_NODAL_LOAD etc.)
                try:
                    children = ConvertStrToListOfInt(ObjectNumber.item[i].children)
                    for c in children:
                        ObjectNumberList.append([c, ObjectNumber.item[i].no])
                # all other objects
                except:
                    ObjectNumberList.append(ObjectNumber.item[i].no)

            if isinstance(ObjectNumberList[0], list):
                ObjectNumberList = sorted(ObjectNumberList, key=lambda x: x[1])
            else:
                ObjectNumberList.sort()

        return ObjectNumberList

class GetAllObjects:
    """
    Returns tuple of 2 lists containing all objects and their parameters and list of imports needed to facilitate re-creating theese.
    Args:
        model(RSTAB Class, optional): Model to be edited
    Returns:
        objects: List of all objects that can be created via Client.
        imports: List of imports needed to be able to create objects from the first list.
    """
    def __new__(cls,
                model = Model):

        # Steps to retrieve data from RSTAB:
        # 1) get numbers of given object type via GetObjectNumbersByType(),
        # 2) get data from individual objects,
        # 3) set import of the type,
        # 4) set individual objects.
        # For each of these steps individual record is made (4 total).

        # Vector of all function
        func_vec = [[ObjectTypes.E_OBJECT_TYPE_COORDINATE_SYSTEM, lambda i: model.clientModel.service.get_coordinate_system(i), 'from RSTAB.BasicObjects.coordinateSystem import CoordinateSystem\n', 'CoordinateSystem'],
			[ObjectTypes.E_OBJECT_TYPE_MATERIAL, lambda i: model.clientModel.service.get_material(i), 'from RSTAB.BasicObjects.material import Material\n', 'Material'],
            [ObjectTypes.E_OBJECT_TYPE_SECTION, lambda i: model.clientModel.service.get_section(i), 'from RSTAB.BasicObjects.section import Section\n', 'Section'],
            [ObjectTypes.E_OBJECT_TYPE_NODE, lambda i: model.clientModel.service.get_node(i), 'from RSTAB.BasicObjects.node import Node\n', 'Node'],
            [ObjectTypes.E_OBJECT_TYPE_MEMBER, lambda i: model.clientModel.service.get_member(i), 'from RSTAB.BasicObjects.member import Member\n', 'Member'],
            [ObjectTypes.E_OBJECT_TYPE_MEMBER_SET, lambda i: model.clientModel.service.get_member_set(i), 'from RSTAB.BasicObjects.memberSet import MemberSet\n', 'MemberSet'],
            [ObjectTypes.E_OBJECT_TYPE_STRUCTURE_MODIFICATION, lambda i: model.clientModel.service.get_structure_modification(i), 'from RSTAB.SpecialObjects.structureModification import StructureModification\n', 'StructureModification'],
            [ObjectTypes.E_OBJECT_TYPE_NODAL_RELEASE, lambda i: model.clientModel.service.get_nodal_release(i), 'from RSTAB.SpecialObjects.nodalRelease import NodalRelease\n', 'NodalRelease'],
            # blocks

            [ObjectTypes.E_OBJECT_TYPE_NODAL_SUPPORT, lambda i: model.clientModel.service.get_nodal_support(i), 'from RSTAB.TypesForNodes.nodalSupport import NodalSupport\n', 'NodalSupport'],

            [ObjectTypes.E_OBJECT_TYPE_MEMBER_HINGE, lambda i: model.clientModel.service.get_member_hinge(i), 'from RSTAB.TypesForMembers.memberHinge import MemberHinge\n', 'MemberHinge'],
            [ObjectTypes.E_OBJECT_TYPE_MEMBER_ECCENTRICITY, lambda i: model.clientModel.service.get_member_eccentricity(i), 'from RSTAB.TypesForMembers.memberEccentricity import MemberEccentricity\n', 'MemberEccentricity'],
            [ObjectTypes.E_OBJECT_TYPE_MEMBER_SUPPORT, lambda i: model.clientModel.service.get_member_support(i), 'from RSTAB.TypesForMembers.memberSupport import MemberSupport\n', 'MemberSupport'],
            [ObjectTypes.E_OBJECT_TYPE_MEMBER_TRANSVERSE_STIFFENER, lambda i: model.clientModel.service.get_member_transverse_stiffeners(i), 'from RSTAB.TypesForMembers.memberTransverseStiffeners import MemberTransverseStiffeners\n', 'MemberTransverseStiffeners'],
            # member_opening
            [ObjectTypes.E_OBJECT_TYPE_MEMBER_STIFFNESS_MODIFICATION, lambda i: model.clientModel.service.get_member_stiffness_modification(i), 'from RSTAB.TypesForMembers.memberStiffnessModification import MemberStiffnessModification\n', 'MemberStiffnessModification'],
            [ObjectTypes.E_OBJECT_TYPE_MEMBER_NONLINEARITY, lambda i: model.clientModel.service.get_member_nonlinearity(i), 'from RSTAB.TypesForMembers.memberNonlinearity import MemberNonlinearity\n', 'MemberNonlinearity'],
            [ObjectTypes.E_OBJECT_TYPE_MEMBER_DEFINABLE_STIFFNESS, lambda i: model.clientModel.service.get_member_definable_stiffness(i), 'from RSTAB.TypesForMembers.memberDefinableStiffness import MemberDefinableStiffness\n', 'MemberDefinableStiffness'],
            [ObjectTypes.E_OBJECT_TYPE_MEMBER_RESULT_INTERMEDIATE_POINT, lambda i: model.clientModel.service.get_member_result_intermediate_point(i), 'from RSTAB.TypesForMembers.memberResultIntermediatePoints import MemberResultIntermediatePoint\n', 'MemberResultIntermediatePoint'],
            # design_support
            [ObjectTypes.E_OBJECT_TYPE_MEMBER_ROTATIONAL_RESTRAINT, lambda i: model.clientModel.service.get_member_rotational_restraint(i), 'from RSTAB.TypesForMembers.memberRotationalRestraint import MemberRotationalRestraint\n', 'MemberRotationalRestraint'],
            [ObjectTypes.E_OBJECT_TYPE_MEMBER_SHEAR_PANEL, lambda i: model.clientModel.service.get_member_shear_panel(i), 'from RSTAB.TypesForMembers.memberShearPanel import MemberShearPanel\n', 'MemberShearPanel'],

            # nodal_release_type
            [ObjectTypes.E_OBJECT_TYPE_CONCRETE_EFFECTIVE_LENGTHS, lambda i: model.clientModel.service.get_concrete_effective_lengths(i), 'from RSTAB.TypesforConcreteDesign.ConcreteEffectiveLength import ConcreteEffectiveLength\n', 'ConcreteEffectiveLength'],
            [ObjectTypes.E_OBJECT_TYPE_CONCRETE_DURABILITY, lambda i: model.clientModel.service.get_concrete_durability(i), 'from RSTAB.TypesforConcreteDesign.ConcreteDurability import ConcreteDurability\n', 'ConcreteDurability'],
            [ObjectTypes.E_OBJECT_TYPE_CONCRETE_DESIGN_SLS_CONFIGURATION, lambda i: model.clientModel.service.get_concrete_design_sls_configuration(i), 'from RSTAB.ConcreteDesign.ConcreteServiceabilityConfigurations import ConcreteServiceabilityConfiguration\n', 'ConcreteServiceabilityConfiguration'],
            [ObjectTypes.E_OBJECT_TYPE_CONCRETE_DESIGN_ULS_CONFIGURATION, lambda i: model.clientModel.service.get_concrete_design_uls_configuration(i), 'from RSTAB.ConcreteDesign.ConcreteUltimateConfigurations import ConcreteUltimateConfiguration\n', 'ConcreteUltimateConfiguration'],
            [ObjectTypes.E_OBJECT_TYPE_STEEL_EFFECTIVE_LENGTHS, lambda i: model.clientModel.service.get_steel_effective_lengths(i), 'from RSTAB.TypesForSteelDesign.steelEffectiveLengths import SteelEffectiveLengths\n', 'SteelEffectiveLengths'],
            [ObjectTypes.E_OBJECT_TYPE_STEEL_BOUNDARY_CONDITIONS, lambda i: model.clientModel.service.get_steel_boundary_conditions(i), 'from RSTAB.TypesForSteelDesign.steelBoundaryConditions import SteelBoundaryConditions\n', 'SteelBoundaryConditions'],
            [ObjectTypes.E_OBJECT_TYPE_STEEL_MEMBER_LOCAL_SECTION_REDUCTION, lambda i: model.clientModel.service.get_steel_member_local_section_reduction(i), 'from RSTAB.TypesForSteelDesign.SteelMemberLocalSectionReduction import SteelMemberLocalSectionReduction\n', 'SteelMemberLocalSectionReduction'],

            [ObjectTypes.E_OBJECT_TYPE_STEEL_DESIGN_SLS_CONFIGURATION, lambda i: model.clientModel.service.get_steel_design_sls_configuration(i), 'from RSTAB.SteelDesign.steelServiceabilityConfiguration import SteelDesignServiceabilityConfigurations\n', 'SteelDesignServiceabilityConfigurations'],
            [ObjectTypes.E_OBJECT_TYPE_STEEL_DESIGN_ULS_CONFIGURATION, lambda i: model.clientModel.service.get_steel_design_uls_configuration(i), 'from RSTAB.SteelDesign.steelUltimateConfigurations import SteelDesignUltimateConfigurations\n', 'SteelDesignUltimateConfigurations'],
            [ObjectTypes.E_OBJECT_TYPE_TIMBER_EFFECTIVE_LENGTHS, lambda i: model.clientModel.service.get_timber_effective_lengths(i), 'from RSTAB.TypesForTimberDesign.timberEffectiveLengths import TimberEffectiveLengths\n', 'TimberEffectiveLengths'],
            [ObjectTypes.E_OBJECT_TYPE_TIMBER_SERVICE_CLASS, lambda i: model.clientModel.service.get_timber_service_class(i), 'from RSTAB.TypesForTimberDesign.timberServiceClass import TimberServiceClass\n', 'TimberServiceClass'],
            [ObjectTypes.E_OBJECT_TYPE_ALUMINUM_MEMBER_LOCAL_SECTION_REDUCTION, lambda i: model.clientModel.service.get_timber_member_local_section_reduction(i), 'from RSTAB.TypesForTimberDesign.timberMemberLocalSectionReduction import TimberMemberLocalSectionReduction\n', 'TimberMemberLocalSectionReduction'],
            [ObjectTypes.E_OBJECT_TYPE_TIMBER_DESIGN_SLS_CONFIGURATION, lambda i: model.clientModel.service.get_timber_design_sls_configuration(i), 'from RSTAB.TimberDesign.timberServiceLimitStateConfigurations import TimberDesignServiceLimitStateConfigurations\n', 'TimberDesignServiceLimitStateConfigurations'],
            [ObjectTypes.E_OBJECT_TYPE_TIMBER_DESIGN_ULS_CONFIGURATION, lambda i: model.clientModel.service.get_timber_design_uls_configuration(i), 'from RSTAB.TimberDesign.timberUltimateConfigurations import TimberDesignUltimateConfigurations\n', 'TimberDesignUltimateConfigurations'],
            [ObjectTypes.E_OBJECT_TYPE_ALUMINUM_EFFECTIVE_LENGTHS, lambda i: model.clientModel.service.get_aluminum_effective_lengths(i), 'from RSTAB.TypesForAluminumDesign.aluminumEffectiveLengths import AluminumEffectiveLengths\n', 'AluminumEffectiveLengths'],
            [ObjectTypes.E_OBJECT_TYPE_ALUMINUM_MEMBER_LOCAL_SECTION_REDUCTION, lambda i: model.clientModel.service.get_aluminum_member_local_section_reduction(i), 'from RSTAB.TypesForAluminumDesign.aluminumMemberLocalSectionReduction import AluminumMemberLocalSectionReduction\n', 'AluminumMemberLocalSectionReduction'],
            [ObjectTypes.E_OBJECT_TYPE_ALUMINUM_MEMBER_TRANSVERSE_WELD, lambda i: model.clientModel.service.get_aluminum_member_transverse_weld(i), 'from RSTAB.TypesForAluminumDesign.aluminumMemberTransverseWelds import AluminumMemberTransverseWeld\n', 'AluminumMemberTransverseWeld'],
            # steel_joints
            # craneways
            # cran
            [ObjectTypes.E_OBJECT_TYPE_IMPERFECTION_CASE, lambda i: model.clientModel.service.get_imperfection_case(i), 'from RSTAB.Imperfections.imperfectionCase import ImperfectionCase\n', 'ImperfectionCase'],
            [ObjectTypes.E_OBJECT_TYPE_MEMBER_IMPERFECTION, lambda i,j: model.clientModel.service.get_member_imperfection(i,j), 'from RSTAB.Imperfections.memberImperfection import MemberImperfection\n', 'MemberImperfection(imperfection_case='],
            [ObjectTypes.E_OBJECT_TYPE_MEMBER_SET_IMPERFECTION, lambda i: model.clientModel.service.get_member_set_imperfection(i), 'from RSTAB.Imperfections.membersetImperfection import MemberSetImperfection\n', 'MemberSetImperfection(imperfection_case='],
            # construction_stag
            [ObjectTypes.E_OBJECT_TYPE_LOAD_CASE, lambda i: model.clientModel.service.get_load_case(i), 'from RSTAB.LoadCasesAndCombinations.loadCase import LoadCase\n', 'LoadCase'],
            [ObjectTypes.E_OBJECT_TYPE_DESIGN_SITUATION, lambda i: model.clientModel.service.get_design_situation(i), 'from RSTAB.LoadCasesAndCombinations.designSituation import DesignSituation\n', 'DesignSituation'],
            [ObjectTypes.E_OBJECT_TYPE_LOAD_COMBINATION, lambda i: model.clientModel.service.get_load_combination(i), 'from RSTAB.LoadCasesAndCombinations.loadCombination import LoadCombination\n', 'LoadCombination'],
            #[ObjectTypes, lambda i: model.clientModel.service.get_(i), 'from RSTAB.LoadCasesAndCombinations.loadCasesAndCombinations import LoadCasesAndCombinations',]
            [ObjectTypes.E_OBJECT_TYPE_RESULT_COMBINATION, lambda i: model.clientModel.service.get_result_combination(i), 'from RSTAB.LoadCasesAndCombinations.resultCombination import ResultCombination\n', 'ResultCombination'],
            [ObjectTypes.E_OBJECT_TYPE_STATIC_ANALYSIS_SETTINGS, lambda i: model.clientModel.service.get_static_analysis_settings(i), 'from RSTAB.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings\n', 'StaticAnalysisSettings'],
            [ObjectTypes.E_OBJECT_TYPE_STABILITY_ANALYSIS_SETTINGS, lambda i: model.clientModel.service.get_stability_analysis_settings(i), 'from RSTAB.LoadCasesAndCombinations.stabilityAnalysisSettings import StabilityAnalysisSettings\n', 'StabilityAnalysisSettings'],
            [ObjectTypes.E_OBJECT_TYPE_MODAL_ANALYSIS_SETTINGS, lambda i: model.clientModel.service.get_modal_analysis_settings(i), 'from RSTAB.LoadCasesAndCombinations.modalAnalysisSettings import ModalAnalysisSettings\n', 'ModalAnalysisSettings'],
            [ObjectTypes.E_OBJECT_TYPE_SPECTRAL_ANALYSIS_SETTINGS, lambda i: model.clientModel.service.get_spectral_analysis_settings(i), 'from RSTAB.LoadCasesAndCombinations.spectralAnalysisSettings import SpectralAnalysisSettings\n', 'SpectralAnalysisSettings'],
            [ObjectTypes.E_OBJECT_TYPE_COMBINATION_WIZARD, lambda i: model.clientModel.service.get_combination_wizard(i), 'from RSTAB.LoadCasesAndCombinations.combinationWizard import CombinationWizard\n', 'CombinationWizard'],
            # member_loads_from_area_loads
            # member_loads_from_free_line_load
            # snow_loads
            # wind_loads
            # wind_profiles
            # wind_simulatio
            [ObjectTypes.E_OBJECT_TYPE_NODAL_LOAD, lambda i,j: model.clientModel.service.get_nodal_load(i,j), 'from RSTAB.Loads.nodalLoad import NodalLoad\n', 'NodalLoad(load_case_no='],
            [ObjectTypes.E_OBJECT_TYPE_MEMBER_LOAD, lambda i,j: model.clientModel.service.get_member_load(i,j), 'from RSTAB.Loads.memberLoad import MemberLoad\n', 'MemberLoad(load_case_no='],
            [ObjectTypes.E_OBJECT_TYPE_MEMBER_SET_LOAD, lambda i,j: model.clientModel.service.get_member_set_load(i,j), 'from RSTAB.Loads.membersetload import MemberSetLoad\n', 'MemberSetLoad(load_case_no='],
            [ObjectTypes.E_OBJECT_TYPE_IMPOSED_NODAL_DEFORMATION, lambda i,j: model.clientModel.service.get_imposed_nodal_deformation(i,j), 'from RSTAB.Loads.imposedNodalDeformation import ImposedNodalDeformation\n', 'ImposedNodalDeformation(load_case_no=']]
            # calculations_diagram
            #[ObjectTypes.E_OBJECT_TYPE_RESPONSE_SPECTRUM, lambda i: model.clientModel.service.get_response_spectrum(i), 'from RSTAB.DynamicLoads.responseSpectrum import ResponseSpectrum\n', 'ResponseSpectrum']]

        def convertSubclases(param):
            '''
            Convert structures/parameters to approriate structure
            '''
            if isinstance(param, str) or isinstance(param, int) or isinstance(param, float) or isinstance(param, bool):
                pass
            elif isinstance(param, list):
                toDel = []
                for i,j in enumerate(param):
                    # Parameters of value None, UNKNOWN or "" are not exported
                    if j == None or j == 'UNKNOWN' or j == "":
                        toDel.append(i)
                    elif isinstance(j, Text):
                        # Change Text to string
                        param[i] = str(j)
                    else:
                        param[i] = convertSubclases(j)
                for td in toDel:
                    param.remove(td)
            else:
                param = dict(param)
                toDel = []
                for key in param.keys().__reversed__():
                    # Parameters of value None, UNKNOWN or "" are not exported
                    if param[key] == None or param[key] == 'UNKNOWN' or param[key] == "":
                        toDel.append(key)
                    elif isinstance(param[key], Text):
                        # Change Text to string
                        param[key] = str(param[key])
                    else:
                        param[key] = convertSubclases(param[key])
                for td in toDel:
                    del param[td]
            return param

        imports = [] # defines what to import with 'imports'
        objects = [] # individual lines written in file

        # Load Cases and Combinations setup
        loadCasesAndCombinations = convertSubclases(dict(model.clientModel.service.get_load_cases_and_combinations()))
        settingsAndOptions = dict(model.clientModel.service.get_model_settings_and_options())
        addonStatuses = GetAllAddonStatuses(model.clientModel)
        del settingsAndOptions['date_of_zero_day']
        settingsAndOptions = convertSubclases(settingsAndOptions)

        objects.append('LoadCasesAndCombinations(params='+str(loadCasesAndCombinations)+')\n')
        objects.append('BaseSettings(params='+str(settingsAndOptions)+')\n')
        objects.append('SetAddonStatuses('+str(addonStatuses)+')\n')
        imports.append('from RSTAB.LoadCasesAndCombinations.loadCasesAndCombinations import LoadCasesAndCombinations\n')
        imports.append('from RSTAB.baseSettings import BaseSettings, MainObjectsToActivate\n')

        # Get number of every type of object supported by Client.
        # Get info of each existing object.
        # Add import to lines.
        # Add each object to lines.
        for id, func in enumerate(func_vec):

            objNumbers = GetObjectNumbersByType(ObjectType=func[0])
            if objNumbers:
                addImport = False
                for idx,i in enumerate(objNumbers):

                    # Print status
                    percent = (idx/len(objNumbers))*100
                    sys.stdout.write("\r                                                                       ")
                    sys.stdout.write("\r{}: {:.0f}%, total progress: {:.1f}% ".format(func[3], (id/len(func_vec))*100, percent))
                    sys.stdout.flush()

                    try:
                        if isinstance(i, list):
                            params = dict(func[1](i[0], i[1]))
                        else:
                            params = dict(func[1](i))
                        addImport = True
                    except:
                        print('INFO: There seems to a be phantom object or issue in your model. Type:', func[3], ', number:', str(i))
                        continue
                    params = convertSubclases(params)
                    # don't set this parameter
                    del params['id_for_export_import']

                    if isinstance(i, list):
                        objects.append(func[3]+str(i[1])+', params='+str(params)+')\n')
                    else:
                        objects.append(func[3]+'(params='+str(params)+')\n')

                # Add import if at least one object was added
                if addImport:
                    imports.append(func[2])

        sys.stdout.write("\r                                                                       ")
        sys.stdout.write("\rDone 100%\n")
        sys.stdout.flush()
        return (objects, imports)
