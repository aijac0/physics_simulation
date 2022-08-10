"""
Implementation of ParticleCollision class and methods.
File: ParticleCollision.py
Author: Aidan Collins
Github: aijac0
Email: aidancollinscs@gmail.com
"""

from sympy import Symbol, Eq, solve, symbols
from sympy import sqrt as symp_sqrt
from math import atan2, sin, cos, pow, sqrt, pi

from Event import Event
from Particle import Particle


class ParticleCollision(Event):

    def __init__(self, targets, time):
        """
        Instantiate a ParticleCollision object.

        Args:
            targets (list(particles)): Particles involved in event.
            
        """
        self.targets = targets
        self.time = time
        
        
    def simulate(self):
        """
        Simulate particle collision.
        """
         
        # Particles involved in collision.
        p1, p2 = self.targets[0], self.targets[1]
        
        # Length and direction of particle velocities before collision
        V1i, d1i = Particle.vector_direction(p1.Vx, p1.Vy)
        V2i, d2i = Particle.vector_direction(p2.Vx, p2.Vy) 
      
        # Angle to the axes of collision
        theta = -atan2((p1.Y - p2.Y), (p1.X - p2.X))
        
        # Velocity of particles in normal direction before collision
        Vn1i = V1i * cos(theta + d1i)
        Vn2i = V2i * cos(theta + d2i)
        
        # Velocity of particles in tangential direction
        Vt1 = V1i * sin(theta + d1i)
        Vt2 = V2i * sin(theta + d2i)
        
        # Momentum of particles in normal direction
        Pn = Vn1i * p1.mass + Vn2i * p2.mass
        
        # Kinetic energy of particles in the normal direction
        KEn = (0.5 * p1.mass * pow(V1i, 2)) + (0.5 * p2.mass * pow(V2i, 2))
        
        # Coefficients of equation to solve for velocity of particles in the normal direction after collision
        a = (pow(p2.mass, 2) + (p1.mass * p2.mass)) / p1.mass
        b = -(2 * Pn * p2.mass) / p1.mass
        c = (pow(Pn, 2) / p1.mass) + (p2.mass * pow(Vt2, 2)) + (p1.mass * pow(Vt1, 2)) - (2 * KEn)
        
        # Velocity of particles in normal direction after collision
        Vn2f = (-b - sqrt(pow(b, 2) - (4 * a * c))) / (2 * a)
        Vn1f = (Pn - (p2.mass * Vn2f)) / p1.mass
        
        # Length particle velocities after collision
        V1f = sqrt(pow(Vn1f, 2) + pow(Vt1, 2))
        V2f = sqrt(pow(Vn2f, 2) + pow(Vt2, 2))
        
        # Direction of particle velocities after collision
        d1f = atan2(Vt1, Vn1f) - theta
        d2f = atan2(Vt2, Vn2f) - theta
    
        # Get particle velocity components after collision
        p1.Vx, p1.Vy = Particle.vector_components(V1f, d1f)
        p2.Vx, p2.Vy = Particle.vector_components(V2f, d2f)


        
    @classmethod
    def is_possible(cls, p1, p2, t, width, height):
        """
        Determine if event is possible between specified particles.

        Args:
            p (Particle): Particle to find event for.
            t (float): Time to calculate possible event.
            width (int): Width of space.
            height (int): Height of space

        Returns:
            bool: Whether or not event is possible, and additional args needed for get_event().
        """
        
        # X,Y bounds over time
        min_x1, min_y1, max_x1, max_y1 = p1.get_bounds(t, width=width, height=height)
        min_x2, min_y2, max_x2, max_y2 = p2.get_bounds(t, width=width, height=height)
        
        # If bounds intersect
        x_intersect = max_x2 > min_x1 and max_x1 > min_x2
        y_intersect = max_y2 > min_y1 and max_y1 > min_y2

        # Return result
        return x_intersect and y_intersect, ()


    @classmethod
    def get_event(cls, p1, p2, *args):
        """
        Get event representing the soonest instance of collision between two particles. 

        Args:
            p1 (Particle): First particle.
            p2 (Particle): Second particle.

        Returns:
            Event: Event representing soonest collision between particles, or None.
        """
        
        # Minimum distance between particles before collision
        d = p1.radius + p2.radius 
        
        # Coefficients of equation to get time that particles collide
        a = p1.Vx ** 2 + p2.Vx ** 2 + p1.Vy ** 2 + p2.Vy ** 2 - 2 * (p1.Vx * p2.Vx + p1.Vy * p2.Vy)
        b = 2 * ((p1.X - p2.X) * (p1.Vx - p2.Vx) + (p1.Y - p2.Y) * (p1.Vy - p2.Vy))
        c = p1.X ** 2 + p2.X ** 2 + p1.Y ** 2 + p2.Y ** 2 - 2 * (p1.X * p2.X + p1.Y * p2.Y) - d ** 2
        
        # Times that particles collide
        sols = []
        
        # Result of expression under sqrt in quadratic equation
        exp = b ** 2 - (4 * a * c)
        
        # If the result of expression is non-negative
        if exp >= 0:
            
            # Results of quadratic equation
            t = (-b - sqrt(exp)) / (2 * a)
            sols.append(t) if t >= 0 else None
            t = (-b + sqrt(exp)) / (2 * a)
            sols.append(t) if t >= 0 else None
            
            # Create event if collision occured
            if sols:
                return cls([p1, p2], cls.round_down(min(sols), 5))
                 
        
if __name__ == "__main__":
    X2, Vx2, X1, Vx1, Y2, Vy2, Y1, Vy1, t, d = symbols("X2 Vx2 X1 Vx1 Y2 Vy2 Y1 Vy1 t d")
    
    eq = Eq(symp_sqrt(
        ((X2 + Vx2 * t) - (X1 + Vx1 * t)) ** 2 + 
        ((Y2 + Vy2 * t) - (Y1 + Vy1 * t)) ** 2
    ), d)
    
    print(eq.simplify())