from RRT import RRT
import numpy
from Plan import Plan
import pb_robot
import table_env
import IPython
from Grasp import Grasp
import math


if __name__ == '__main__':
    pb_robot.utils.connect(use_gui=True)
    pb_robot.utils.disable_real_time()
    pb_robot.utils.set_default_camera()

    objects, floor, robot = table_env.execute()
    # knife_pose = objects['spoon'].get_transform()
    # t_1 = numpy.array([[math.cos(math.pi / 2), -math.sin(math.pi / 2), 0, 0],
    #                    [math.sin(math.pi / 2), math.cos(math.pi / 2), 0, 0],
    #                    [0, 0, 1, 0],
    #                    [0., 0., 0., 1.]])
    # t_2 = numpy.array([[math.cos(3 * math.pi / 2), 0, math.sin(3 * math.pi / 2), 0],
    #                    [0, 1, 0, 0],
    #                    [-math.sin(3 * math.pi / 2), 0, math.cos(3 * math.pi / 2), 0],
    #                    [0., 0., 0., 1.]])
    # t_3 = numpy.array([[math.cos(math.pi / 2), -math.sin(math.pi / 2), 0, 0],
    #                    [math.sin(math.pi / 2), math.cos(math.pi / 2), 0, 0],
    #                    [0, 0, 1, 0],
    #                    [0., 0., 0., 1.]])
    # rotation = numpy.linalg.multi_dot([t_1, t_2, t_3])
    # translation = numpy.array([[1, 0, 0, 0.05],
    #                            [0, 1, 0, 0],
    #                            [0, 0, 1, -.11],
    #                            [0., 0., 0., 1.]])
    # rel = numpy.dot(rotation, translation)
    # robot.arm.SetJointValues(robot.arm.ComputeIK(numpy.dot(knife_pose, rel)))
    # robot.arm.SetJointValues(robot.arm.ComputeIK(knife_pose))
    grasp = Grasp(robot, objects)
    while True:
        robot.arm.SetJointValues(grasp.grasp('spoon')[1])
        input('next')


    IPython.embed()
    pb_robot.utils.wait_for_user()
    pb_robot.utils.disconnect()