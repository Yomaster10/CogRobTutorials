(define (problem farmers_dilemma)
        (:domain farmer)
        
	(:objects
        Fox - fox
        Chicken - chicken
        Seed - seed
        Boat - boat
        Left_Bank Right_Bank - location
        )

	(:init
        (at Fox Left_Bank)(at Chicken Left_Bank)(at Seed Left_Bank)
        (at Boat Left_Bank)(boat-clear Boat)
        )

	(:goal (and (at Fox Right_Bank)
                    (at Chicken Right_Bank)
                    (at Seed Right_Bank)
                    (at Boat Right_Bank)
                )
        )
)