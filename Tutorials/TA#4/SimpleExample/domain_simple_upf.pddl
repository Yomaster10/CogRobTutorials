(define (domain simple-domain)
 (:requirements :strips :typing :negative-preconditions)
 (:types robot apple location)
 (:predicates (at_ ?robot - robot ?location - location) (on ?apple - apple ?location - location) (holding ?robot - robot ?apple - apple))
 (:action move
  :parameters ( ?r - robot ?l_from - location ?l_to - location)
  :precondition (and (at_ ?r ?l_from) (not (at_ ?r ?l_to)))
  :effect (and (at_ ?r ?l_to) (not (at_ ?r ?l_from))))
 (:action pick
  :parameters ( ?a - apple ?r - robot ?l - location)
  :precondition (and (at_ ?r ?l) (on ?a ?l) (not (holding ?r ?a)))
  :effect (and (not (on ?a ?l)) (holding ?r ?a)))
 (:action place
  :parameters ( ?a - apple ?r - robot ?l - location)
  :precondition (and (at_ ?r ?l) (not (on ?a ?l)) (holding ?r ?a))
  :effect (and (on ?a ?l) (not (holding ?r ?a))))
)
