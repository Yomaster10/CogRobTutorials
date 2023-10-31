# This code was written by Yotam Granov

import random, sys
from scipy.spatial import KDTree
from PRM_Geometry import *

def Create_Samples(map, obstacles, N_samples=100, N_knn=3):
    samples = []
    while len(samples) <= N_samples:
        tx = random.random() * map.width
        ty = random.random() * map.height
        obs_kd_tree = KDTree([o.center for o in obstacles])

        dist, idx = obs_kd_tree.query([tx, ty], k=N_knn)        
        no_col = True
        for i in range(N_knn):
            if dist[i] <= obstacles[idx[i]].radius:
                no_col = False
                break
        if no_col:
            samples.append(Node([tx,ty]))
    return samples

def Create_Roadmap(samples, obstacles, N_knn=3):
    """
    Creates the roadmap
    :param samples: list of XY positions of sampled points [m]
    :param obstacles: list of obstacles in the C-Space
    :returns: the roadmap
    """
    samples_kd_tree = KDTree([s.center for s in samples])
    N_sample = len(samples)
    roadmap = []
    PRM_graph = Graph(samples)
    for s in samples:
        edges = []; PRM_graph.graph[s] = {}
        dists, idx = samples_kd_tree.query(s.center, k=N_sample)       
        for i in range(1,N_sample):
            neighbor = samples[idx[i]]
            no_col = True
            edge = Edge(s, neighbor, cost=dists[i])
            for e in roadmap:
                if edge == e:
                    continue
            for o in obstacles:
                if edge.Check_Edge_Obstacle_Collision(o):
                    no_col = False
            if no_col:
                PRM_graph.graph[s][neighbor] = edge.cost
                roadmap.append(edge)
                edges.append(edge)
            if len(edges) >= N_knn:
                break
    return roadmap, PRM_graph

def Add_Start_Goal_To_Roadmap(roadmap, PRM_graph, start_node, goal_node, obstacles):
    samples = PRM_graph.nodes
    N_sample = len(samples)
    samples_kd_tree = KDTree([s.center for s in samples])
    PRM_graph.nodes.append(start_node)
    PRM_graph.nodes.append(goal_node)
    for s in [start_node,goal_node]:
        edges = []; PRM_graph.graph[s] = {}
        dists, idx = samples_kd_tree.query(s.center, k=N_sample)    
        for i in range(1,N_sample):
            neighbor = samples[idx[i]]
            no_col = True
            if s == start_node:
                edge = Edge(s, neighbor, cost=dists[i])
            else: 
                edge = Edge(neighbor, s, cost=dists[i])
            for e in roadmap:
                if edge == e:
                    continue
            for o in obstacles:
                if edge.Check_Edge_Obstacle_Collision(o):
                    no_col = False
            if no_col:
                if s == start_node:
                    PRM_graph.graph[s][neighbor] = edge.cost
                else:
                    PRM_graph.graph[neighbor][s] = edge.cost
                roadmap.append(edge)
                edges.append(edge)
            if len(edges) > 0:
                break
    return roadmap, PRM_graph

def Dijkstra_Algorithm(PRM_graph, start_node, goal_node, edges):
    """
    Runs Dijkstra's algorithm on the roadmap
    """
    unvisited_nodes = list(PRM_graph.nodes)
    shortest_path = {}
    previous_nodes = {}
    # We'll use max_value to initialize the "infinity" value of the unvisited nodes   
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    
    # However, we initialize the starting node's value with 0   
    shortest_path[start_node] = 0
    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes: # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        # The code block below retrieves the current node's neighbors and updates their distances
            neighbors = PRM_graph.Get_Outgoing_Edges(current_min_node)
            for neighbor in neighbors:
                tentative_value = shortest_path[current_min_node] + PRM_graph.Get_Edge_Value(current_min_node, neighbor)
                if tentative_value < shortest_path[neighbor]:# or (current_min_node == goal_node and goal_up):
                    shortest_path[neighbor] = tentative_value
                    # We also update the best path to the current node
                    previous_nodes[neighbor] = current_min_node
        unvisited_nodes.remove(current_min_node)
    
    path = []
    node = goal_node
    if node not in previous_nodes:
        print("\tPath could not be obtained...")
        return None, None, None

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    path.append(start_node)
    
    path_value = shortest_path[goal_node]
    best_path = list(reversed(path))

    best_edges = []
    for i in range(len(path)-1):
        current_edge = Get_Edge(best_path[i], best_path[i+1], edges)
        best_edges.append(current_edge)

    print(f"\tDijkstra search completed, shortest path has value {path_value:.3f}")
    return path_value, best_path, best_edges

def PRM_Solve(start_node, goal_node, samples, roadmap, PRM_graph, obstacles):
    """
    Runs PRM planning algorithm
    """
    print("Running Dijkstra's Algorithm on the Probabilistic Roadmap, with " + str(len(samples)) + " nodes left to explore...")

    new_graph = {}
    new_graph[start_node] = {}
    
    roadmap2, PRM_graph2 = Add_Start_Goal_To_Roadmap(roadmap, PRM_graph, start_node, goal_node, obstacles)
    path_value, best_path, best_edges = Dijkstra_Algorithm(PRM_graph2, start_node, goal_node, roadmap2)

    if path_value==None or best_path==None or best_edges==None:
        return None, None
    else:
        traj = []
        for i in range(len(best_edges)):
            traj.append(best_path[i])
            traj.append(best_edges[i])
        traj.append(best_path[-1])

    print("Finished running Dijkstra's Algorithm on the PRM.\n")
    return traj