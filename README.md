physics_simulation
==============================

Customizable simulation of particles in space.

Overview
------------

Running Simulation.py begins the simulation. Any keyword argument passed to the Simulation constructor will be passed to every constructor throughout the program. The simulation begins by initializing the Space object and a list of Particle objects. Each frame is iteratively simulated and stored to a specified filename. For each frame, the Space object gets the soonest event to occur, simulates it, and repeats until the end of the frame. Rather than check if an event occured between any combination of particles, only the combinations where events are possible are considered.


Project Organization
------------

    ├── LICENSE
    ├── README.md                   <- The top-level README for developers using this project.
    ├── src
    │   ├── Event.py                <- Abstract class representing a generic event within the simulation.
    │   ├── BoundaryCollision.py    <- Event representing a collision between a particle and its space boundary.
    │   ├── ParticleCollision.py    <- Event representing a collision between two particles.
    │   ├── EventManager.py         <- Class to detect and handle events within the simulation.
    │   ├── Particle.py             <- Class representing a particle within space.
    │   ├── Space.py                <- Class representing the space in which to simulate particles.
    │   └── Simulation.py           <- Class representing the simulation as a whole.
    │
    ├── example1.avi                <- Example of 30 particles in a 100x100 space with default arguments. Render time: 43.56 seconds