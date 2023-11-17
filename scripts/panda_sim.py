from franka_interface import ArmInterface
from pddl_setup import *

import rospy
import table_env
import pb_robot
import IPython
import vobj
import util


# def reset():
#     """
#     Reset all objects to their initial conditions.
#     """
#     for obj in objects:
#         objects[obj].set_transform(init_conditions[obj])
#     for obj in list(robot.arm.grabbedObjects):
#         robot.arm.Release(robot.arm.grabbedObjects[obj])
#     robot.arm.SetJointValues(init_conditions['initial_q'])
#     path = [arm.joint_angles(), init_conditions['initial_q']]
#     path = util.convert(arm, path)
#     arm.execute_position_path(path)

def plan_solution(arm, robot, objects, openable, floor):
    max_iteration = 2
    cur_iteration = 1
    tamp = TAMP_Functions(robot, objects, floor, openable)
    minForce = [0, 0, 0, 0, 0, 0]
    while cur_iteration <= max_iteration:
        print("Starting Iteration", cur_iteration, minForce)
        arm.hand.open()
        robot.arm.hand.Open()
        result, newForce = iteration(robot, objects, tamp, arm, minForce)
        if result:
            # Completed
            return
        else:
            minForce = newForce

def iteration(robot, objects, tamp, arm, minForce):
    pddlstream_problem = pddlstream_from_tamp(robot, objects, tamp, arm, minForce)
    _, _, _, stream_map, init, goal = pddlstream_problem
    print('stream', stream_map)
    print('init', init)
    print('goal', goal)
    stream_info = {'cfree': StreamInfo(negate=True), 'cfreeholding': StreamInfo(negate=True),
                   'collisionCheck': StreamInfo(negate=True)}
    solution = solve_focused(pddlstream_problem, stream_info=stream_info, planner='ff-astar')
    print_solution(solution)
    plan, cost, evaluations = solution
    print('plan', plan)
    return util.execute_path(plan, objects, arm)

if __name__ == '__main__':
    rospy.init_node('testing_node')
    arm = ArmInterface()
    objects, openable, floor, robot = table_env.execute()
    plan = plan_solution(arm, robot, objects, openable, floor)
    if plan is None:
        print('No plan found')
    else:
        for obj in objects:
            pose = objects[obj].get_transform()
            print(obj, pose)

    # util.execute_path(plan, objects, arm) To execute plan
    IPython.embed()
    pb_robot.utils.wait_for_user()
    pb_robot.utils.disconnect()

