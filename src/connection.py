import pymunk


def get_shape(x, y, space):
    # See if we clicked on anything
    shape_list = space.point_query((x, y), 1, pymunk.ShapeFilter())

    # If we did, remember what we clicked on
    if len(shape_list) > 0:
        shape = shape_list[0]
    else:
        shape = None
    return shape


def make_pin_joint_connection(x, y, space, joints, shape_1, shape_2):
    if get_shape(x, y, space) is None:
        return
    if shape_1 is None:
        print("Shape 1 Found")
        shape_1 = get_shape(x, y, space)
    elif shape_2 is None:
        print("Shape 2 Found")
        shape_2 = get_shape(x, y, space)
        joint = pymunk.PinJoint(shape_1.shape.body, shape_2.shape.body)
        space.add(joint)
        joints.append(joint)
        shape_1 = None
        shape_2 = None
        print("Joint Connection Made")
    return shape_1, shape_2


def make_damped_spring_connection(x, y, space, joints, shape_1, shape_2):
    if get_shape(x, y, space) is None:
        return
    if shape_1 is None:
        print("Shape 1 Found")
        shape_1 = get_shape(x, y, space)
    elif shape_2 is None:
        print("Shape 2 Found")
        shape_2 = get_shape(x, y, space)
        joint = pymunk.DampedSpring(shape_1.shape.body, shape_2.shape.body, (0, 0), (0, 0), 45, 300, 30)
        space.add(joint)
        joints.append(joint)
        shape_1 = None
        shape_2 = None
        print("Spring Connection Made")
    return shape_1, shape_2
