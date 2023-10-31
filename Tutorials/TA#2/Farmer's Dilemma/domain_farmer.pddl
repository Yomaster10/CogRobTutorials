(define (domain farmer)
    (:requirements :typing :adl :universal-preconditions)  

    (:types boat location good - object
            fox chicken seed - good
    )

    (:predicates (at ?o - object ?l - location)(on-boat ?g - good ?b - boat)(boat-clear ?b - boat) )

    (:action load
       :parameters (?g - good ?l - location ?b - boat)
       :precondition (and (at ?g ?l)
                          (at ?b ?l)
                          (boat-clear ?b))
       :effect (and (on-boat ?g ?b)
                    (not (boat-clear ?b))
                    (not (at ?g ?l)))
    )

    (:action sail
       :parameters (?from ?to - location ?b - boat ?f - fox ?c - chicken ?s - seed)
       :precondition (and (at ?b ?from)
                          (forall (?l - location)
                              (and (not (and (at ?f ?l)
                                        (at ?c ?l)))
                                   (not (and (at ?c ?l)
                                        (at ?s ?l))))
                          )
                     )
       :effect (and (at ?b ?to)
                    (not (at ?b ?from)))
    )

    (:action unload
       :parameters (?g - good ?l - location ?b - boat)
       :precondition (and (on-boat ?g ?b)
                          (at ?b ?l)
                          (not (boat-clear ?b)))
       :effect (and (at ?g ?l)
                    (boat-clear ?b)
                    (not (on-boat ?g ?b)))
    )
)