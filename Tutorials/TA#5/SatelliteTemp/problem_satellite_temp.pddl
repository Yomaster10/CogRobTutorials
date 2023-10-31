; This is based on the Satellite Temporal problem from AIPS 2002
(define (problem satellite_problem)
	(:domain satellite)

	(:objects
	satellite1 - satellite
	instrument1 - instrument
	thermograph1 - mode
	spectrograph1 - mode
	Star1 - direction
	Star2 - direction
	GroundStation1 - direction
	Phenomenon1 - direction
	Phenomenon2 - direction
	Phenomenon3 - direction
	)

	(:init
	(supports instrument1 thermograph1)
	(supports instrument1 spectrograph1)
	(calibration_target instrument1 GroundStation1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 Phenomenon2)
	)

	(:goal (and (have_image Phenomenon1 spectrograph1)
				(have_image Phenomenon2 spectrograph1)
				(have_image Phenomenon3 spectrograph1)
				(have_image Star1 thermograph1)
				(have_image Star2 thermograph1)
			)
	)

	(:metric minimize (total-time)) ; note: here we have the metric, which we didn't represent using the UPF
)