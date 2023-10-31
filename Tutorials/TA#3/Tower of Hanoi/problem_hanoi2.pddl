(define (problem hanoi2)
        (:domain hanoi)

	(:objects d1 d2 p1 p2 p3)

	(:init (On d1 d2)(On d2 p1)(Clear d1)(Clear p2)(Clear p3)(Smaller d2 d1)
        (Smaller p1 d1)(Smaller p2 d1)(Smaller p3 d1)(Smaller p1 d2)(Smaller p2 d2)(Smaller p3 d2))

	(:goal (and (On d1 d2)(On d2 p3)))
)