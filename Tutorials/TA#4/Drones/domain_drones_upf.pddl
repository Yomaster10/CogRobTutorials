(define (domain drones-domain)
 (:requirements :strips :typing :negative-preconditions)
 (:types
    drone location good - object
    sugar milk - good
    customer warehouse - location
 )
 (:predicates (drone_at ?drone - drone ?location - location) (holding ?drone - drone ?good - good) (clear ?drone - drone) (customer_wants ?customer - customer ?good - good) (adjacent ?l1 - location ?l2 - location) (warehouse_has ?warehouse - warehouse ?good - good))
 (:action fly
  :parameters ( ?d - drone ?l_from - location ?l_to - location)
  :precondition (and (drone_at ?d ?l_from) (adjacent ?l_from ?l_to) (not (drone_at ?d ?l_to)))
  :effect (and (drone_at ?d ?l_to) (not (drone_at ?d ?l_from))))
 (:action load
  :parameters ( ?d - drone ?g - good ?w - warehouse)
  :precondition (and (drone_at ?d ?w) (clear ?d) (warehouse_has ?w ?g) (not (holding ?d ?g)))
  :effect (and (holding ?d ?g) (not (clear ?d))))
 (:action unload
  :parameters ( ?d - drone ?g - good ?c - customer)
  :precondition (and (drone_at ?d ?c) (customer_wants ?c ?g) (holding ?d ?g) (not (clear ?d)))
  :effect (and (not (holding ?d ?g)) (not (customer_wants ?c ?g)) (clear ?d)))
)
