import warnings
warnings.simplefilter("ignore", UserWarning)
import unified_planning as up
from unified_planning.shortcuts import *
from unified_planning.io import PDDLWriter

def main():
    # Declaring types
    Drone = UserType("Drone")
    Location = UserType("Location")
    Good = UserType("Good")
    Customer = UserType("Customer", father=Location)
    Warehouse = UserType("Warehouse", father=Location)
    Sugar = UserType("Sugar", father=Good)
    Milk = UserType("Milk", father=Good)

    # Creating predicates
    Drone_At = Fluent("Drone_At", BoolType(), drone=Drone, location=Location)
    Holding = Fluent("Holding", BoolType(), drone=Drone, good=Good)
    Clear = Fluent("Clear", BoolType(), drone=Drone)
    Customer_Wants = Fluent("Customer_Wants", BoolType(), customer=Customer, good=Good)
    Adjacent = Fluent("Adjacent", BoolType(), l1=Location, l2=Location)
    Warehouse_Has = Fluent("Warehouse_Has", BoolType(), warehouse=Warehouse, good=Good)

    # Creating actions
    fly = InstantaneousAction("fly", d=Drone, l_from=Location, l_to=Location)
    l_from = fly.parameter("l_from")
    l_to = fly.parameter("l_to")
    d = fly.parameter("d")
    fly.add_precondition(Drone_At(d,l_from))
    fly.add_precondition(Adjacent(l_from,l_to))
    fly.add_precondition(Not(Drone_At(d,l_to)))
    fly.add_effect(Drone_At(d,l_to),True)
    fly.add_effect(Drone_At(d,l_from),False)

    load = InstantaneousAction("load", d=Drone, g=Good, w=Warehouse)
    d = load.parameter("d")
    g = load.parameter("g")
    w = load.parameter("w")
    load.add_precondition(Drone_At(d,w))
    load.add_precondition(Clear(d))
    load.add_precondition(Warehouse_Has(w,g))
    load.add_precondition(Not(Holding(d,g)))
    load.add_effect(Holding(d,g),True)
    load.add_effect(Clear(d),False)

    unload = InstantaneousAction("unload", d=Drone, g=Good, c=Customer)
    d = unload.parameter("d")
    g = unload.parameter("g")
    c = unload.parameter("c")
    unload.add_precondition(Drone_At(d,c))
    unload.add_precondition(Customer_Wants(c,g))
    unload.add_precondition(Holding(d,g))
    unload.add_precondition(Not(Clear(d)))
    unload.add_effect(Holding(d,g),False)
    unload.add_effect(Customer_Wants(c,g),False)
    unload.add_effect(Clear(d),True)

    # Declaring objects
    drones = [Object(f"D{i}", Drone) for i in range(1,4)]
    customers = [Object(f"C{i}", Customer) for i in range(1,10)]
    warehouses = [Object(f"W{i}", Warehouse) for i in range(1,3)]
    sugar0 = Object("sugar0", Sugar)
    milk0 = Object("milk0", Milk)

    # Loading the domain into the problem and adding objects
    problem_drones = Problem("drones")
    problem_drones.add_objects(drones)
    problem_drones.add_objects(customers)
    problem_drones.add_objects(warehouses)
    problem_drones.add_objects([sugar0,milk0])
    problem_drones.add_fluent(Drone_At, default_initial_value=False)
    problem_drones.add_fluent(Holding, default_initial_value=False)
    problem_drones.add_fluent(Clear, default_initial_value=True)
    problem_drones.add_fluent(Customer_Wants, default_initial_value=False)
    problem_drones.add_fluent(Adjacent, default_initial_value=False)
    problem_drones.add_fluent(Warehouse_Has, default_initial_value=False)
    problem_drones.add_action(fly)
    problem_drones.add_action(load)
    problem_drones.add_action(unload)

    # Declaring the initial state
    problem_drones.set_initial_value(Drone_At(drones[0],warehouses[0]), True)
    problem_drones.set_initial_value(Drone_At(drones[1],warehouses[1]), True)
    problem_drones.set_initial_value(Drone_At(drones[2],customers[5]), True)
    problem_drones.set_initial_value(Warehouse_Has(warehouses[1],milk0), True)
    problem_drones.set_initial_value(Warehouse_Has(warehouses[0],sugar0), True)
    problem_drones.set_initial_value(Customer_Wants(customers[2],milk0), True)
    problem_drones.set_initial_value(Customer_Wants(customers[6],sugar0), True)
    problem_drones.set_initial_value(Customer_Wants(customers[6],milk0), True)
    problem_drones.set_initial_value(Customer_Wants(customers[7],sugar0), True)

    adjacency_dict = {'C1':['W1'], 'C2':['W1'], 'C3':['C5'], 'C4':['C5','C7'], 'C5':['C3','C4','C8','W1'], 'C6':['C8'], 'C7':['C4','W2'],
    'C8':['C5','C6','C9','W2'], 'C9':['C8'], 'W1':['C1','C2','C5'], 'W2':['C7','C8']}

    locations = [i for i in customers]
    locations.extend(warehouses)
    for l1 in locations:
        for l2 in locations:
            if l2.name in adjacency_dict[l1.name]:
                problem_drones.set_initial_value(Adjacent(l1,l2), True)

    # Setting the goals
    problem_drones.add_goal(Not(Customer_Wants(customers[2],milk0)))
    problem_drones.add_goal(Not(Customer_Wants(customers[6],sugar0)))
    problem_drones.add_goal(Not(Customer_Wants(customers[6],milk0)))
    problem_drones.add_goal(Not(Customer_Wants(customers[7],sugar0)))

    # Writing the PDDl files
    w = PDDLWriter(problem_drones)
    w.write_domain('Drones/domain_drones_upf.pddl')
    w.write_problem('Drones/problem_drones_upf.pddl')

    # Solving the problem
    up.shortcuts.get_env().credits_stream = None
    with OneshotPlanner(name='fast-downward-opt') as planner:
        result = planner.solve(problem_drones)
        plan = result.plan
        if plan is not None:
            print("%s returned:" % planner.name)
            print(plan)
        else:
            print("No plan found.")
    return

if __name__ == '__main__':
    main()