from RSTAB.enums import CoordinateSystemType
from RSTAB.initModel import Model, clearAttributes, deleteEmptyAttributes

class CoordinateSystem():
    def __init__(self,
             no: int = 1,
             type = CoordinateSystemType.TYPE_GLOBAL_XYZ,
             parameter: list = None,
             name: str = None,
             comment: str = '',
             params: dict = None,
             model = Model):

        '''
        Args:
            no (int): Coordinate System Tag
            type (enum): Coordinate System Type Enumeration
            parameter (int or Enum): Coordinate System Type Parameter
                for type == CoordinateSystemType.TYPE_OFFSET_XYZ:
                    parameter = [offset_coordinate_x, offset_coordinate_y, offset_coordinate_z]
                for type == CoordinateSystemType.TYPE_3_POINTS:
                    parameter = [origin_coordinate_x, origin_coordinate_y, origin_coordinate_z, u_axis_point_coordinate_x, u_axis_point_coordinate_y, u_axis_point_coordinate_z, uw_plane_point_coordinate_x, uw_plane_point_coordinate_y, uw_plane_point_coordinate_z]
                for type == CoordinateSystemType.TYPE_2_POINTS_AND_ANGLE:
                    parameter = [origin_coordinate_x, origin_coordinate_y, origin_coordinate_z, u_axis_point_coordinate_x, u_axis_point_coordinate_y, u_axis_point_coordinate_z, uw_plane_angle]
                for type == CoordinateSystemType.TYPE_POINT_AND_3_ANGLES:
                    parameter = [origin_coordinate_x, origin_coordinate_y, origin_coordinate_z, rotation_angles_sequence enumeration, rotation_angle_1, rotation_angle_2, rotation_angle_3]
            name (str): User Defined Name
            comment (str, optional): Comment
            params (dict, optional): Any WS Parameter relevant to the object and its value in form of a dictionary
            model (RSTAB Class, optional): Model to be edited
        '''

        # Client model | CoordinateSystem
        clientObject = model.clientModel.factory.create('ns0:coordinate_system')

        # Clears object attributes | Sets all attributes to None
        clearAttributes(clientObject)

        # CoordinateSystem No.
        clientObject.no = no

        # CoordinateSystem type
        clientObject.type = type.name

        # For CoordinateSystem Type Offset XYZ
        if type == CoordinateSystemType.TYPE_OFFSET_XYZ:
            clientObject.origin_coordinate_x = parameter[0]
            clientObject.origin_coordinate_y = parameter[1]
            clientObject.origin_coordinate_z = parameter[2]

        # For CoordinateSystem Type 3 Points
        elif type == CoordinateSystemType.TYPE_3_POINTS:
            clientObject.origin_coordinate_x = parameter[0]
            clientObject.origin_coordinate_y = parameter[1]
            clientObject.origin_coordinate_z = parameter[2]
            clientObject.u_axis_point_coordinate_x = parameter[3]
            clientObject.u_axis_point_coordinate_y = parameter[4]
            clientObject.u_axis_point_coordinate_z = parameter[5]
            clientObject.uw_plane_point_coordinate_x = parameter[6]
            clientObject.uw_plane_point_coordinate_y = parameter[7]
            clientObject.uw_plane_point_coordinate_z = parameter[8]

        # For CoordinateSystem Type 2 Points and Angle
        elif type == CoordinateSystemType.TYPE_2_POINTS_AND_ANGLE:
            clientObject.origin_coordinate_x = parameter[0]
            clientObject.origin_coordinate_y = parameter[1]
            clientObject.origin_coordinate_z = parameter[2]
            clientObject.u_axis_point_coordinate_x = parameter[3]
            clientObject.u_axis_point_coordinate_y = parameter[4]
            clientObject.u_axis_point_coordinate_z = parameter[5]
            clientObject.uw_plane_angle = parameter[6]

        # For CoordinateSystem Type Point and 3 Angles
        elif type == CoordinateSystemType.TYPE_POINT_AND_3_ANGLES:
            clientObject.origin_coordinate_x = parameter[0]
            clientObject.origin_coordinate_y = parameter[1]
            clientObject.origin_coordinate_z = parameter[2]
            clientObject.rotation_angles_sequence = parameter[3].name
            clientObject.rotation_angle_1 = parameter[4]
            clientObject.rotation_angle_2 = parameter[5]
            clientObject.rotation_angle_3 = parameter[6]

        # CoordinateSystem User Defined Name
        if name:
            clientObject.user_defined_name_enabled = True
            clientObject.name = name

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        if params:
            for key in params:
                clientObject[key] = params[key]

        # Delete None attributes for improved performance
        deleteEmptyAttributes(clientObject)

        # Add CoordinateSystem to client model
        model.clientModel.service.set_coordinate_system(clientObject)
