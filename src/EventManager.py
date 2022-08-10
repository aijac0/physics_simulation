"""
Implementation of EventManager class and methods.
File: EventManager.py
Author: Aidan Collins
Github: aijac0
Email: aidancollinscs@gmail.com
"""

from ParticleCollision import ParticleCollision
from BoundaryCollision import BoundaryCollision


class EventManager:
    
    def __init__(self, b_collision=True, p_collision=True, **kwargs):
        """
        Instantiate an EventManager object.

        Args:
            b_collision (bool, optional): Turn on boundary collision. Defaults to True.
            p_collision (bool, optional): Turn on particle collision. Defaults to True.
        """
        
        # Attributes
        self.events = []
        self.time = 0
        self.single_cls = []
        self.multiple_cls = []
        
        # If boundary collision is enabled
        if b_collision:
            self.single_cls.append(BoundaryCollision)
        
        # If particle collision is enabled
        if p_collision:
            self.multiple_cls.append(ParticleCollision)
        
        
    def get_events(self, particles, t, width, height):
        """
        Get the soonest events within timeframe.

        Args:
            particles (list): Particles to find events for.
            t (int): Time to find events.
            width (int): Width of space.
            height (int): Height of space.
        """
        
        # List to store events occuring at specified time
        self.events = []
        self.time = t
        
        # Iterate over every particle
        for i in range(len(particles)):
            p1 = particles[i]
            
            # Get events involving p1
            for event_cls in self.single_cls:
                self.__get_event(event_cls, [p1], width, height)
            
            # Iterate over every other particle
            for j in range(i + 1, len(particles)):
                p2 = particles[j]
                
                # Get events involving p1 and p2
                for event_cls in self.multiple_cls:
                    self.__get_event(event_cls, [p1, p2], width, height)

    
    def __get_event(self, event_cls, targets, width, height):
        """
        Get and handle the result of finding event.

        Args:
            event_cls (Event): Event to find.
            targets (tuple): Particles to find event for.
            width (int): Width of space.
            height (int): Height of space.
        """
        
        # Determine if event is possible
        is_possible, args = event_cls.is_possible(*targets, self.time, width, height)
        
        # If event is possible
        if is_possible:
            
            # Get soonest instance of event.
            event = event_cls.get_event(*targets, width, height, *args)
            
            # Determine if event occurs sooner than previously stored events.
            if event:
                if event.time < self.time:
                    self.events = [event]
                    self.time = event.time
                elif event.time == self.time:
                    self.events.append(event)