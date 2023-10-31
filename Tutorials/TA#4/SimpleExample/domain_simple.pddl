(define (domain simple)
    (:requirements :typing :adl)

    (:types apple location robot - object)

    (:predicates (On ?a - apple ?l - location)(Holding ?r - robot ?a - apple)(At ?r - robot ?l - location))

    (:action pick
    :parameters (?a - apple ?r - robot ?l - location)
    :precondition (and (On ?a ?l)
                       (not (Holding ?r ?a))
                       (At ?r ?l))
    :effect (and (not (On ?a ?l))
                 (Holding ?r ?a))
    )

    (:action place
    :parameters (?a - apple ?r - robot ?l - location)
    :precondition (and (not (On ?a ?l))
                       (Holding ?r ?a)
                       (At ?r ?l))
    :effect (and (On ?a ?l)
                 (not (Holding ?r ?a)))
    )

    (:action move
    :parameters (?r - robot ?from ?to - location)
    :precondition (and (At ?r ?from)
                       (not (At ?r ?to)))
    :effect (and (At ?r ?to)
                 (not (At ?r ?from)))
    ) 
)