#!/usr/bin/env python

# from __future__ import print_function

import os
import IPython
import pb_robot
import numpy

from Plan import Plan
from Grasp import Grasp
from RRT import RRT
from Place import Place

def execute():
    # Launch pybullet
    # pb_robot.utils.connect(use_gui=True)
    # pb_robot.utils.disable_real_time()
    # pb_robot.utils.set_default_camera()
    pb_robot.viz.draw_pose(pb_robot.geometry.pose_from_tform(numpy.eye(4)), length=0.5, width=10)

    # Create robot object
    robot = pb_robot.panda.Panda()

    # Add floor object 
    objects_path = pb_robot.helper.getDirectory("YCB_Robot")
    floor_file = os.path.join(objects_path, 'short_floor.urdf')
    floor = pb_robot.body.createBody(floor_file)

    # Add fork object
    fork_file = os.path.join(objects_path, 'fork.urdf')
    fork = pb_robot.body.createBody(fork_file)
    fork_pose = numpy.array([[1, 0, 0, 0.3],
                             [0, 0, -1, 0.2],
                             [0, 1, 0, pb_robot.placements.stable_z(fork, floor) + 0.01],
                             [0., 0., 0., 1.]])
    fork.set_transform(fork_pose)

    # Add knife object
    knife_file = os.path.join(objects_path, 'knife.urdf')
    knife = pb_robot.body.createBody(knife_file)
    knife_pose = numpy.array([[1., 0., 0., -0.4],
                              [0., 0., -1., 0.4],
                              [0., 1., 0., pb_robot.placements.stable_z(knife, floor) + 0.01],
                              [0., 0., 0., 1.]])
    knife.set_transform(knife_pose)

    # Add spoon object
    spoon_file = os.path.join(objects_path, 'spoon.urdf')
    spoon = pb_robot.body.createBody(spoon_file)
    spoon_pose = numpy.array([[1, 0, 0, 0.35],
                              [0, 0, -1, 0.4],
                              [0, 1, 0, pb_robot.placements.stable_z(spoon, floor) + 0.01],
                              [0., 0., 0., 1.]])
    spoon.set_transform(spoon_pose)

    # Add plate object
    plate_file = os.path.join(objects_path, 'plate.urdf')
    plate = pb_robot.body.createBody(plate_file)
    plate_pose = numpy.array([[0., 0., 1., 0.3],
                              [0., 1., 0., -.2],
                              [1., 0., 0., pb_robot.placements.stable_z(plate, floor)],
                              [0., 0., 0., 1.]])
    plate.set_transform(plate_pose)
    objects = {'fork': fork, 'spoon': spoon, 'knife': knife, 'plate': plate}

    # plan = Plan(robot, objects, floor)
    # plan.set_default()
    #
    # grasp = Grasp(robot, objects)
    # place = Place(robot, objects, floor)
    # # Pick
    # robot.arm.hand.Open()
    # motion = RRT(robot)
    # pick = None
    # obj = 'plate'
    # while True:
    #     # q_start = robot.arm.GetJointValues()
    #     grasp_pose, q_grasp = grasp.grasp(obj)
    #     relative_grasp = numpy.dot(numpy.linalg.inv(objects[obj].get_transform()), grasp_pose)
    #     # print(relative_grasp)
    #     grasp_in_world = numpy.dot(objects[obj].get_transform(), relative_grasp)
    #     conf = robot.arm.ComputeIK(grasp_in_world)
    #     print(robot.arm.IsCollisionFree(conf))
    #     robot.arm.SetJointValues(conf)
    #     # pick = motion.motion(q_start, conf)
    #     input('next')
    # for q in pick:
    #     robot.arm.SetJointValues(q)
    # # robot.arm.Grab(objects[obj], relative_grasp)
    # print('picked')
    # # Place
    # place_path = None
    # while True:
    #     place_pose = place.samplePlacePose(obj)
    #     relative_grasp = numpy.dot(numpy.linalg.inv(objects[obj].get_transform()), grasp_pose)
    #     q_goal = robot.arm.ComputeIK(numpy.dot(place_pose, relative_grasp))
    #     # while not robot.arm.IsCollisionFree(q_goal):
    #     #     place_pose = place.place_tsr[obj].sample()
    #     #
    #     #     relative_grasp = numpy.dot(numpy.linalg.inv(objects[obj].get_transform()), grasp_pose)
    #     #     q_goal = robot.arm.ComputeIK(numpy.dot(place_pose, relative_grasp))
    #     print(robot.arm.IsCollisionFree(q_goal))
    #     robot.arm.SetJointValues(q_goal)
    #     input('next')

    # robot.arm.hand.Close()
    #
    # for q in place:
    #     robot.arm.SetJointValues(q)
    #
    # robot.arm.Release(objects[obj])
    #
    # input('hi')

    # IPython.embed()

    # Close out Pybullet
    # pb_robot.utils.wait_for_user()
    # pb_robot.utils.disconnect()
    return objects, floor, robot
