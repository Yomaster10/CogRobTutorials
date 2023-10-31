(define (domain hanoi)
    (:requirements :strips)

    (:predicates (On ?x ?y)(Clear ?o)(Smaller ?a ?b))

    (:action move
    :parameters (?d ?from ?to)
    :precondition (and (Clear ?d)
                       (Clear ?to)
                       (Smaller ?to ?d)
                       (On ?d ?from))
    :effect (and (On ?d ?to)
                 (Clear ?from)
                 (not (Clear ?to))
                 (not (On ?d ?from)))
    )
)