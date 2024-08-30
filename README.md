# SLIME-SIMULATIONS-USING-PYTHON
 This code simulates the slime using various factors like pheromones, obstacles and interactions between other colored slimes

# Slime Simulation

## Overview
This project simulates a group of "slimes" moving around a 2D environment, depositing and sensing pheromones, and interacting with obstacles and food sources. The simulation is rendered using the Pygame library and allows for drawing obstacles with the mouse, which the slimes will avoid. The simulation also records the output as a video.

## Features
- **Slime Movement**: Slimes move around the environment, depositing pheromones and responding to the concentration of pheromones around them.
- **Obstacle Interaction**: Users can draw rectangular obstacles that slimes will avoid.
- **Food Attraction**: Slimes are attracted to food sources placed randomly on the screen.
- **Pheromone Dynamics**: Slimes deposit pheromones as they move, which evaporate over time.
- **Multi-threaded Simulation**: Slime updates are processed in parallel using threads for better performance.
- **Video Recording**: The simulation's output is saved as a video file with a blur effect and increased resolution.

## Requirements
- Python 3.x
- Pygame
- NumPy
- OpenCV

## Installation
1. **Install Python 3.x**: Make sure Python is installed on your system.
2. **Install Required Libraries**: You can install the necessary libraries using pip:

   ```bash
   pip install pygame numpy opencv-python

## Running the Simulation

### Run the Python Script
Execute the script using Python:

```python slime_simulation.py```

## Customization
You can adjust various parameters at the beginning of the script to change the behavior of the slimes:

- **NUM_SLIME**: Number of slimes in the simulation.
- **SPEED**: Movement speed of the slimes.
- **SENSOR_DISTANCE**: Distance at which slimes can sense pheromones and food.
- **ROTATION_ANGLE**: Angle by which slimes turn when adjusting their direction.
- **DEPOSIT_AMOUNT**: Amount of pheromone deposited by each slime.
- **EVAPORATION_RATE**: Rate at which pheromones evaporate over time.
- **FOOD_ATTRACTION**: Attraction strength of food sources.
- **AVOIDANCE_RADIUS**: Distance at which slimes avoid obstacles and other slimes.
