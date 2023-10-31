import unified_planning as up
from unified_planning.shortcuts import *
from unified_planning.io import PDDLWriter

def main():
    # Declaring types
    Match = UserType('Match')
    Fuse = UserType('Fuse')

    # Creating predicates (i.e. fluents)
    handfree = Fluent('handfree')
    light = Fluent('light')
    match_used = Fluent('match_used', BoolType(), m=Match)
    fuse_mended = Fluent('fuse_mended', BoolType(), f=Fuse)

    # Creating (durative) actions
    light_match = DurativeAction('light_match', m=Match)
    m = light_match.parameter('m')
    light_match.set_fixed_duration(15) # This declares the total duration of the action
    light_match.add_condition(StartTiming(), Not(match_used(m))) # This predicate must be true at the start of the action
    light_match.add_effect(StartTiming(), match_used(m), True) # This predicate will no longer be true after the start of the action
    light_match.add_effect(StartTiming(), light, True) # This predicate will no longer be true after the start of the action
    light_match.add_effect(EndTiming(), light, False) # This predicate will become true at the end of the action

    fix_fuse = DurativeAction('fix_fuse', f=Fuse)
    f = fix_fuse.parameter('f')
    fix_fuse.set_fixed_duration(10)
    fix_fuse.add_condition(StartTiming(), handfree)
    fix_fuse.add_condition(ClosedTimeInterval(StartTiming(), EndTiming()), light) # This predicate must be true over the course of the whole action
    fix_fuse.add_effect(StartTiming(), handfree, False)
    fix_fuse.add_effect(EndTiming(), fuse_mended(f), True)
    fix_fuse.add_effect(EndTiming(), handfree, True)

    # Declaring objects
    fuses = [Object(f'F{i}', Fuse) for i in range(1,4)]
    matches = [Object(f'M{i}', Match) for i in range(1,4)]

    # Loading the domain into the problem and adding objects
    problem_match = Problem('MatchCellar')
    problem_match.add_objects(fuses)
    problem_match.add_objects(matches)
    ## adding fluents (predicates) to the problem
    problem_match.add_fluent(handfree)
    problem_match.add_fluent(light)
    problem_match.add_fluent(match_used, default_initial_value=False)
    problem_match.add_fluent(fuse_mended , default_initial_value=False)
    ## adding (durative) actions to the problem
    problem_match.add_action(light_match)
    problem_match.add_action(fix_fuse)

    # Declaring the initial state
    problem_match.set_initial_value(light, False)
    problem_match.set_initial_value(handfree, True)

    # Setting the goals
    for f in fuses:
        problem_match.add_goal(fuse_mended(f))
    
    # Writing the PDDl files
    w = PDDLWriter(problem_match)
    w.write_domain('MatchCellar/domain_match_upf.pddl')
    w.write_problem('MatchCellar/problem_match_upf.pddl')

    up.shortcuts.get_env().credits_stream = None
    with OneshotPlanner(problem_kind=problem_match.kind) as planner:
        result = planner.solve(problem_match)
        plan = result.plan
        if plan is not None:
            print("%s returned:" % planner.name)
            for start, action, duration in plan.timed_actions:
                print("%s: %s [%s]" % (float(start), action, float(duration)))
        else:
            print("No plan found.")

if __name__ == '__main__':
    main()