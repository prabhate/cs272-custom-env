# Wildfire and Drone in Forest Environment

## Project Summary
<!-- Around 200 Words -->
<!-- Cover (1) What problem you are solving, (2) Who will use this RL module and be happy with the learning, and (3) a brief description of the results -->

Wildfires pose a significant threat to forests, wildlife, and the environment. This project addresses the challenge of wildfire containment using Reinforcement Learning (RL). The environment consists of a 10x10 grid representing a forest. Two entities, the Wildfire and the Drone, are initialized in random cells. The Wildfire spreads randomly, igniting cells, while the Drone, guided by a policy, extinguishes fires and accumulates rewards for each step taken. If the Drone passes through a cell, it prevents the Wildfire from entering, acting as a strategic barrier. The objective is to eliminate all fires in the forest.

## State Space
<!-- Define the observation space -->

The state space is represented by the 10x10 grid, where each cell can be empty, contain fire, or be occupied by the entities.

<!--| Num | Observation                       | Min | Max |-->
<!--|-----|-----------------------------------|-----|-----|-->
<!--| 0   | Forest Grid (0: Empty, 1: Fire, 2: Drone, 3: Fire + Drone) | 0   | 3   |-->

## Action Space
<!-- Define the action space -->

Both entities have the same action space, allowing movement in any direction (up, down, left, right) within the grid.

| Num | Action                                  
|-----|-----------------------------------------
| 0   | Move Up                                 
| 1   | Move Down                               
| 2   | Move Left                               
| 3   | Move Right                              

## Rewards
<!-- Define the updated reward structure -->

The Drone receives rewards as follows:
- -1 for revisiting a cell.
- 1 for visiting a new cell.
- 100 for extinguishing a fire cell.

The Wildfire does not receive explicit rewards; its objective is to ignite cells. The cumulative reward for the Drone is used as a performance metric.

## RL Algorithm 
<!-- Specify the RL algorithm to be used -->

We employ DQN (Deep Q-Network), a model-free RL algorithm that utilizes a neural network to approximate the Q-values. DQN is suitable for discrete action spaces and facilitates learning optimal policy for Drone agent to efficiently control and contain wildfires.


## Starting State
<!-- Specify the starting state conditions -->

The Wildfire and Drone are initially placed in random cells within the 10x10 grid.

## Episode End
<!-- Specify the conditions for episode termination -->

An episode ends when all fires are extinguished, and the forest is declared safe.

## Results
![alt text](https://github.com/prabhate/cs272-custom-env/blob/main/intro-custom-env-and-ray/metrics.png)
