; This is based on the Satellite Numeric problem from AIPS 2002
(define (problem satellite_num_problem)
	(:domain satellite_num)

	(:objects
		satellite0 - satellite
		instrument0 - instrument
		image0 - mode
		Star0 - direction
		GroundStation1 - direction
		Phenomenon2 - direction
	)

	(:init
		(supports instrument0 image0)
		(calibration_target instrument0 GroundStation1)
		(on_board instrument0 satellite0)
		(power_avail satellite0)
		(pointing satellite0 Phenomenon2)
		(= (data_capacity satellite0) 550)
		(= (fuel satellite0) 240)
		(= (data Phenomenon2 image0) 150)
		(= (data Star0 image0) 250)
		(= (slew_time GroundStation1 Star0) 18)
		(= (slew_time Star0 GroundStation1) 18)
		(= (slew_time Phenomenon2 Star0) 14)
		(= (slew_time Star0 Phenomenon2) 14)
		(= (slew_time Phenomenon2 GroundStation1) 89)
		(= (slew_time GroundStation1 Phenomenon2) 89)
		(= (data-stored) 0)
		(= (fuel-used) 0)
	)
	
	(:goal (and (have_image Star0 image0)
				(have_image Phenomenon2 image0)
		   )
	)

	(:metric minimize (fuel-used))
)