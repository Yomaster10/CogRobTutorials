# This code was partly written by Oren Salzman and Dean Zadok, and partly by Yotam Granov and Niv Ostroff

import itertools
from matplotlib import pyplot as plt
from shapely.geometry import mapping
from shapely.geometry.polygon import Polygon, LineString

class Plotter:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()

    def add_obstacles(self, obstacles):
        for obstacle in obstacles:
            self.ax.add_patch(plt.Polygon(obstacle.exterior.coords, color='b'))

    def add_robot(self, point, distance_to_vertex):
        x, y = point
        self.distance_to_vertex = distance_to_vertex
        target = Polygon([(x - distance_to_vertex, y), (x, y + distance_to_vertex), (x + distance_to_vertex, y), (x, y - distance_to_vertex)])
        self.ax.add_patch(plt.Polygon(target.exterior.coords, color='r'))

    def add_goal(self, point, distance_to_vertex):
        x, y = point
        self.distance_to_vertex = distance_to_vertex
        target = Polygon([(x - distance_to_vertex, y), (x, y + distance_to_vertex), (x + distance_to_vertex, y), (x, y - distance_to_vertex)])
        self.ax.add_patch(plt.Polygon(target.exterior.coords, color='g'))

    def add_visibility_graph(self, edges):
        for edge in edges:
            plt.plot(list(edge.xy[0]), list(edge.xy[1]), color='black', linestyle='dashed')

    def add_shortest_path(self, edges):
        if len(edges) > 0:
            current_vertex = edges[0]
            for edge in edges[1:]:
                plt.plot([current_vertex[0], edge[0]], [current_vertex[1], edge[1]], color='yellow', linewidth=5,
                        alpha=0.4)
                self.add_robot(edge, self.distance_to_vertex)
                current_vertex = edge

    def show_graph(self):
        plt.autoscale()
        plt.show()

def Create_Visibility_Graph(obstacles, source=None, dest=None):
    """
    Constructs the visibility graph of a given map
    :param obstacles: A list of the obstacles in the map
    :param source: The starting position of the robot
    :param dest: The destination of the query
    :return: A list of LineStrings holding the edges of the visibility graph
    """
    # First, we add the vertices of all the obstacles to the graph
    vertices = []; lines = []
    for poly in obstacles:
        for i in mapping(poly)['coordinates']:
            for x in i:
                vertices.append(x)

    # Next, we add the start and goal nodes to the graph if they're given as inputs
    if source is not None:
        vertices.append(source)
    if dest is not None:
        vertices.append(dest)

    # Finally, we iterate over all pairs of vertices in the graph, and connect an edge between them if they are mutually visible
    for pair in itertools.combinations(vertices, 2):
        intersects = False
        line = LineString(pair)
        for poly in obstacles:
            if (line.covered_by(poly) or line.crosses(poly)): # collision-checking
                intersects = True
                break
        if not intersects: # the two vertices are mutually visible
            lines.append(line)
    return lines