from RSTAB.initModel import Model, clearAttributes, deleteEmptyAttributes
from RSTAB.enums import StaticAnalysisSettingsIterativeMethodForNonlinearAnalysis, StaticAnalysisType

class StaticAnalysisSettings():

    def __init__(self,
                 no: int = 1,
                 name: str = None,
                 analysis_type = StaticAnalysisType.GEOMETRICALLY_LINEAR,
                 comment: str = '',
                 params: dict = None,
                 model = Model):
        """
        Args:
            no (int): Static Analysis Setting Tag
            name (str): Static Analysis Setting Name
            analysis_type (enum): Analysis Type Enumeration
            comment (str, optional): Comments
            params (dict, optional): Any WS Parameter relevant to the object and its value in form of a dictionary
            model (RSTAB Class, optional): Model to be edited
        """
        # Client model | Surface
        clientObject = model.clientModel.factory.create('ns0:static_analysis_settings')

        # Clears object atributes | Sets all atributes to None
        clearAttributes(clientObject)

        # Static Analysis Settings No.
        clientObject.no = no

        # Name
        if name:
            clientObject.user_defined_name_enabled = True
            clientObject.name = name

        # Analysis Type
        clientObject.analysis_type = analysis_type.name

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        if params:
            for key in params:
                clientObject[key] = params[key]

        # Delete None attributes for improved performance
        deleteEmptyAttributes(clientObject)

        # Add Static Analysis Settings to client model
        model.clientModel.service.set_static_analysis_settings(clientObject)

    @staticmethod
    def GeometricallyLinear(
                  no: int = 1,
                  name: str = None,
                  load_modification = [False, 1, False],
                  bourdon_effect: bool = False,
                  mass_conversion = [False, 0, 0, 0],
                  comment: str = '',
                  params: dict = None,
                  model = Model):

        """
        Args:
            no (int): Static Analysis Setting Tag
            name (str): Static Analysis Setting Name
            load_modification (list): Load Modification Parameters
                load_modification = [loading_by_multiplier_factor, multiplier_factor, dividing_results]
            mass_conversion (list): Mass Conversion Parameters
                mass_conversion = [mass_conversion_enabled, mass_conversion_factor_in_direction_x, mass_conversion_factor_in_direction_y, mass_conversion_factor_in_direction_z]
            comment (str): Comments
            params (dict): Any WS Parameter relevant to the object and its value in form of a dictionary
            model (RSTAB Class): Model to be edited
        """

        # Client model
        clientObject = model.clientModel.factory.create('ns0:static_analysis_settings')

        # Clears object atributes | Sets all atributes to None
        clearAttributes(clientObject)

        # Static Analysis Settings No.
        clientObject.no = no

        # Name
        if name:
            clientObject.user_defined_name_enabled = True
            clientObject.name = name

        # Static Analysis Type
        clientObject.analysis_type = StaticAnalysisType.GEOMETRICALLY_LINEAR.name

        # Bourdon Effect Displacement
        clientObject.displacements_due_to_bourdon_effect = bourdon_effect

        # Conversion of Mass into Load
        clientObject.mass_conversion_enabled = mass_conversion[0]
        if mass_conversion[0]:
            clientObject.mass_conversion_factor_in_direction_x = mass_conversion[1]
            clientObject.mass_conversion_factor_in_direction_y = mass_conversion[2]
            clientObject.mass_conversion_factor_in_direction_z = mass_conversion[3]

        if load_modification[0]:
            clientObject.modify_loading_by_multiplier_factor = True
            clientObject.loading_multiplier_factor = load_modification[1]
            clientObject.divide_results_by_loading_factor = load_modification[2]

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        if params:
            for key in params:
                clientObject[key] = params[key]

        # Delete None attributes for improved performance
        deleteEmptyAttributes(clientObject)

        # Add Static Analysis Settings to client model
        model.clientModel.service.set_static_analysis_settings(clientObject)

    @staticmethod
    def LargeDeformation(
                  no: int = 1,
                  name: str = None,
                  iterative_method = StaticAnalysisSettingsIterativeMethodForNonlinearAnalysis.NEWTON_RAPHSON,
                  precision_of_convergence_criteria_for_nonlinear_calculation: float = 0,
                  max_number_of_iterations: float = 100,
                  number_of_load_increments: float = 1,
                  load_modification = [False, 1, False],
                  bourdon_effect: bool = True,
                  mass_conversion = [False, 0, 0, 1],
                  comment: str = '',
                  params: dict = {'save_results_of_all_load_increments': False},
                  model = Model):

        """
        Args:
            no (int): Static Analysis Setting Tag
            name (str):  Static Analysis Setting Name
            iterative_method (enum): Static Analysis Settings Iterative Method for Non-linear Analysis Enumeration
            precision_of_convergence_criteria_for_nonlinear_calculation (float): Precision of Convergence defaults to 0
            max_number_of_iterations (float): Maximum Number of Iterations
            number_of_load_increments (float): Number of Load Increments
            load_modification (list): Load Modification Parameters
                load_modification = [loading_by_multiplier_factor, multiplier_factor, dividing_results]
            bourdon_effect (bool): Bourdon Effect Boolean
            mass_conversion (list): Mass Conversion Parameters
                mass_conversion = [mass_conversion_enabled, mass_conversion_factor_in_direction_x, mass_conversion_factor_in_direction_y, mass_conversion_factor_in_direction_z]
            comment (str): Comments
            params (dict): Any WS Parameter relevant to the object and its value in form of a dictionary
            model (RSTAB Class): Model to be edited
        """

        # Client model
        clientObject = model.clientModel.factory.create('ns0:static_analysis_settings')

        # Clears object atributes | Sets all atributes to None
        clearAttributes(clientObject)

        # Static Analysis Settings No.
        clientObject.no = no

        # Name
        if name:
            clientObject.user_defined_name_enabled = True
            clientObject.name = name

        # Static Analysis Type
        clientObject.analysis_type = StaticAnalysisType.LARGE_DEFORMATIONS.name

        # Bourdon Effect Displacement
        clientObject.displacements_due_to_bourdon_effect = bourdon_effect

        # Iterative Method
        # TODO: bug 32711
        #clientObject.iterative_method_for_nonlinear_analysis = iterative_method.name

        clientObject.max_number_of_iterations = max_number_of_iterations
        clientObject.number_of_load_increments = number_of_load_increments

        # Conversion of Mass into Load
        clientObject.mass_conversion_enabled = mass_conversion[0]
        if mass_conversion[0]:
            clientObject.mass_conversion_factor_in_direction_x = mass_conversion[1]
            clientObject.mass_conversion_factor_in_direction_y = mass_conversion[2]
            clientObject.mass_conversion_factor_in_direction_z = mass_conversion[3]

        # Method for Equation System
        #clientObject.method_of_equation_system = method_of_equation_system.name

        # Modify Loading by Multiplier Factor
        if load_modification[0]:
            clientObject.modify_loading_by_multiplier_factor = True
            clientObject.loading_multiplier_factor = load_modification[1]
            clientObject.divide_results_by_loading_factor = load_modification[2]

        # Modify Standard precision and Tolerance Settings.
        if precision_of_convergence_criteria_for_nonlinear_calculation:
            clientObject.standard_precision_and_tolerance_settings_enabled = True
            clientObject.precision_of_convergence_criteria_for_nonlinear_calculation = precision_of_convergence_criteria_for_nonlinear_calculation

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        if params:
            for key in params:
                clientObject[key] = params[key]

        # Delete None attributes for improved performance
        deleteEmptyAttributes(clientObject)

        # Add Static Analysis Settings to client model
        model.clientModel.service.set_static_analysis_settings(clientObject)

    @staticmethod
    def SecondOrderPDelta(
                  no: int = 1,
                  name: str = None,
                  max_number_of_iterations: int = 100,
                  number_of_load_increments: int = 1,
                  load_modification = [False, 0, False],
                  precision_of_convergence_criteria_for_nonlinear_calculation: float = 0,
                  favorable_effect_due_to_tension_in_members : bool = False,
                  bourdon_effect: bool = True,
                  internal_forces_to_deformed_structure = [True, True, True, True],
                  mass_conversion = [False, 0, 0, 1],
                  comment: str = '',
                  params: dict = None,
                  model = Model):
        """
        Args:
            no (int): Static Analysis Setting Tag
            name (str):  Static Analysis Setting Name
            max_number_of_iterations (int): Maximum Number of Iterations
            number_of_load_increments (int): Number of Load Increments
            load_modification (list): Modify Loading by Multiplier Factor
                load_modification = [modify_loading_by_multiplier_factor, loading_multiplier_factor, divide_results_by_loading_factor]
            precision_of_convergence_criteria_for_nonlinear_calculation (float): Precision of Convergence defaults to 0
            favorable_effect_due_to_tension_in_members (bool): Favorable Effect due to Tension In Members Boolean
            bourdon_effect (bool): Bourdon Effect Boolean
            internal_forces_to_deformed_structure (list): Internal Forces to Deformed Structure List
                internal_forces_to_deformed_structure = [refer_internal_forces_to_deformed_structure, internal_forces_to_deformed_structure_for_moments, internal_forces_to_deformed_structure_for_normal_forces, internal_forces_to_deformed_structure_for_shear_forces]
            mass_conversion (list): Mass Conversion Parameters
                mass_conversion = [mass_conversion_enabled, mass_conversion_factor_in_direction_x, mass_conversion_factor_in_direction_y, mass_conversion_factor_in_direction_z]
            comment (str): Comments
            params (dict): Any WS Parameter relevant to the object and its value in form of a dictionary
            model (RSTAB Class): Model to be edited
        """

        # Client model
        clientObject = model.clientModel.factory.create('ns0:static_analysis_settings')

        # Clears object atributes | Sets all atributes to None
        clearAttributes(clientObject)

        # Static Analysis Settings No.
        clientObject.no = no

        # Name
        if name:
            clientObject.user_defined_name_enabled = True
            clientObject.name = name

        # Static Analysis Type
        clientObject.analysis_type = StaticAnalysisType.SECOND_ORDER_P_DELTA.name

        # Maximum Number of Iterations
        clientObject.max_number_of_iterations = max_number_of_iterations

        # Number of Load Increments
        clientObject.number_of_load_increments = number_of_load_increments

        # Modify Loading by Multiplier Factor
        if load_modification[0]:
            clientObject.modify_loading_by_multiplier_factor = True
            clientObject.loading_multiplier_factor = load_modification[1]
            clientObject.divide_results_by_loading_factor = load_modification[2]

        # Consider Favorable Effect due to Tension in Members
        clientObject.consider_favorable_effect_due_to_tension_in_members = favorable_effect_due_to_tension_in_members

        # Bourdon Effect Displacement
        clientObject.displacements_due_to_bourdon_effect = bourdon_effect

        # Conversion of Mass Into Load
        clientObject.mass_conversion_enabled = mass_conversion[0]
        if mass_conversion[0]:
            clientObject.mass_conversion_factor_in_direction_x = mass_conversion[1]
            clientObject.mass_conversion_factor_in_direction_y = mass_conversion[2]
            clientObject.mass_conversion_factor_in_direction_z = mass_conversion[3]

        # Iterative Method Settings
        if internal_forces_to_deformed_structure[0]:
            clientObject.refer_internal_forces_to_deformed_structure = True
            clientObject.refer_internal_forces_to_deformed_structure_for_moments = internal_forces_to_deformed_structure[1]
            clientObject.refer_internal_forces_to_deformed_structure_for_normal_forces = internal_forces_to_deformed_structure[2]
            clientObject.refer_internal_forces_to_deformed_structure_for_shear_forces = internal_forces_to_deformed_structure[3]

        # Modify Standard Precision and Tolerance Settings
        if precision_of_convergence_criteria_for_nonlinear_calculation:
            clientObject.standard_precision_and_tolerance_settings_enabled = True
            clientObject.precision_of_convergence_criteria_for_nonlinear_calculation = precision_of_convergence_criteria_for_nonlinear_calculation

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        if params:
            for key in params:
                clientObject[key] = params[key]

        # Delete None attributes for improved performance
        deleteEmptyAttributes(clientObject)

        # Add Static Analysis Settings to client model
        model.clientModel.service.set_static_analysis_settings(clientObject)
