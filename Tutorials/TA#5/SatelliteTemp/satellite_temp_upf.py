### This problem is based on the temporal "Satellite" domain from the AIPS 2002 Competition
import unified_planning as up
from unified_planning.shortcuts import *
from unified_planning.io import PDDLWriter

def main():
    # Declaring types
    Satellite = UserType("Satellite")
    Direction = UserType("Direction")
    Instrument = UserType("Instrument")
    Mode = UserType("Mode")

    # Creating predicates (i.e. fluents)
    On_Board = Fluent("On_Board", BoolType(), i=Instrument, s=Satellite)
    Supports = Fluent("Supports", BoolType(), i=Instrument, m=Mode)
    Pointing = Fluent("Pointing", BoolType(), s=Satellite, d=Direction)
    Power_Avail = Fluent("Power_Avail", BoolType(), s=Satellite)
    Power_On = Fluent("Power_On", BoolType(), i=Instrument)
    Calibrated = Fluent("Calibrated", BoolType(), i=Instrument)
    Have_Image = Fluent("Have_Image", BoolType(), d=Direction, m=Mode)
    Calibration_Target = Fluent("Calibration_Target", BoolType(), i=Instrument, d=Direction)

    # Creating (durative) actions
    turn_to = DurativeAction('turn_to', s=Satellite, d_new=Direction, d_prev=Direction)
    s = turn_to.parameter('s')
    d_new = turn_to.parameter('d_new')
    d_prev = turn_to.parameter('d_prev')
    turn_to.set_fixed_duration(5)
    turn_to.add_condition(StartTiming(), Pointing(s, d_prev))
    turn_to.add_condition(ClosedTimeInterval(StartTiming(), EndTiming()), Not(Equals(d_new, d_prev)))
    turn_to.add_effect(EndTiming(), Pointing(s, d_new), True)
    turn_to.add_effect(StartTiming(), Pointing(s, d_prev), False)

    switch_on = DurativeAction('switch_on', i=Instrument, s=Satellite)
    i = switch_on.parameter('i')
    s = switch_on.parameter('s')
    switch_on.set_fixed_duration(2)
    switch_on.add_condition(ClosedTimeInterval(StartTiming(), EndTiming()), On_Board(i,s))
    switch_on.add_condition(StartTiming(), Power_Avail(s))
    switch_on.add_effect(EndTiming(), Power_On(i), True)
    switch_on.add_effect(StartTiming(), Power_Avail(s), False)
    switch_on.add_effect(StartTiming(), Calibrated(i), False)

    switch_off = DurativeAction('switch_off', i=Instrument, s=Satellite)
    i = switch_off.parameter('i')
    s = switch_off.parameter('s')
    switch_off.set_fixed_duration(1)
    switch_off.add_condition(ClosedTimeInterval(StartTiming(), EndTiming()), On_Board(i,s))
    switch_off.add_condition(StartTiming(), Power_On(i))
    switch_off.add_effect(StartTiming(), Power_On(i), False)
    switch_off.add_effect(EndTiming(), Power_Avail(s), True)

    calibrate = DurativeAction('calibrate', s=Satellite, i=Instrument, d=Direction)
    s = calibrate.parameter('s')
    i = calibrate.parameter('i')
    d = calibrate.parameter('d')
    calibrate.set_fixed_duration(5)
    calibrate.add_condition(ClosedTimeInterval(StartTiming(), EndTiming()), On_Board(i,s))
    calibrate.add_condition(ClosedTimeInterval(StartTiming(), EndTiming()), Calibration_Target(i,d))
    calibrate.add_condition(StartTiming(), Pointing(s, d))
    calibrate.add_condition(ClosedTimeInterval(StartTiming(), EndTiming()), Power_On(i))
    calibrate.add_condition(EndTiming(), Power_On(i))
    calibrate.add_effect(EndTiming(), Calibrated(i), True)

    take_image = DurativeAction('take_image', s=Satellite, d=Direction, i=Instrument, m=Mode)
    s = take_image.parameter('s')
    d = take_image.parameter('d')
    i = take_image.parameter('i')
    m = take_image.parameter('m')
    take_image.set_fixed_duration(7)
    take_image.add_condition(ClosedTimeInterval(StartTiming(), EndTiming()), Calibrated(i))
    take_image.add_condition(ClosedTimeInterval(StartTiming(), EndTiming()), On_Board(i,s))
    take_image.add_condition(ClosedTimeInterval(StartTiming(), EndTiming()), Supports(i,m))
    take_image.add_condition(ClosedTimeInterval(StartTiming(), EndTiming()), Power_On(i))
    take_image.add_condition(ClosedTimeInterval(StartTiming(), EndTiming()), Pointing(s,d))
    take_image.add_condition(EndTiming(), Power_On(i))    
    take_image.add_effect(EndTiming(), Have_Image(d,m), True)

    # Declaring objects
    satellite1 = Object("satellite1", Satellite)
    instrument1 = Object("instrument1", Instrument)
    thermograph1 = Object("thermograph1", Mode)
    spectrograph1 = Object("spectrograph1", Mode)
    Star1 = Object("Star1", Direction)
    Star2 = Object("Star2", Direction)
    GroundStation1 = Object("GroundStation1", Direction)
    Phenomenon1 = Object("Phenomenon1", Direction)
    Phenomenon2 = Object("Phenomenon2", Direction)
    Phenomenon3 = Object("Phenomenon3", Direction)
    objects = [satellite1, instrument1, thermograph1, spectrograph1, Star1,
               Star2, GroundStation1, Phenomenon1, Phenomenon2, Phenomenon3]

    # Loading the domain into the problem and adding objects
    problem_satellite_temp = Problem("satellite_temp")
    problem_satellite_temp.add_objects(objects)

    ## adding fluents (predicates) to the problem
    problem_satellite_temp.add_fluent(On_Board, default_initial_value=False)
    problem_satellite_temp.add_fluent(Supports, default_initial_value=False)
    problem_satellite_temp.add_fluent(Pointing, default_initial_value=False)
    problem_satellite_temp.add_fluent(Power_Avail, default_initial_value=True)
    problem_satellite_temp.add_fluent(Power_On, default_initial_value=False)
    problem_satellite_temp.add_fluent(Calibrated, default_initial_value=False)
    problem_satellite_temp.add_fluent(Have_Image, default_initial_value=False)
    problem_satellite_temp.add_fluent(Calibration_Target, default_initial_value=False)

    ## adding (durative) actions to the problem
    problem_satellite_temp.add_action(turn_to)
    problem_satellite_temp.add_action(switch_on)
    problem_satellite_temp.add_action(switch_off)
    problem_satellite_temp.add_action(calibrate)
    problem_satellite_temp.add_action(take_image)

    # Declaring the initial state
    problem_satellite_temp.set_initial_value(Supports(instrument1,thermograph1), True)
    problem_satellite_temp.set_initial_value(Supports(instrument1,spectrograph1), True)
    problem_satellite_temp.set_initial_value(Calibration_Target(instrument1,GroundStation1), True)
    problem_satellite_temp.set_initial_value(On_Board(instrument1,satellite1), True)    
    problem_satellite_temp.set_initial_value(Pointing(satellite1, Phenomenon2), True)
    
    # Setting the goals
    for p in [Phenomenon1, Phenomenon2, Phenomenon3]:
        problem_satellite_temp.add_goal(Have_Image(p, spectrograph1))
    for s in [Star1, Star2]:
        problem_satellite_temp.add_goal(Have_Image(s, thermograph1))

    # Writing the PDDl files
    w = PDDLWriter(problem_satellite_temp)
    w.write_domain('SatelliteTemp/domain_satellite_temp_upf.pddl')
    w.write_problem('SatelliteTemp/problem_satellite_temp_upf.pddl')

    # Solving the problem
    up.shortcuts.get_env().credits_stream = None
    with OneshotPlanner(name='tamer') as planner:
        result = planner.solve(problem_satellite_temp)
        plan = result.plan
        if plan is not None:
            print("%s returned:" % planner.name)
            for start, action, duration in plan.timed_actions:
                print("%s: %s [%s]" % (float(start), action, float(duration)))
        else:
            print("No plan found.")

if __name__ == '__main__':
    main()