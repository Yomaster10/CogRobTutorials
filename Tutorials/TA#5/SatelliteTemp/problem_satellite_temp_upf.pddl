(define (problem satellite_temp-problem)
 (:domain satellite_temp-domain)
 (:objects
   satellite1 - satellite
   instrument1 - instrument
   thermograph1 spectrograph1 - mode
   star1 star2 groundstation1 phenomenon1 phenomenon2 phenomenon3 - direction
 )
 (:init (supports instrument1 thermograph1) (supports instrument1 spectrograph1) (calibration_target instrument1 groundstation1) (on_board instrument1 satellite1) (pointing satellite1 phenomenon2) (power_avail satellite1))
 (:goal (and (have_image phenomenon1 spectrograph1) (have_image phenomenon2 spectrograph1) (have_image phenomenon3 spectrograph1) (have_image star1 thermograph1) (have_image star2 thermograph1)))
)
