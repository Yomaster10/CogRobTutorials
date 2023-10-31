(define (problem satellite_num-problem)
 (:domain satellite_num-domain)
 (:objects
   satellite0 - satellite
   instrument0 - instrument
   image0 - mode
   star0 groundstation1 phenomenon2 - direction
 )
 (:init (supports instrument0 image0) (calibration_target instrument0 groundstation1) (on_board instrument0 satellite0) (power_avail satellite0) (pointing satellite0 phenomenon2) (= (data_capacity satellite0) 550) (= (fuel satellite0) 240) (= (data phenomenon2 image0) 150) (= (data star0 image0) 250) (= (slew_time star0 groundstation1) 18) (= (slew_time star0 phenomenon2) 14) (= (slew_time groundstation1 star0) 18) (= (slew_time groundstation1 phenomenon2) 89) (= (slew_time phenomenon2 star0) 14) (= (slew_time phenomenon2 groundstation1) 89) (= (data groundstation1 image0) 0) (= (slew_time star0 star0) 0) (= (slew_time groundstation1 groundstation1) 0) (= (slew_time phenomenon2 phenomenon2) 0) (= (data_stored) 0) (= (fuel_used) 0))
 (:goal (and (have_image star0 image0) (have_image phenomenon2 image0)))
)
