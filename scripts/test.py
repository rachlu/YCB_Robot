from RRT import *
import numpy
from Plan import Plan
import pb_robot
import table_env
import IPython
from Grasp import Grasp
import math
import vobj
from TAMP_Functions import *
from Place import Place
from Open import Open

if __name__ == '__main__':
    # pb_robot.utils.connect(use_gui=True)
    # pb_robot.utils.disable_real_time()
    # pb_robot.utils.set_default_camera()

    objects, floor, robot = table_env.execute()
    robot.arm.hand.Open()
    grasp = Grasp(robot, objects)
    tamp = TAMP_Functions(robot, objects, floor)
    q = vobj.BodyConf(robot, robot.arm.GetJointValues())
    pose = vobj.Pose('door', objects['door'].get_transform())
    result = tamp.get_open_traj('door', q, pose)[0]
    input('execute?')
    for cmd in result[0]:
        cmd.execute()
    for cmd in result[1]:
        cmd.execute()
    #rrt = RRT(robot, constraint=rotation_constraint)
    # rrt = RRT(robot, objects)
    # placable = {key: objects[key] for key in (set(objects.keys()) - {'door'})}
    # place = Place(robot, placable, floor)
    # while True:
    #     g, q = grasp.grasp('door')
    #     robot.arm.SetJointValues(q)
    #     print(robot.arm.IsCollisionFree(q))
    #     input('next')
    #
    # open = Open(robot, objects, floor)
    # q_initial = robot.arm.GetJointValues()
    # initial_grasp, q = grasp.grasp('door')
    # robot.arm.SetJointValues(q)
    # robot.arm.hand.Close()
    # relative_grasp = numpy.dot(numpy.linalg.inv(objects['door'].get_transform()), initial_grasp)
    # path = open.get_circular(q, initial_grasp)
    # while path is None:
    #     initial_grasp, q = grasp.grasp('door')
    #     robot.arm.SetJointValues(q)
    #     robot.arm.hand.Close()
    #     relative_grasp = numpy.dot(numpy.linalg.inv(objects['door'].get_transform()), initial_grasp)
    #     path = open.get_circular(q, relative_grasp)
    #     print('calucating')
    # input('do it')
    # robot.arm.Grab(objects['door'], relative_grasp)
    # for i in path[0]:
    #     i.execute()
    # while True:
    #     robot.arm.SetJointValues(q_initial)
    #     initial_grasp, q = grasp.grasp('door')
    #     robot.arm.hand.Close()
    #     relative_grasp = numpy.dot(numpy.linalg.inv(objects['door'].get_transform()), initial_grasp)
    #     robot.arm.Grab(objects['door'], relative_grasp)
    #     print(robot.arm.GetEETransform())
    #     #path = open.check_traj(q, end_grasp)
    #     path = open.get_trajectory(q, initial_grasp)
    #     path = vobj.TrajPath(robot, path)
    #     print(path.path)
    #     input('execute?')
    #     path.execute()
    #     input('next?')
    #     robot.arm.Release(objects['door'])
    # q1 = robot.arm.GetJointValues()
    # q2 = robot.arm.randomConfiguration()
    # sample = int(np.sqrt((q1 - q2).dot(q1 - q2)) / 0.5)
    # num = 1
    # while num < sample:
    #     q_new = q1 + (q2 - q1) / sample * num
    #     robot.arm.SetJointValues(q_new)
    #     input('next')
    #     num += 1
    # q1 = traj[0]
    # q2 = traj[1]
    # for num in range(10):
    #     q_new = q1 + (q2 - q1) / 9 * num
    #     robot.arm.SetJointValues(q_new)
    #     input('next')
    '''
    while True:
        t = numpy.array([[1, 0, 0, -0.5],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0.005],
                         [0., 0., 0., 1.]])
        angle = random.uniform(0, 2 * math.pi)
        rotate = numpy.array([[math.cos(angle), -math.sin(angle), 0, 0],
                              [math.sin(angle), math.cos(angle), 0, 0],
                              [0, 0, 1, 0],
                              [0., 0., 0., 1.]])
        objects['knife'].set_transform(numpy.dot(t, rotate))
        input('next')
    '''
    # while True:
    #     grasp, q = grasp.grasp('door')
    #     robot.arm.SetJointValues(q)
    #     while True:
    #         # robot.arm.hand.Close()
    #         # print(rotation_constraint2(robot, objects['bowl'].get_transform()))
    #         # pb_robot.viz.draw_tform(objects['bowl'].get_transform(), length=0.3, width=3)
    #         back = numpy.array([[1, 0, 0, 0],
    #                       [0, 1, 0, 0],
    #                       [0, 0, 1, -.05],
    #                       [0., 0., 0., 1.]])
    #         grasp = numpy.dot(grasp, back)
    #         q = robot.arm.ComputeIK(grasp, seed_q=q)
    #         robot.arm.SetJointValues(q)
    #         ans = input('next?')
    '''
    while True:
        q_start = robot.arm.GetJointValues()
        print('start', q_start)
        q_end = rrt.sample_config()
        print('goal', q_end)
        path = rrt.motion(q_start, q_end)
        print(path)
        if path is None:
            continue
        input('execute?')
        p = vobj.TrajPath(robot, path)
        p.execute()
        ans = input('next')
        if ans.upper() == 'N':
            break

    while True:
        q_start = robot.arm.GetJointValues()
        q_goal = rrt.sample_config()
        path = rrt.motion(q_start, q_goal)
        print(path)
        if path is None:
            continue
        p = vobj.TrajPath(robot, path)
        p.execute()
        input('next')
    '''
    # obj = 'bowl'
    # grasp, q = grasp.grasp(obj)
    # robot.arm.SetJointValues(q)
    # grasp = numpy.dot(numpy.linalg.inv(objects[obj].get_transform()), grasp)
    # robot.arm.Grab(objects[obj], grasp)
    # robot.arm.hand.Close()
    # tamp = TAMP_Functions(robot, objects, floor)
    # #old_pos = objects['bowl'].get_transform()
    '''
    while True:
        print()
        q = robot.arm.randomConfiguration()
        robot.arm.SetJointValues(q)
        #t = robot.arm.GetEETransform()
        #print(t)
        p = objects['bowl'].get_transform()
        pb_robot.viz.draw_tform(p, length=0.2, width=3)
        print(rotation_constraint2(robot, p))
        if input('next').upper() == 'N':
            break     
    '''
    '''    
    while True:
    #     old_pos = vobj.Pose(obj, objects[obj].get_transform())
    #     #obj_pose = sampleTable(obj, old_pos)[0][0].pose
         obj_pose = place.samplePlacePose(obj)
         world_grasp = numpy.dot(obj_pose, grasp)
         new_q = robot.arm.ComputeIK(world_grasp)
         if new_q is None:
             print('none')
             continue
         robot.arm.SetJointValues(q)
         print(rotation_constraint(robot, new_q))
         #q_start = robot.arm.GetJointValues()
         #input('goal')
         robot.arm.SetJointValues(new_q)
         #input('plan?')
         #path = vobj.TrajPath(robot, rrt.motion(q_start, new_q))
         #print(path.path)
         #if path.path is None:
             #print('no path')
             #continue
    #     for num in range(len(path.path)):
    #         print((num+1), '/', len(path.path))
    #         print(robot.arm.IsCollisionFree(path.path[num]))
         #path.execute()
         #robot.arm.SetJointValues(new_q)
         #print(robot.arm.IsCollisionFree(new_q))
         input('next')
         
         ans = input('next? (R?)')
         #while ans.upper() == 'R':
            #path.execute()
            #ans = input('next? (R?)')
    #
         if ans.upper() == 'N':
             break
         #input('next')
    #     '''
    '''
    for obj in objects:
        print(obj)
        obj_pose = place.samplePlacePose(obj)
        objects[obj].set_transform(obj_pose)
    '''
    IPython.embed()
    pb_robot.utils.wait_for_user()
    pb_robot.utils.disconnect()
