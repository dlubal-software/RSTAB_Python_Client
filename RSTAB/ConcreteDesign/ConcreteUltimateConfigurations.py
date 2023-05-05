from RSTAB.initModel import Model, clearAttributes, deleteEmptyAttributes, ConvertToDlString


class ConcreteUltimateConfiguration():

    def __init__(self,
                no: int = 1,
                name: str = 'ULS',
                members: str = 'All',
                member_sets: str = 'All',
                comment: str = '',
                params: dict = None,
                model = Model):
        """
        Args:
            no (int): Configuration Tag
            name (str): User Defined Name
            members (str): Assigned Members
            member_sets (str): Assigned Member Sets
            comment (str, optional): Comment
            params (dict, optional): Any WS Parameter relevant to the object and its value in form of a dictionary
            model (RSTAB Class, optional): Model to be edited
        """

        # Client model | Concrete Durabilities
        clientObject = model.clientModel.factory.create('ns0:concrete_design_uls_configuration')

        # Clears object atributes | Sets all atributes to None
        clearAttributes(clientObject)

        # Concrete Durability No.
        clientObject.no = no

        # User Defined Name
        if name:
            clientObject.user_defined_name_enabled = True
            clientObject.name = name

        # Assigned Members
        if members == 'All':
            clientObject.assigned_to_all_members = True

        else:
            clientObject.assigned_to_all_members = False
            clientObject.assigned_to_members = ConvertToDlString(members)

        # Assigned Member Sets
        if member_sets == 'All':
            clientObject.assigned_to_all_member_sets = True

        else:
            clientObject.assigned_to_all_member_sets = False
            clientObject.assigned_to_member_sets = ConvertToDlString(member_sets)

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        if params:
            for key in params:
                clientObject[key] = params[key]

        # Delete None attributes for improved performance
        deleteEmptyAttributes(clientObject)

        # Add Global Parameter to client model
        model.clientModel.service.set_concrete_design_uls_configuration(clientObject)
