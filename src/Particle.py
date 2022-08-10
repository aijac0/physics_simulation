"""
Implementation of Particle class and methods.
File: Particle.py
Author: Aidan Collins
Github: aijac0
Email: aidancollinscs@gmail.com
"""

from math import cos, sin, pi, atan2, pow, sqrt
from random import uniform, choice
from typing import Collection


class Particle:
    
    def __init__(self, color, mass, radius, X, Y, Vx, Vy):
        """
        Instantiate a Particle object.

        Args:
            id (int): Particle identifier.
            radius (float): Radius of particle.
            mass (float): Mass of particle.
            X (float): X position of particle.
            Y (float): Y position of particle.
            Vx (float): X velocity of particle.
            Vy (float): Y velocity of particle.
        """
        
        self.color = color
        self.mass = mass
        self.radius = radius
        self.X, self.Y = X, Y
        self.Vx, self.Vy = Vx, Vy

    
    def simulate(self, tts):
        """
        Update vectors of particle after passing a specified time.

        Args:
            tts (float): Specified time to pass.
        """
        
        # Update X,Y position
        self.X, self.Y = self.get_position(tts)
        
        
    def get_position(self, t):
        """
        Get position of particle after passing a specified time.

        Args:
            t (float): Specified time to pass.

        Returns:
            tuple: Final X,Y position
        """
        
        # Final X,Y position
        Xf = self.X + self.Vx * t
        Yf = self.Y + self.Vy * t
        return Xf, Yf
    
    
    def get_bounds(self, t, width=None, height=None):
        """
        Get the boundaries of the path of a particle over time.

        Args:
            t (float): Time over which to get path.
            width (int, optional): Width of space. Defaults to None.
            height (int, optional): Height of space. Defaults to None.

        Returns:
            tuple: min_X, min_Y, max_X, max_Y
        """
        
        # Final position
        Xf, Yf = self.get_position(t)
        
        # X,Y bounds over time
        min_X, max_X = (self.X - self.radius, Xf + self.radius) if self.X < Xf else (Xf - self.radius, self.X + self.radius)
        min_Y, max_Y = (self.Y - self.radius, Yf + self.radius) if self.Y < Yf else (Yf - self.radius, self.Y + self.radius)
        
        # Update values with bounds if applicable
        if width:
            min_X = max(min_X, 0)
            max_X = min(max_X, width)
        if height:
            min_Y = max(min_Y, 0)
            max_Y= min(max_Y, height)
        
        return min_X, min_Y, max_X, max_Y
    
    
    @classmethod
    def vector_components(cls, length, direction):
        """
        Get the X,Y components of a vector given length and direction.

        Args:
            length (float): Length of vector.
            direction (float): Direction of vector, in radians.

        Returns:
            tuple: X_component, Y_component
        """
        
        return length * cos(direction), length * sin(direction)
    
    @classmethod
    def vector_direction(cls, X, Y):
        """
        Get the vector length and direction from X,Y components.

        Args:
            X (float): Vector X component
            Y (float): Vector Y component

        Returns:
            tuple: length, direction
        """
        
        # Length of vector
        length = sqrt(pow(X, 2) + pow(Y, 2))

        # Direction of vector in radians
        direction = atan2(Y, X)
        
        return length, direction
    
    
    @classmethod
    def particle_generator(cls, n_particles, width, height, color_r=['b','c','m','y','r'],
                           density_r=(0.8,1.2), volume_r=(5,15), energy_r=(1500,2500), direction_r=(0,2*pi), **kwargs):
        """
        Generator for Particle objects with specified parameters.
        Each parameter is either a float or a tuple.
        Tuple means that a random value within bounds will be given.

        Args:
            X_r (tuple): X position of particle.
            Y_r (tuple): Y position of particle.
            mass_r (tuple, optional): Mass of particle. Defaults to 5.
            radius_r (tuple, optional): Radius of particle. Defaults to (5,10).
            vel_r (tuple, optional): Length of velocity vector. Defaults to (5, 20).
            direction_r (tuple, optional): Direction of vectors. Defaults to (0,2*pi).

        Yields:
            Particle: Generated particle
        """
        
        # Divide space into equal grids for each particle
        w, h = cls.__factorize(n_particles, width / height)
        x_grid, y_grid = width // w, height // h
        X_r, Y_r = [0, x_grid], [0, y_grid]
        
        # Repeat particle generation indefinitely
        while True:
            
            # Get random values from parameters
            color = choice(color_r)
            volume = uniform(*volume_r)
            density = uniform(*density_r)
            energy = uniform(*energy_r)
            direction = uniform(*direction_r)
            
            # Translate random values into particle arguments
            radius = sqrt(volume / pi)
            mass = density * volume
            vel = sqrt((2 * energy) / mass)
            
            # Get particle position; continue if particle volume is too large for grid
            curr_X_r = X_r[0] + radius, X_r[1] - radius
            curr_Y_r = Y_r[0] + radius, Y_r[1] - radius
            if curr_X_r[0] > curr_X_r[1] or curr_Y_r[0] > curr_Y_r[1]:
                continue
            X = uniform(*curr_X_r)
            Y = uniform(*curr_Y_r)
            
            # Get vector components from length and direction
            Vx, Vy = cls.vector_components(vel, direction)
            
            # Yield particle
            p = cls(color, mass, radius, X, Y, Vx, Vy)
            yield p
            
            # Get next parameters
            if X_r[1] == width:
                X_r[0], X_r[1] = 0, x_grid
                Y_r[0] = Y_r[1]
                Y_r[1] += y_grid
            else:
                X_r[0] = X_r[1]
                X_r[1] += x_grid
                
                
    @classmethod
    def __factorize(cls, n, ratio):
        """
        Get the factors a,b of 'n' where a/b is closest to 'ratio'.

        Args:
            n (int): Number to get the factors of.
            ratio (float): Ratio of factors to get closest to.

        Returns:
            tuple: Factors of n.
        """
        
        # Initial factors
        factors = (1, n)
        
        # Iterate over every integer from 2 to n-1
        for a in range(2, n):
            
            # If n is evenly divisible by a, get n / a
            if n % a == 0:
                b = n // a
                
                # Determine if a / b is closer to ratio than the previously stored factors
                if abs(a / float(b) - ratio) < abs(factors[0] / float(factors[1]) - ratio):
                    factors = (a, b)
        
        return factors