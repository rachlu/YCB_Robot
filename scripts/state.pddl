(define (domain table-tamp)
    (:requirements :strips :equality)
    (:predicates
        (Conf ?q)
        (Pose ?p)
        (GraspPose ?o ?p)
        ;(PlacePose ?o ?g ?p)
        (AtConf ?q)
        (AtPose ?o ?p)
        (On ?o ?r)
        (Kin ?q ?p)
        (Holding ?o)
        (HandEmpty)
        (Graspable ?o)
        (CF-Trajectory ?q1 ?q2 ?t)
        (Placed ?o)
        (Region ?r)
        (Supported ?o ?p)
    )

    (:action move
        :parameters (?q1 ?q2 ?t)
        :precondition (and (CF-Trajectory ?q1 ?q2 ?t)
                            (Conf ?q1)
                            (Conf ?q2)
                            (AtConf ?q1))
        :effect (and (AtConf ?q2) (not (AtConf ?q1)))
    )

    (:action grab
        :parameters (?o ?p1 ?p2 ?q)
        :precondition (and (HandEmpty)
                          (AtConf ?q)
                          (Kin ?q ?p2)
                          (AtPose ?o ?p1)
                          (Pose ?p2)
                          (GraspPose ?o ?p2)
                          (Graspable ?o))
        :effect (and (Holding ?o) (not (HandEmpty)) (not (AtPose ?o ?p1)))
    )

    (:action place
        :parameters (?o ?p ?g ?q)
        :precondition (and (not (HandEmpty))
                          (AtConf ?q)
                          (Kin ?q ?p)
                          (Pose ?p)
                          (Holding ?o)
                          (GraspPose ?o ?g))
        :effect (and (not (Holding ?o)) (HandEmpty) (AtPose ?o ?p))
    )

    (:derived (On ?o ?r)
        (exists (?p) (and (Region ?r) (AtPose ?o ?p) (Supported ?o ?p)))
    )
)

    (:stream cfree
        :inputs (?t ?o ?p)
        :domain (and (ObjPose ?o ?p) (Traj ?t))
        :certified (CFree ?t ?o ?p)
    )

    (:stream cfreeholding
        :inputs (?t ?o ?g ?o2 ?p)
        :domain (and (ObjPose ?o ?p) (Traj_Holding ?t ?o ?g))
        :certified (CFreeHolding ?t ?o ?g ?o2 ?p)
    )

    (:derived (UnSafeTraj ?t)
        (exists (?o ?p) (and (AtPose ?o ?p) (not (CFree ?t ?o ?p))))
    )

    (:derived (UnSafeTrajHolding ?t ?o ?g)
        (exists (?o2 ?p) (and (AtGrasp ?o ?g) (AtPose ?o ?p) (not (CFreeHolding ?t ?o ?g ?o2 ?p))))
    )
