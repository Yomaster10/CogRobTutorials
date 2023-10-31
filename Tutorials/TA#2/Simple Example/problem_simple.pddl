(define (problem simple_example)
        (:domain simple)
	(:objects
        Apple - apple
        Robot - robot
        Shelf Table - location
        )
	(:init (On Apple Shelf)(At Robot Table))

	(:goal (On Apple Table))
)