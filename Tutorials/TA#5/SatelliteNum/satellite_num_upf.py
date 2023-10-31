### This problem is based on the numeric "Satellite" domain from the AIPS 2002 Competition
import unified_planning as up
from unified_planning.shortcuts import *
from unified_planning.io import PDDLWriter

def main():
    # Declaring types
    Satellite = UserType("Satellite")
    Direction = UserType("Direction")
    Instrument = UserType("Instrument")
    Mode = UserType("Mode")

    # Creating predicates (i.e. boolean fluents)
    On_Board = Fluent("On_Board", BoolType(), i=Instrument, s=Satellite)
    Supports = Fluent("Supports", BoolType(), i=Instrument, m=Mode)
    Pointing = Fluent("Pointing", BoolType(), s=Satellite, d=Direction)
    Power_Avail = Fluent("Power_Avail", BoolType(), s=Satellite)
    Power_On = Fluent("Power_On", BoolType(), i=Instrument)
    Calibrated = Fluent("Calibrated", BoolType(), i=Instrument)
    Have_Image = Fluent("Have_Image", BoolType(), d=Direction, m=Mode)
    Calibration_Target = Fluent("Calibration_Target", BoolType(), i=Instrument, d=Direction)

    # Creating numeric fluents
    Data_Capacity = Fluent("Data_Capacity", IntType(), s=Satellite)
    Data = Fluent("Data", IntType(), d=Direction, m=Mode)
    Slew_Time = Fluent("Slew_Time", IntType(), a=Direction, b=Direction)
    Data_Stored = Fluent("Data_Stored", IntType())
    Fuel = Fluent("Fuel", IntType(), s=Satellite)
    Fuel_Used = Fluent("Fuel_Used", IntType())

    # Creating actions
    turn_to = InstantaneousAction('turn_to', s=Satellite, d_new=Direction, d_prev=Direction)
    s = turn_to.parameter('s')
    d_new = turn_to.parameter('d_new')
    d_prev = turn_to.parameter('d_prev')
    turn_to.add_precondition(Pointing(s, d_prev))
    turn_to.add_precondition(Not(Equals(d_prev, d_new)))
    turn_to.add_precondition(GE(Fuel(s), Slew_Time(d_new, d_prev)))
    turn_to.add_effect(Pointing(s, d_new), True)
    turn_to.add_effect(Pointing(s, d_prev), False)
    turn_to.add_effect(Fuel(s), Fuel(s) - Slew_Time(d_new, d_prev))
    ## Alternate (doesn't work yet): turn_to.add_decrease_effect(Fuel(s), Slew_Time(d_new, d_prev))
    turn_to.add_effect(Fuel_Used, Fuel_Used + Slew_Time(d_new, d_prev))
    ## Alternate (doesn't work yet): turn_to.add_increase_effect(Fuel_Used, Slew_Time(d_new, d_prev))

    switch_on = InstantaneousAction('switch_on', i=Instrument, s=Satellite)
    i = switch_on.parameter('i')
    s = switch_on.parameter('s')
    switch_on.add_precondition(On_Board(i,s))
    switch_on.add_precondition(Power_Avail(s))
    switch_on.add_effect(Power_On(i), True)
    switch_on.add_effect(Calibrated(i), False)
    switch_on.add_effect(Power_Avail(s), False)

    switch_off = InstantaneousAction('switch_off', i=Instrument, s=Satellite)
    i = switch_off.parameter('i')
    s = switch_off.parameter('s')
    switch_off.add_precondition(On_Board(i,s))
    switch_off.add_precondition(Power_On(i))
    switch_off.add_effect(Power_On(i), False)
    switch_off.add_effect(Power_Avail(s), True)

    calibrate = InstantaneousAction('calibrate', s=Satellite, i=Instrument, d=Direction)
    s = calibrate.parameter('s')
    i = calibrate.parameter('i')
    d = calibrate.parameter('d')
    calibrate.add_precondition(On_Board(i,s))
    calibrate.add_precondition(Calibration_Target(i,d))
    calibrate.add_precondition(Pointing(s, d))
    calibrate.add_precondition(Power_On(i))
    calibrate.add_effect(Calibrated(i), True)

    take_image = InstantaneousAction('take_image', s=Satellite, d=Direction, i=Instrument, m=Mode)
    s = take_image.parameter('s')
    d = take_image.parameter('d')
    i = take_image.parameter('i')
    m = take_image.parameter('m')
    take_image.add_precondition(Calibrated(i))
    take_image.add_precondition(On_Board(i,s))
    take_image.add_precondition(Supports(i,m))
    take_image.add_precondition(Power_On(i))
    take_image.add_precondition(Pointing(s,d))
    take_image.add_precondition(GE(Data_Capacity(s), Data(d,m)))
    take_image.add_effect(Have_Image(d,m), True)    
    take_image.add_effect(Data_Capacity(s), Data_Capacity(s) - Data(d,m))
    ## Alternate (doesn't work yet): take_image.add_decrease_effect(Data_Capacity(s), Data(d,m))
    take_image.add_effect(Data_Stored, Data_Stored + Data(d,m))
    ## Alternate (doesn't work yet): take_image.add_increase_effect(Data_Stored, Data(d,m))

    # Declaring objects
    satellite0 = Object("satellite0", Satellite)
    instrument0 = Object("instrument0", Instrument)
    image0 = Object("image0", Mode)
    Star0 = Object("Star0", Direction)
    GroundStation1 = Object("GroundStation1", Direction)
    Phenomenon2 = Object("Phenomenon2", Direction)
    objects = [satellite0, instrument0, image0, Star0, GroundStation1, Phenomenon2]

    # Loading the domain into the problem and adding objects
    problem_satellite_num = Problem("satellite_num")
    problem_satellite_num.add_objects(objects)

    ## adding predicates (boolean fluents) to the problem
    problem_satellite_num.add_fluent(On_Board, default_initial_value=False)
    problem_satellite_num.add_fluent(Supports, default_initial_value=False)
    problem_satellite_num.add_fluent(Pointing, default_initial_value=False)
    problem_satellite_num.add_fluent(Power_Avail, default_initial_value=True)
    problem_satellite_num.add_fluent(Power_On, default_initial_value=False)
    problem_satellite_num.add_fluent(Calibrated, default_initial_value=False)
    problem_satellite_num.add_fluent(Have_Image, default_initial_value=False)
    problem_satellite_num.add_fluent(Calibration_Target, default_initial_value=False)

    ## adding numeric fluents to the problem
    problem_satellite_num.add_fluent(Data_Capacity)
    problem_satellite_num.add_fluent(Data, default_initial_value=0)
    problem_satellite_num.add_fluent(Slew_Time, default_initial_value=0)
    problem_satellite_num.add_fluent(Data_Stored, default_initial_value=0)
    problem_satellite_num.add_fluent(Fuel)
    problem_satellite_num.add_fluent(Fuel_Used, default_initial_value=0)

    ## adding actions to the problem
    problem_satellite_num.add_action(turn_to)
    problem_satellite_num.add_action(switch_on)
    problem_satellite_num.add_action(switch_off)
    problem_satellite_num.add_action(calibrate)
    problem_satellite_num.add_action(take_image)

    # Declaring the initial state (predicates)
    problem_satellite_num.set_initial_value(Supports(instrument0,image0), True)
    problem_satellite_num.set_initial_value(Calibration_Target(instrument0,GroundStation1), True)
    problem_satellite_num.set_initial_value(On_Board(instrument0,satellite0), True)
    problem_satellite_num.set_initial_value(Power_Avail(satellite0), True) # Did we need this?
    problem_satellite_num.set_initial_value(Pointing(satellite0, Phenomenon2), True)

    # Declaring the initial state (numeric fluents)
    problem_satellite_num.set_initial_value(Data_Capacity(satellite0), 550)
    problem_satellite_num.set_initial_value(Fuel(satellite0), 240)
    problem_satellite_num.set_initial_value(Data(Phenomenon2, image0), 150)
    problem_satellite_num.set_initial_value(Data(Star0, image0), 250)

    slew_dict = {Star0 : {GroundStation1 : 18, Phenomenon2 : 14},
                 GroundStation1 : {Star0 : 18, Phenomenon2 : 89},
                 Phenomenon2 : {Star0 : 14, GroundStation1 : 89}}
    for d1 in slew_dict:
        for d2 in slew_dict[d1]:
            problem_satellite_num.set_initial_value(Slew_Time(d1,d2), slew_dict[d1][d2])

    # Setting the goals
    problem_satellite_num.add_goal(Have_Image(Star0, image0))
    problem_satellite_num.add_goal(Have_Image(Phenomenon2, image0))
    
    # Writing the PDDl files
    w = PDDLWriter(problem_satellite_num)
    w.write_domain('SatelliteNum/domain_satellite_num_upf.pddl')
    w.write_problem('SatelliteNum/problem_satellite_num_upf.pddl')

    # Solving the problem
    up.shortcuts.get_env().credits_stream = None
    with OneshotPlanner(name='tamer') as planner:
        result = planner.solve(problem_satellite_num)
        plan = result.plan
        if plan is not None:
            print("%s returned:" % planner.name)
            print(plan)
            print()
            Get_Final_Values(problem_satellite_num, plan)
        else:
            print("No plan found.")
    return

def Get_Final_Values(problem, plan):
    fuel = problem.fluent("Fuel")
    slew = problem.fluent("Slew_Time")
    data_cap = problem.fluent("Data_Capacity")
    data = problem.fluent("Data")
    sat = problem.object("satellite0")
   
    fuel_left = problem.initial_value(fuel(sat))._content.payload
    data_left = problem.initial_value(data_cap(sat))._content.payload
    print(f"Initial Fuel Level: {fuel_left}, Initial Data Capacity: {data_left}")

    for a in plan.actions:
        if a.action.name == 'turn_to':
            d_new = a.actual_parameters[1]
            d_prev = a.actual_parameters[2]
            fuel_spent = problem.initial_value(slew(d_new, d_prev))._content.payload
            fuel_left -= fuel_spent
        elif a.action.name == 'take_image':
            d = a.actual_parameters[1]
            m = a.actual_parameters[3]
            data_spent = problem.initial_value(data(d, m))._content.payload
            data_left -= data_spent
    print(f"Final Fuel Level: {fuel_left}, Final Data Capacity: {data_left}")
    return

if __name__ == '__main__':
    main()