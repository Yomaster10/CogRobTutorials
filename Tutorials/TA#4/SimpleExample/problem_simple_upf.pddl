(define (problem simple-problem)
 (:domain simple-domain)
 (:objects
   robot0 - robot
   apple0 - apple
   shelf table - location
 )
 (:init (at_ robot0 table) (on apple0 shelf))
 (:goal (and (on apple0 table)))
)
