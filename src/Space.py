"""
Implementation of Space class and methods
File: Space.py
Author: Aidan Collins
Github: aijac0
Email: aidancollinscs@gmail.com
"""

from random import uniform
from typing import Collection
from math import sqrt

from Particle import Particle
from EventManager import EventManager


class Space:
    
    def __init__(self, n_particles, width=500, height=500, **kwargs):
        """
        Create a 2D particle space.
        Each optional parameter is either an int or a tuple.
        Tuple means that a random value within bounds will be given.

        Args:
            n_particles (int): Number of particles in space.
            height (int/tuple, optional): Size of Y dimension. Defaults to 500.
            width (int/tuple, optional): Size of X dimension. Defaults to 500.
        """
        
        # Get random values if specified
        width = uniform(*width) if isinstance(width, Collection) else width
        height = uniform(*height) if isinstance(height, Collection) else height
        
        # Attributes
        self.n_particles = n_particles
        self.width = width
        self.height = height
        self.manager = EventManager(self, **kwargs)
        
        # Create particles
        self.__create_particles(**kwargs)
               
    
    def simulate(self, tts):
        """
        Simulate particles in space for specified time.

        Args:
            tts (int): Time to simulate.
        """
        
        # Repeatedly simulate events until tts is 0
        while tts > 0:
            
            # Get the next events to occur
            self.manager.get_events(self.particles, tts, self.width, self.height)
            
            # Proceed simulation until event
            for p in self.particles:
                p.simulate(self.manager.time)
            tts -= self.manager.time
                
            # Simulate events
            for event in self.manager.events:
                event.simulate()
                                 
                            
    def __create_particles(self, **kwargs):
        """
        Create particles to fill space.
        """
        
        # Create list to hold particles
        self.particles = [None] * self.n_particles
        
        # Create particle generator
        p_gen = Particle.particle_generator(self.n_particles, self.width, self.height, **kwargs)
        
        # Iteratively generate new particles
        for i in range(self.n_particles):
            self.particles[i] = p_gen.__next__()
                    
                    
if __name__ == "__main__":
    n = 24
    ratio = 1/5
    
    factors = Space.factorize(n, ratio)
    print(factors)