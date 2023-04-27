(define (domain table-tamp)
    (:requirements :strips :equality)
    (:predicates
        (Conf ?q)
        (AtConf ?q)
        (ObjState ?o ?s)
        (AtObjState ?o ?s)
        (Grasp ?o ?g)
        (On ?o ?r)
        (Kin ?o ?p ?g ?q ?t)
	    (KinOpen ?o ?c ?g ?q1 ?q2 ?t)
        (Holding ?o)
        (HandEmpty)
        (UprightObj ?o)
        (Trajectory ?q1 ?q2 ?t)
        (Traj ?t)
        (UnSafeTraj ?t)
        (CFreeTraj ?t ?o ?g)
        (Trajectory_Holding ?o ?g ?q1 ?q2 ?t)
        (Trajectory_Holding_Upright ?o ?g ?q1 ?q2 ?t)
        (Traj_Holding ?t ?o ?g)
        (UnSafeHolding ?t ?o ?g)
        (CFreeHolding ?t ?o ?g ?o2 ?p)
        (Region ?r)
        (Supported ?o ?p ?r)
        (AtGrasp ?o ?g)
        (InCollision ?o ?p)
        (Safe ?o ?p ?o2 ?p2)
        (CanMove)
        (Openable ?o)
        (Open ?o ?h)
        (Close ?o ?h)
        (Open_Traj ?o ?g ?q1 ?q2 ?c1 ?c2 ?h ?t1 ?t2)
        (Close_Traj ?o ?g ?q1 ?q2 ?c1 ?c2 ?h ?t1 ?t2)
        (OpenEnough ?o ?q ?h)
        (OpenGrasp ?o ?g ?h)
        (CloseGrasp ?o ?g ?h)
        (Placeable ?o)
	    (Graspable ?o)
	    (HoldingOpenable ?o ?h)
	    (Handle ?o ?h)
	    (ValidStateTransition ?o ?q1 ?q2 ?k)
	    (ValidCloseTransition ?o ?q1 ?q2 ?h)
	)

    (:action move_free
        :parameters (?q1 ?q2 ?t)
        :precondition (and (Trajectory ?q1 ?q2 ?t)
                            (Conf ?q1)
                            (Conf ?q2)
                            (AtConf ?q1)
                            (HandEmpty)
                            (not (UnSafeTraj ?t))
                      	    (CanMove))
        :effect (and (AtConf ?q2) (not (AtConf ?q1)) (not (CanMove)))
    )

    (:action move_holding
        :parameters (?o ?g ?q1 ?q2 ?t)
        :precondition (and (Trajectory_Holding ?o ?g ?q1 ?q2 ?t)
                            (Conf ?q1)
                            (Conf ?q2)
                            (AtConf ?q1)
                            (Grasp ?o ?g)
                            (AtGrasp ?o ?g)
                            (not (UnSafeHolding ?t ?o ?g))
                            (CanMove)
                            (not (UprightObj ?o))
                            )
        :effect (and (AtConf ?q2) (not (AtConf ?q1)) (not (CanMove)))
    )

    (:action move_holding_upright
        :parameters (?o ?g ?q1 ?q2 ?t)
        :precondition (and (Trajectory_Holding_Upright ?o ?g ?q1 ?q2 ?t)
                            (Conf ?q1)
                            (Conf ?q2)
                            (AtConf ?q1)
                            (Grasp ?o ?g)
                            (AtGrasp ?o ?g)
                            (not (UnSafeHolding ?t ?o ?g))
                            (CanMove)
                            (UprightObj ?o)
                            )
        :effect (and (AtConf ?q2) (not (AtConf ?q1)) (not (CanMove)))
    )

    (:action open_obj
        :parameters (?o ?c1 ?c2 ?g ?q1 ?q2 ?h ?t1 ?t2)
        :precondition (and (Openable ?o)
                            (OpenGrasp ?o ?g ?h)
                            (Conf ?q1)
                            (Conf ?q2)
                            (AtConf ?q1)
                            (ValidStateTransition ?o ?c1 ?c2 ?h)
                            (ObjState ?o ?c1)
                            (AtObjState ?o ?c1)
                            (ObjState ?o ?c2)
                            (Open_Traj ?o ?g ?q1 ?q2 ?c1 ?c2 ?h ?t1 ?t2)
                            (not (UnSafeHolding ?t2 ?o ?g))
                            (not (UnSafeTraj ?t1))
			    )
        :effect (and (HandEmpty) (AtObjState ?o ?c2) (not (AtObjState ?o ?c1)) (AtConf ?q2) (not (AtConf ?q1)) 
                    (CanMove) (not (Close ?o ?h)))
    )

    (:action close_obj
        :parameters (?o ?c1 ?c2 ?g ?q1 ?q2 ?h ?t1 ?t2)
        :precondition (and (Openable ?o)
                            (CloseGrasp ?o ?g ?h)
                            (Conf ?q1)
                            (Conf ?q2)
                            (AtConf ?q1)
                            (ValidCloseTransition ?o ?c1 ?c2 ?h)
                            (ObjState ?o ?c1)
                            (ObjState ?o ?c2)
                            (AtObjState ?o ?c1)
                            (Close_Traj ?o ?g ?q1 ?q2 ?c1 ?c2 ?h ?t1 ?t2)
                            (not (UnSafeHolding ?t2 ?o ?g))
                            (not (UnSafeTraj ?t1))
        )
        :effect (and (AtObjState ?o ?c2) (not (AtObjState ?o ?c1)) (AtConf ?q2) (not (AtConf ?q1)) (CanMove)
                     (Close ?o ?h) (HandEmpty))
    )

    (:action grab
        :parameters (?o ?p ?g ?q ?t)
        :precondition (and (HandEmpty)
                          (Conf ?q)
                          (AtConf ?q)
                          (Kin ?o ?p ?g ?q ?t)
                          (ObjState ?o ?p)
                          (AtObjState ?o ?p)
                          (Grasp ?o ?g)
                          (Placeable ?o)
                          (not (UnSafeHolding ?t ?o ?g))
                          )
        :effect (and (not (HandEmpty)) (not (AtObjState ?o ?p)) (AtGrasp ?o ?g) (CanMove))
    )

    (:action place
        :parameters (?o ?p ?g ?q ?t)
        :precondition (and (Placeable ?o)
                          (ObjState ?o ?p)
                          (Conf ?q)
                          (AtConf ?q)
                          (Kin ?o ?p ?g ?q ?t)
                          (Grasp ?o ?g)
                          (AtGrasp ?o ?g)
                          (not (InCollision ?o ?p))
                          (not (UnSafeHolding ?t ?o ?g)))
        :effect (and (HandEmpty) (AtObjState ?o ?p) (not (AtGrasp ?o ?g)) (CanMove))
    )

    (:derived (On ?o ?r)
        (exists (?p) (and (Region ?r) (ObjState ?o ?p) (AtObjState ?o ?p) (Supported ?o ?p ?r)))
    )

    (:derived (Holding ?o)
        (exists (?g) (and (Graspable ?o) (Grasp ?o ?g) (AtGrasp ?o ?g)))
    )

    (:derived (InCollision ?o ?p)
        (exists (?o2 ?p2) (and (ObjState ?o2 ?p2) (AtObjState ?o2 ?p2) (not (Safe ?o ?p ?o2 ?p2))))
    )

    (:derived (UnSafeTraj ?t)
        (exists (?o ?p) (and (ObjState ?o ?p) (AtObjState ?o ?p) (not (CFreeTraj ?t ?o ?p))))
    )

    (:derived (UnSafeHolding ?t ?o ?g)
        (exists (?o2 ?p) (and (Grasp ?o ?g) (ObjState ?o2 ?p) (AtGrasp ?o ?g) (AtObjState ?o2 ?p) (not (CFreeHolding ?t ?o ?g ?o2 ?p))))
    )

    (:derived (Open ?o ?h)
        (exists (?p) (and (Openable ?o) (Handle ?o ?h) (ObjState ?o ?p) (AtObjState ?o ?p) (OpenEnough ?o ?p ?h)))
    )
)
