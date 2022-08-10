"""
Implementation of B_Collision class and methods.
File: BoundaryCollision.py
Author: Aidan Collins
Github: aijac0
Email: aidancollinscs@gmail.com
"""

from sympy import Symbol, Eq, solve

from Event import Event


class BoundaryCollision(Event):
    
    def __init__(self, target, time, x_hit, y_hit):
        """
        Instantiate a BoundaryCollision object.

        Args:
            target (Particle): Particle involved in event.
            x_hit (int): Whether or not particle collided with X boundary.
            y_hit (int): Whether or not particle collided with Y boundary.
        """
        self.target = target
        self.time = time
        self.x_hit = x_hit
        self.y_hit = y_hit
        
        
    def simulate(self):
        """
        Simulate boundary collision.
        """
        
        # Negate Vy if particle collided with x boundary
        if self.x_hit:
            self.target.Vx *= -1
            
        # Negate Vx if particle collided with y boundary
        if self.y_hit:
            self.target.Vy *= -1
    
    
    @classmethod
    def is_possible(cls, p, t, width, height):
        """
        Determine if boundary collision is possible.

        Args:
            p (Particle): Particle to find event for.
            t (float): Time to calculate possible event.
            width (int): Width of space.
            height (int): Height of space

        Returns:
            tuple: Whether or not event is possible, and additional args needed for get_event().
        """
        
        # X,Y bounds over time
        min_x, min_y, max_x, max_y = p.get_bounds(t)
        
        # If bounds intersect with space boundaries
        minx_inter = min_x <= 0
        miny_inter = min_y <= 0
        maxx_inter = max_x >= width
        maxy_inter = max_y >= height
        
        # Return result
        args = (minx_inter, miny_inter, maxx_inter, maxy_inter)
        return minx_inter or miny_inter or maxx_inter or maxy_inter, args
    
        
    @classmethod
    def get_event(cls, p, width, height, min_x, min_y, max_x, max_y):
        """
        Get event representing the soonest instance of particle colliding with space boundary. 

        Args:
            p (Particle): Particle to find event for.
            width (int): Width of space.
            height (int): Height of space.
            min_x (bool): If collision with minimum X boundary is possible.
            min_y (bool): If collision with minimum Y boundary is possible.
            max_x (bool): If collision with maximum X boundary is possible.
            max_y (bool): If collision with maximum Y boundary is possible.

        Returns:
            Event: Event representing soonest collision with boundary, or None.
        """
        
        # Time variable
        t = Symbol('t', positive=True)
        
        # Minimum distance between particle and boundary before collision
        d = p.radius
        
        # Times that particle collides between X,Y boundaries
        x_sols = set()
        y_sols = set()
        
        # Get time that particle collides with minimum X boundary
        if min_x:
            sol = (d - p.X) / p.Vx
            x_sols.add(sol)
                
        # Get time that particle collides with maximum X boundary
        if max_x:
            sol = (width - d - p.X) / p.Vx
            x_sols.add(sol)
        
        # Get time that particle collides with minimum Y boundary
        if min_y:
            sol = (d - p.Y) / p.Vy
            y_sols.add(sol)
                
        # Get time that particle collides with maximum Y boundary
        if max_y:
            sol = (height - d - p.Y) / p.Vy
            y_sols.add(sol)
        
        # Create event object if collision occured
        if x_sols and y_sols:
            x_sol = min(x_sols)
            y_sol = min(y_sols)
            return cls(p, cls.round_down(min(x_sol, y_sol), 3), x_sol <= y_sol, y_sol <= x_sol)
        elif x_sols:
            return cls(p, cls.round_down(min(x_sols), 3), True, False)
        elif y_sols:
            return cls(p, cls.round_down(min(y_sols), 3), False, True)