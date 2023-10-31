(define (domain satellite_num-domain)
 (:requirements :strips :typing :negative-preconditions :equality :numeric-fluents)
 (:types satellite instrument mode direction)
 (:predicates (on_board ?i - instrument ?s - satellite) (supports ?i - instrument ?m - mode) (pointing ?s - satellite ?d - direction) (power_avail ?s - satellite) (power_on ?i - instrument) (calibrated ?i - instrument) (have_image ?d - direction ?m - mode) (calibration_target ?i - instrument ?d - direction))
 (:functions (data_capacity ?s - satellite) (data ?d - direction ?m - mode) (slew_time ?a - direction ?b - direction) (data_stored) (fuel ?s - satellite) (fuel_used))
 (:action turn_to
  :parameters ( ?s - satellite ?d_new - direction ?d_prev - direction)
  :precondition (and (pointing ?s ?d_prev) (not (= ?d_prev ?d_new)) (<= (slew_time ?d_new ?d_prev) (fuel ?s)))
  :effect (and (pointing ?s ?d_new) (not (pointing ?s ?d_prev)) (assign (fuel ?s) (- (fuel ?s) (slew_time ?d_new ?d_prev))) (assign (fuel_used) (+ (slew_time ?d_new ?d_prev) (fuel_used)))))
 (:action switch_on
  :parameters ( ?i - instrument ?s - satellite)
  :precondition (and (on_board ?i ?s) (power_avail ?s))
  :effect (and (power_on ?i) (not (calibrated ?i)) (not (power_avail ?s))))
 (:action switch_off
  :parameters ( ?i - instrument ?s - satellite)
  :precondition (and (on_board ?i ?s) (power_on ?i))
  :effect (and (not (power_on ?i)) (power_avail ?s)))
 (:action calibrate
  :parameters ( ?s - satellite ?i - instrument ?d - direction)
  :precondition (and (on_board ?i ?s) (calibration_target ?i ?d) (pointing ?s ?d) (power_on ?i))
  :effect (and (calibrated ?i)))
 (:action take_image
  :parameters ( ?s - satellite ?d - direction ?i - instrument ?m - mode)
  :precondition (and (calibrated ?i) (on_board ?i ?s) (supports ?i ?m) (power_on ?i) (pointing ?s ?d) (<= (data ?d ?m) (data_capacity ?s)))
  :effect (and (have_image ?d ?m) (assign (data_capacity ?s) (- (data_capacity ?s) (data ?d ?m))) (assign (data_stored) (+ (data ?d ?m) (data_stored)))))
)
