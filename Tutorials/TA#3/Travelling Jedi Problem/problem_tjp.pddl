(define (problem tjp_problem)
 (:domain tjp)

 (:objects Tatooine Hoth Naboo Dagobah Coruscant Endor_Moon Death_Star)

 (:init (At Tatooine)(Adjacent Tatooine Hoth)(Adjacent Hoth Tatooine)(Adjacent Tatooine Dagobah)(Adjacent Dagobah Tatooine)(Adjacent Tatooine Coruscant)(Adjacent Coruscant Tatooine)
        (Adjacent Naboo Hoth)(Adjacent Hoth Naboo)(Adjacent Hoth Coruscant)(Adjacent Coruscant Hoth)(Adjacent Endor_Moon Dagobah)(Adjacent Dagobah Endor_Moon)(Adjacent Coruscant Death_Star)(Adjacent Death_Star Coruscant)
        (Adjacent Endor_Moon Death_Star)(Adjacent Death_Star Endor_Moon)(Adjacent Naboo Dagobah)(Adjacent Dagobah Naboo)(Adjacent Dagobah Coruscant)(Adjacent Coruscant Dagobah)
 )

 (:goal (and (At Tatooine)(forall (?l)(Visited ?l))))
)