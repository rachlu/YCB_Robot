import random
import numpy
import vobj
import math
import util
import pb_robot


def sampleTable(obj):
    r = random.choice([(-0.5, -0.3), (0.2, 0.7)])
    x = random.uniform(*r)
    r = random.choice([(-0.45, -0.25), (0.25, 0.45)])
    y = random.uniform(*r)

    # Random rotation
    angle = random.uniform(0, 2 * math.pi)
    # rotate = numpy.array([[math.cos(angle), -math.sin(angle), 0, 0],
    #                       [math.sin(angle), math.cos(angle), 0, 0],
    #                       [0, 0, 1, 0],
    #                       [0., 0., 0., 1.]])
    rotate = util.get_rotation_arr('Z', angle)

    translation = numpy.array([[1, 0, 0, x],
                               [0, 1, 0, y],
                               [0, 0, 1, 0],
                               [0., 0., 0., 1.]])

    pose = numpy.dot(translation, rotate)
    cmd = [vobj.Pose(obj, pose)]
    return (cmd,)


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