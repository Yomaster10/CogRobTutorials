# This code was written by Yotam Granov

import matplotlib.pyplot as plt
from PRM_Geometry import *
from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')

class Plotter:
    def __init__(self, map, obstacles, start, goal, samples, roadmap, PRM_graph, trajectory, axis=None):
        self.map = map
        self.obstacles = obstacles
        self.goal = goal
        self.start = start
        self.samples = samples
        self.roadmap = roadmap
        self.PRM_graph = PRM_graph
        self.trajectory = trajectory
        self.ax = axis
    
    def plot_init(self, axis=None):
        """
        Plots the initial image (.png) of the map, including obstacles, goal zones, and the starting point
        :param axis: axis of the subplot to add the plot to
        """
        if axis is None:
            _, axis = plt.subplots()
        axis.set_ylim(0,self.map.height)
        axis.set_xlim(0,self.map.width)
        axis.set_title('Initial Map (C-Space)')
        axis.set_ylabel('y [m]')
        axis.set_xlabel('x [m]')

        # plotting the map, obstacles, and goal zones
        self.map.plot_rectangle(axis)
        for o in self.obstacles:
            o.plot_circle(axis)
        self.start.plot_node(axis)
        self.goal.plot_node(axis)

        plt.show()
        return

    def plot_PRM(self, axis=None):
        """
        Plots the map (.png or .gif) after the PRM is generated, including the initial map contents as well as the sampled points and the edges of the roadmap
        :param axis: axis of the subplot to add the plot to
        """
        if axis is None:
            _, axis = plt.subplots()
        axis.set_ylim(0,self.map.height)
        axis.set_xlim(0,self.map.width)
        axis.set_title('Probabilistic Roadmap')
        axis.set_ylabel('y [m]')
        axis.set_xlabel('x [m]')

        # plotting the map, obstacles, and goal zones
        self.map.plot_rectangle(axis)
        for o in self.obstacles:
            o.plot_circle(axis)
        self.start.plot_node(axis)
        self.goal.plot_node(axis)

        # plotting all the nodes (including the start and goal nodes)
        for idx_s, s in enumerate(self.samples):
            s.plot_node(axis)
            xlabel_string = 'x [m]       Nodes: ' + str(idx_s+1) + ' / ' + str(len(self.samples))
            axis.set_xlabel(xlabel_string)
            if len(self.samples) < 100:
                plt.pause(0.001)
            elif len(self.samples) >= 100:
                if idx_s % 10 == 0 or idx_s == len(self.samples) - 1:
                    plt.pause(0.001)

        # plotting all the edges
        for idx_e, e in enumerate(self.roadmap):
            e.plot_edge(axis)
            e.Highlight_Nodes(axis)
            xlabel_string_new = xlabel_string + ', Edges: ' + str(idx_e+1) + ' / ' + str(len(self.roadmap))
            axis.set_xlabel(xlabel_string_new)
            if len(self.roadmap) < 200:
                plt.pause(0.001)
            elif len(self.roadmap) >= 200 and len(self.roadmap) < 1000:
                if idx_e == len(self.roadmap) - 1:
                    axis.set_xlabel(xlabel_string_new + ', Plotting Complete!')   
                if idx_e % 20 == 0 or idx_e == len(self.roadmap) - 1:
                    plt.pause(0.001)
            elif len(self.roadmap) >= 1000:
                if idx_e == len(self.roadmap) - 1:
                    axis.set_xlabel(xlabel_string_new )   
                if idx_e % 200 == 0 or idx_e == len(self.roadmap) - 1:
                    plt.pause(0.001)
        plt.show()
        return

    def plot_Dijkstra(self, axis=None, clean=False):
        """
        Plots the map showing the paths obtained by the Dijkstra algorithm, including those paths, the PRM (optinal), and the initial map contents
        :param axis: axis of the subplot to add the plot to
        :param clean: if True, then only the Dijkstra paths are shown, otherwise the whole PRM is shown as well
        """
        if axis is None:
            _, axis = plt.subplots()
        axis.set_ylim(0,self.map.height)
        axis.set_xlim(0,self.map.width)
        if clean:
            axis.set_title('Final C-Space Trajectory')
        else:
            axis.set_title('PRM with Dijkstra Path')
        axis.set_ylabel('y [m]')
        axis.set_xlabel('x [m]')

        # plotting the map, obstacles, and goal zones
        self.map.plot_rectangle(axis)
        for o in self.obstacles:
            o.plot_circle(axis)
        self.start.plot_node(axis)
        self.goal.plot_node(axis)
        if not clean: # show the original PRM, else show only the shortest paths
            for s in self.samples:
                s.plot_node(axis)
            for e in self.roadmap:
                e.plot_edge(axis)

        # plotting the solution trajectory (including the start and goal nodes)
        axis.set_xlabel('x [m]')
        for o in self.trajectory:
            if isinstance(o,Node):
                if not isinstance(o,Start_Node) and not isinstance(o,Goal_Node):
                    o.plot_node(axis, color='yellow')
                else:
                    o.plot_node(axis)
            elif isinstance(o,Edge):
                o.plot_edge(axis, color='yellow')
            plt.pause(0.001)
        plt.show()
        return

    def plot_final(self):
        self.plot_Dijkstra(clean=False)
        self.plot_Dijkstra(clean=True)
        return