# This code was written by Yotam Granov

import random
from PRM_Geometry import *
from PRM_MotionPlanner import *
from PRM_Plotter import *

def Create_Obstacles(N_obs):
    """
    Creates the obstacles for our problem
    :param N_obs: the number of obstacles to instantiate
    :returns: list of the obstacle instances
    """
    obs = []
    for _ in range(N_obs):
        r = random.randint(2, 10)
        x = random.randint(0+r, 100-r)
        y = random.randint(0+r, 100-r)
        obs.append(Obstacle(r,[x,y]))
    return obs

def Create_Start_Node(obs):
    """
    Creates the start node for our problem
    :param obs: list of the obstacle instances in our problem
    :param goals: list of the goal zone instances
    :returns: the start node instance
    """
    start_not_found = True
    while start_not_found:
        start_not_found = False
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        start = Start_Node([x,y])
        for o in obs:
            if not Check_Point_Not_In_Circle(start,o):
                start_not_found = True
                continue
    return start

def Create_Goal_Node(obs):
    """
    Creates the goal node for our problem
    :param obs: list of the obstacle instances in our problem
    :returns: the goal node instance
    """
    goal_not_found = True
    while goal_not_found:
        goal_not_found = False
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        goal = Goal_Node([x,y])
        for o in obs:
            if not Check_Point_Not_In_Circle(goal,o):
                goal_not_found = True
                continue
    return goal

def main():
    N_samples = 200
    N_obs = random.randint(5, 20)

    map = Map()
    obs = Create_Obstacles(N_obs)
    start = Create_Start_Node(obs)
    goal = Create_Goal_Node(obs)
        
    samples = Create_Samples(map, obs, N_samples=N_samples)
    roadmap, PRM_graph = Create_Roadmap(samples, obs, N_knn=5)
    trajectory = PRM_Solve(start, goal, samples, roadmap, PRM_graph, obs)
 
    plotter = Plotter(map, obs, start, goal, samples, roadmap, PRM_graph, trajectory)
    plotter.plot_init()
    plotter.plot_PRM()
    plotter.plot_final()
    return

if __name__ == '__main__':
    main()