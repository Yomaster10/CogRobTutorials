import unified_planning as up
from unified_planning.shortcuts import *
from unified_planning.io import PDDLWriter

def main():
    # Declaring types
    Apple = UserType("Apple")
    Robot = UserType("Robot")
    Location = UserType("Location")

    # Creating predicates
    At = Fluent("At", BoolType(), robot=Robot, location=Location)
    On = Fluent("On", BoolType(), apple=Apple, location=Location)
    Holding = Fluent("Holding", BoolType(), robot=Robot, apple=Apple)

    # Creating actions
    move = InstantaneousAction("move", r=Robot, l_from=Location, l_to=Location)
    l_from = move.parameter("l_from")
    l_to = move.parameter("l_to")
    r = move.parameter("r")
    move.add_precondition(At(r,l_from))
    move.add_precondition(Not(At(r,l_to)))
    move.add_effect(At(r,l_to),True)
    move.add_effect(At(r,l_from),False)

    pick = InstantaneousAction("pick", a=Apple, r=Robot, l=Location)
    a = pick.parameter("a")
    r = pick.parameter("r")
    l = pick.parameter("l")
    pick.add_precondition(At(r,l))
    pick.add_precondition(On(a,l))
    pick.add_precondition(Not(Holding(r,a)))
    pick.add_effect(On(a,l),False)
    pick.add_effect(Holding(r,a),True)

    place = InstantaneousAction("place", a=Apple, r=Robot, l=Location)
    a = pick.parameter("a")
    r = pick.parameter("r")
    l = pick.parameter("l")
    place.add_precondition(At(r,l))
    place.add_precondition(Not(On(a,l)))
    place.add_precondition(Holding(r,a))
    place.add_effect(On(a,l),True)
    place.add_effect(Holding(r,a),False)

    # Declaring objects
    robot0 = Object("robot0", Robot)
    apple0 = Object("apple0", Apple)
    shelf = Object("shelf", Location)
    table = Object("table", Location)

    # Loading the domain into the problem and adding objects
    problem_simple = Problem("simple")
    problem_simple.add_objects([robot0,apple0,shelf,table])
    problem_simple.add_fluent(At, default_initial_value=False)
    problem_simple.add_fluent(On, default_initial_value=False)
    problem_simple.add_fluent(Holding, default_initial_value=False)
    problem_simple.add_action(move)
    problem_simple.add_action(pick)
    problem_simple.add_action(place)

    # Declaring the initial state
    problem_simple.set_initial_value(At(robot0,table), True)
    problem_simple.set_initial_value(On(apple0,shelf), True)

    # Setting the goals
    problem_simple.add_goal(On(apple0,table))

    # Writing the PDDl files
    w = PDDLWriter(problem_simple)
    w.write_domain('SimpleExample/domain_simple_upf.pddl')
    w.write_problem('SimpleExample/problem_simple_upf.pddl')

    # Solving the problem
    up.shortcuts.get_env().credits_stream = None
    with OneshotPlanner(name='fast-downward') as planner:
        result = planner.solve(problem_simple)
        plan = result.plan
        if plan is not None:
            print("%s returned:" % planner.name)
            print(plan)
        else:
            print("No plan found.")
    return

if __name__ == '__main__':
    main()