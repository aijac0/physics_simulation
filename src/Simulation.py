"""
Implementation of Simulation class and methods.
File: Simulation.py
Author: Aidan Collins
Github: aijac0
Email: aidancollinscs@gmail.com
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import EllipseCollection
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from random import uniform
from typing import Collection
import cv2
from os import system

from Space import Space


class Simulation:
    
    def __init__(self, time=300, fps=60, n_particles=30, **kwargs):
        """
        Initialize a Simulation object.
        Each parameter is either an int or a tuple.
        Tuple means that a random value within bounds will be given.

        Args:
            time (int/tuple, optional): Time to simulate, in seconds. Defaults to 300.
            fps (int/tuple, optional): Number of frames to render per second. Defaults to 60.
            n_particles (int/tuple, optional): Number of particles to simulate. Defaults to 30.
        """
        
        # Get random values if specified
        n_particles = uniform(*n_particles) if isinstance(n_particles, Collection) else n_particles
        time = uniform(*time) if isinstance(time, Collection) else time
        fps = uniform(*fps) if isinstance(fps, Collection) else fps
        
        # Attributes
        self.time = time
        self.fps = fps
        
        # Array to hold particle positions for each frame
        self.frames = np.empty((self.fps * self.time, n_particles, 2), dtype=np.float32)
        
        # Space to simulate
        self.space = Space(n_particles, **kwargs)
        
        
    def simulate(self, filename, **kwargs):
        """
        Simulate particles in space, rendering frames and storing them with specified filename.

        Args:
            filename (str): File to store rendered frames.
        """
        
        print("Simulating...")
        
        # Time to simulate for each frame
        tts = 1 / self.fps
        
        # Initialize visualization environment
        fig, ax, s, c, out = self.__init_visualize(filename, **kwargs)
        
        # Simulate each frame
        for i in range(1, len(self.frames)):
            print("Frame: " + str(i))
            
            # Elapse time in space 
            self.space.simulate(tts)
            
            # Render and store frame
            self.__visualize_frame(fig, ax, s, c, out)
            
        # Finalize visualization environment
        self.__final_visualize(out)
        
    
    def __init_visualize(self, filename, ratio=(800,800)):
        """
        Initialize frame visualization environment.

        Args:
            filename (str): File to store rendered frames.
            ratio (tuple, optional): Aspect ratio of each frame. Defaults to (800,800).

        Returns:
            tuple: figure, axis, sizes, colors, output stream
        """
        
        # Create plot
        plt.rcParams["figure.figsize"] = [ratio[0] / 100, ratio[1] / 100]
        plt.rcParams["figure.autolayout"] = True
        fig, ax = plt.subplots()
        ax.set_xlim((0, self.space.width))
        ax.set_ylim((0, self.space.height))
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_aspect('equal')
        
        # Get particle sizes
        s = [p.radius * 2 for p in self.space.particles]
        
        # Get particle colors
        c = [p.color for p in self.space.particles]
        
        # Create stream to video file
        out = cv2.VideoWriter(filename + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), self.fps, ratio)
        
        return fig, ax, s, c, out
        
        
    def __visualize_frame(self, fig, ax, s, c, out):
        """
        Visualize frame and store to output stream

        Args:
            fig (Figure): Matplotlib figure for frame
            ax (Axes): Matplotlib axis for frame
            s (list): Size of each particle
            c (list): Color of each particle
            out (VideoWriter): Output stream to write rendered frames to.
        """

        # Plot particles
        offsets = [(p.X, p.Y) for p in self.space.particles]
        pts = ax.add_collection(EllipseCollection(widths=s, heights=s, facecolor=c, angles=0, units='xy', offsets=offsets, transOffset=ax.transData))
        
        # Get plot as image
        canvas = FigureCanvas(fig)
        canvas.draw()
        image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape(canvas.get_width_height()[::-1] + (3,))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        out.write(image)
        
        # Reset plot
        pts.remove()
        
        
    def __final_visualize(self, out):
        """
        Finalize frame visualization environment.

        Args:
            out (VideoWriter): Output stream to write rendered frames to.
        """
        
        out.release()

    
if __name__ == "__main__":
    
    sim = Simulation(time=30, fps=30, n_particles=50, width=100, height=100)
    sim.simulate('example1')  