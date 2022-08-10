"""
Implementation of abstract Event class and methods.
File: Event.py
Author: Aidan Collins
Github: aijac0
Email: aidancollinscs@gmail.com
"""

from abc import ABC, abstractclassmethod, abstractmethod
from math import floor, pow


class Event(ABC):
    
    @abstractmethod
    def simulate(cls):
        """
        Simulate event.
        """
        pass
    
    @abstractclassmethod
    def is_possible(cls):
        """
        Determine if event is possible.
        """
        pass
    
    @abstractclassmethod
    def get_event(cls):
        """
        Get the next event.
        """
        pass
    
    def round_down(num, precision):
        
        exp = pow(10, precision)
        return floor(num * exp) / exp