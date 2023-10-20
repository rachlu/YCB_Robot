import random
import numpy 
import vobj
import math
import pb_robot
import time

def increment_stiffness(s1, increment, max_stiffness=None):
    s1 = numpy.array(s1)
    if not max:
        return s1 + increment
    s1 += increment
    for i in range(len(s1)):
        s1[i] = min(s1[i], max_stiffness[i])
    return s1

def execute_path(path, objects, arm):
    for action in path:
        if action.name == 'open_obj' or action.name == 'close_obj':
            cmd1 = action.args[-2]
            cmd2 = action.args[-1]
            cmd1.extend(cmd2)
            for cmd in cmd1:
                result = cmd.execute(arm)
                time.sleep(1)
                if result == False:
                    print("Failed Need to replan")
                    return
            continue
            
        for cmd in action.args[-1]:
            cmd.execute(arm)
            time.sleep(1)


def sampleTable(obj):
    r = random.choice([(-0.5, -0.3), (0.2, 0.7)])
    x = random.uniform(*r)
    r = random.choice([(-0.45, -0.25), (0.25, 0.45)])
    y = random.uniform(*r)

    # Random rotation
    angle = random.uniform(0, 2 * math.pi)
    rotate = get_rotation_arr('Z', angle)

    translation = numpy.array([[1, 0, 0, x],
                               [0, 1, 0, y],
                               [0, 0, 1, 0],
                               [0., 0., 0., 1.]])

    pose = numpy.dot(translation, rotate)
    cmd = [vobj.Pose(obj, pose)]
    return cmd


def collision_Test(robot, objects, nonmovable, q1, q2, sample, constraint=None):
    """
    Returns True if q1 to q2 is collision free.
    """
    for num in range(sample + 1):
        if constraint is not None:
            if not constraint[0](robot, q1 + (q2 - q1) / sample * num, objects[constraint[1]]):
                return False
        if not robot.arm.IsCollisionFree(q1 + (q2 - q1) / sample * num, obstacles=nonmovable):
            return False
    return True


def getDistance(q1, q2):
    """
    Returns the total radian distance from configuration q1 to configuration q2.
    """
    x = q1 - q2
    return numpy.sqrt(x.dot(x))


def get_increment(obj, start_conf, total, knob):
    """
    Given a total return the increment and number of samples to get to the specified total. Sample is an integer.
    Total = increment * sample.
    :param obj: Object being moved
    :param total: Total distance or radians the object is moved
    :return: Increment and sample (integer)
    """
    print('============ GET_INCREMENT ==============')
    print('START', start_conf, 'TOTAL', total)
    sample = 5
    increment = total/sample
    if obj == 'door':
        increment = (increment, )
    else:
        if 'top' in knob:
            increment = (increment, 0)
        else:
            increment = (0, increment)
    return increment, sample


def get_rotation_arr(axis, angle):
    if axis.upper() == 'X':
        return numpy.array([[1, 0, 0, 0],
                            [0, math.cos(angle), -math.sin(angle), 0],
                            [0, math.sin(angle), math.cos(angle), 0],
                            [0., 0., 0., 1.]])
    elif axis.upper() == 'Y':
        return numpy.array([[math.cos(angle), 0, math.sin(angle), 0],
                            [0, 1, 0, 0],
                            [-math.sin(angle), 0, math.cos(angle), 0],
                            [0., 0., 0., 1.]])
    elif axis.upper() == 'Z':
        return numpy.array([[math.cos(angle), -math.sin(angle), 0, 0],
                            [math.sin(angle), math.cos(angle), 0, 0],
                            [0, 0, 1, 0],
                            [0., 0., 0., 1.]])
    else:
        raise Exception("Invalid Axis (not XYZ)")


def collision_link_body(body1, link, body2):
    """
    Returns whether body2 is in collision with specified link of body1.
    """
    for link2 in body2.links:
        if pb_robot.collisions.pairwise_link_collision(body1, link, body2, link2):
            return True
    return False


def convert(arm, path):
    """
    :param path: list of robot configurations
    :return: list of dictionaries of robot configurations
    """
    final_path = []
    for num in range(len(path)):
        q = path[num]
        final_path.append(arm.convertToDict(q))
    return final_path


def skewMatrix(v):
    """
    Creates a 3x3 skew symmetric matrix from given 3D vector. (Credit to Rachel Holladay)
    :param v: 3D v vector
    :return: 3x3 skew symmetric matrix
    """

    skew = numpy.array([[0, -v[2], v[1]],
                        [v[2], 0, -v[0]],
                        [-v[1], v[0], 0]])
    return skew


def adjointTransform(T):
    """
    Given a Transform T in SE(3), create the adjoint representation.
    (Credit: Lynch and Park's book and Rachel Holladay)
    :param T: Homogenous Transformation in SE(3)
    :return: Adjoint 6x6 matrix representation of T
    """

    rotation = T[:3, :3]
    transform = T[:3, 3]

    adj = numpy.zeros((6, 6))
    adj[:3, :3] = numpy.dot(skewMatrix(transform), rotation)
    adj[:3, 3:6] = rotation
    adj[3:6, :3] = rotation

    return adj


def wrenchFrameTransform(w, frame):
    new_w = numpy.dot(numpy.transpose(adjointTransform(frame)), w)
    return new_w

