from RSTAB.initModel import Model

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
            number_of_divisions_for_result_diagram (int): Number of divisions for result diagram,
            number_of_divisions_for_special_types_of_members (int): Number of divisions for Special Types of Members  ,
            number_of_divisions_for_determination_of_max_min_values (int): Number of divisions for determination of max min values ,
            activate_member_divisions (bool): Activate member division,
            model (RSTAB Class, optional): Model to be edited

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

def GetMemberDivisions(model = Model):
    return model.clientModel.service.get_member_divisions()
