(define (problem drones-problem)
 (:domain drones-domain)
 (:objects
   d1 d2 d3 - drone
   c1 c2 c3 c4 c5 c6 c7 c8 c9 - customer
   w1 w2 - warehouse
   sugar0 - sugar
   milk0 - milk
 )
 (:init (drone_at d1 w1) (drone_at d2 w2) (drone_at d3 c6) (warehouse_has w2 milk0) (warehouse_has w1 sugar0) (customer_wants c3 milk0) (customer_wants c7 sugar0) (customer_wants c7 milk0) (customer_wants c8 sugar0) (adjacent c1 w1) (adjacent c2 w1) (adjacent c3 c5) (adjacent c4 c5) (adjacent c4 c7) (adjacent c5 c3) (adjacent c5 c4) (adjacent c5 c8) (adjacent c5 w1) (adjacent c6 c8) (adjacent c7 c4) (adjacent c7 w2) (adjacent c8 c5) (adjacent c8 c6) (adjacent c8 c9) (adjacent c8 w2) (adjacent c9 c8) (adjacent w1 c1) (adjacent w1 c2) (adjacent w1 c5) (adjacent w2 c7) (adjacent w2 c8) (clear d1) (clear d2) (clear d3))
 (:goal (and (not (customer_wants c3 milk0)) (not (customer_wants c7 sugar0)) (not (customer_wants c7 milk0)) (not (customer_wants c8 sugar0))))
)
