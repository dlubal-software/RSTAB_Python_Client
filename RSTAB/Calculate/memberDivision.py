from RSTAB.initModel import Model, GetAddonStatus
from RSTAB.enums import AddOn

class MemberDivision():

    def __init__(self,
                 number_of_divisions_for_result_diagram: int = 10,
                 number_of_divisions_for_special_types_of_members: int = 10,
                 number_of_divisions_for_determination_of_max_min_values: int = 10,
                 activate_member_divisions: bool = True,
                 model = Model):
        """
        The object is automaticaly created therefore we can assume that it will not be created but only updated.
        Only posititve values are recognized.

        Args:
            number_of_divisions_for_result_diagram: int = 10,
            number_of_divisions_for_special_types_of_members: int = 10,
            number_of_divisions_for_determination_of_max_min_values: int = 10,
            activate_member_divisions: bool = True,
            model = Model

        """
        # Get current member divisions
        clientObject = model.clientModel.service.get_member_divisions()

        # Number of divisions for result diagram
        clientObject.number_of_divisions_for_result_diagram = number_of_divisions_for_result_diagram

        # Number of divisions for special types of members
        clientObject.number_of_divisions_for_special_types_of_members = number_of_divisions_for_special_types_of_members

        # Number of divisions for determination of max min values
        clientObject.number_of_divisions_for_determination_of_max_min_values = number_of_divisions_for_determination_of_max_min_values

        # Activate member divisions
        clientObject.activate_member_divisions = activate_member_divisions

        # Add Mesh Settings to client model
        model.clientModel.service.set_member_divisions(clientObject)


# def set_member_divisions(all_settings, model = Model):
#     model.clientModel.service.set_member_divisions(all_settings)

def GetModelInfo(model = Model):
    return model.clientModel.service.get_model_info()

def GetMeshStatistics(model = Model):
    mesh_stats = model.clientModel.service.get_mesh_statistics()
    return model.clientModel.dict(mesh_stats)

def GenerateMesh(model = Model, skip_warnings = True):
    model.clientModel.service.generate_mesh(skip_warnings)

def GetMemberDivisions(model = Model):
    return model.clientModel.service.get_member_divisions()