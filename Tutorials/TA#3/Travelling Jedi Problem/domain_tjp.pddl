(define (domain tjp)
 (:requirements :strips :negative-preconditions :universal-preconditions)

 (:predicates (At ?l) (Adjacent ?l1 ?l2) (Visited ?l) )

 (:action fly
  :parameters (?l_from ?l_to)
  :precondition (and (At ?l_from)(Adjacent ?l_from ?l_to)(not (Visited ?l_to)))
  :effect (and (At ?l_to)(not (At ?l_from))(Visited ?l_to))
 )
)