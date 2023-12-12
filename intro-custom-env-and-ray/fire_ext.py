import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np

class FireExtinguisherEnv(gym.Env):
    def __init__(self):
        super(FireExtinguisherEnv, self).__init__()

        self.grid_size = 5
        self.max_steps = 1000

        # Define observation space and action space
        self.observation_space = spaces.Discrete(self.grid_size ** 2)
        self.action_space = spaces.Discrete(4)  # Four discrete actions: 0 (up), 1 (down), 2 (left), 3 (right)

        # Initialize state
        self.agent_pos = None
        self.target_pos = None
        self.fire_cells = set()
        self.extinguished_fire_cells = set()


        self.steps = 0

        self.reset()

    def reset(self, seed=None, options=None):
        # Reset the environment to the initial state

        # Randomly place agent and target
        self.agent_pos = self._get_random_position()
        self.target_pos = self._get_random_position()

        # Initialize fire cells
        self.fire_cells.clear()
        self.extinguished_fire_cells.clear()

        # Reset step counter
        self.steps = 0

        # Return initial observation
        return self._get_observation(), self._get_info()

    def step(self, action):
        # Take a step in the environment based on the action
        # Update the state, calculate reward, done flag, and additional info

        # Define action effects on position
        action_effects = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        # Update agent position
        action_effect = action_effects[action]
        new_agent_pos = (self.agent_pos[0] + action_effect[0], self.agent_pos[1] + action_effect[1])

        # Ensure agent stays within the grid boundaries
        new_agent_pos = self._clip_position(new_agent_pos)

        # Check if the agent visited a cell with fire
        if new_agent_pos in self.fire_cells:
           
            self.fire_cells.discard(new_agent_pos)

        # Update agent position
        self.agent_pos = new_agent_pos

       

        # Randomly move the target
        target_action = np.random.choice([0, 1, 2, 3])
        target_effect = action_effects[target_action]
        new_target_pos = (self.target_pos[0] + target_effect[0], self.target_pos[1] + target_effect[1])
        new_target_pos = self._clip_position(new_target_pos)
        if new_target_pos not in self.extinguished_fire_cells:
            self.target_pos = new_target_pos
        

        if self.target_pos not in self.extinguished_fire_cells:
            # Generate fire in the cell if its not visited by the agent before 
            self.fire_cells.add(self.target_pos)

       

        # Calculate reward 
        #  if agent puts down the fire then reward =100, if it goes to new cell then reward=1, else reward=-1
        if self.agent_pos in self.fire_cells:
            reward = 100
        elif self.agent_pos not in self.extinguished_fire_cells:
            reward = 1
        else:
            reward = -1

         # Add the new agent position to the extinguished fire cells
        self.extinguished_fire_cells.add(self.agent_pos)

        # Check if the goal is reached 
        done = (len(self.fire_cells)==0) or (len(self.extinguished_fire_cells) == self.grid_size**2)
        
        # Additional info (you can provide additional information if needed)
        truncated = (self.steps == self.max_steps)
        
        info = self._get_info()
        observation = self._get_observation()
        # Increment step counter
        self.steps += 1

        # Return the next observation, reward, done flag, and additional info
        return observation, reward, done, truncated, info
   
    def render(self, mode='human'):
        # Visualize the environment using pygame

        if mode == 'human':
            screen_size = 300
            cell_size = screen_size // self.grid_size

            pygame.init()
            screen = pygame.display.set_mode((screen_size, screen_size))

            # Draw the grid
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    pygame.draw.rect(screen, (255, 255, 255), (j * cell_size, i * cell_size, cell_size, cell_size), 1)

            # Draw agent, target, and fire cells
            agent_color = (0, 255, 0)#green
            target_color = (0, 0, 255)#blue
            fire_color = (255, 0, 0)#red

            pygame.draw.rect(screen, agent_color, (self.agent_pos[1] * cell_size, self.agent_pos[0] * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, target_color, (self.target_pos[1] * cell_size, self.target_pos[0] * cell_size, cell_size, cell_size))

            for fire_pos in self.fire_cells:
                pygame.draw.rect(screen, fire_color, (fire_pos[1] * cell_size, fire_pos[0] * cell_size, cell_size, cell_size))

            pygame.display.flip()

            # Event handling (close window with X button)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

    def _get_info(self):
        # return {'fire_cells': list(self.fire_cells),'agent_pos':self.agent_pos,'target_pos':self.target_pos}
        return {}
    
    def _get_observation(self):
        # Encode the current state as an observation
        return self.agent_pos[0] * self.grid_size + self.agent_pos[1]

    def _get_random_position(self):
        # Get a random position within the grid
        return np.random.randint(self.grid_size), np.random.randint(self.grid_size)

    def _clip_position(self, position):
        # Clip the position to ensure it stays within the grid boundaries
        return (
            np.clip(position[0], 0, self.grid_size - 1),
            np.clip(position[1], 0, self.grid_size - 1)
            )

# To try the environment use below code
'''
# Register the environment
gym.register(
    id='FireExtinguisher-v0',
    entry_point='fire_ext:FireExtinguisherEnv',  # Replace with the actual module name
)

# Create and run the environment
if __name__ == "__main__":
    env = gym.make('FireExtinguisher-v0')
    observation = env.reset()
    t=0

    # Run the environment for a few steps
    for _ in range(100000):
        t+=1
        action = env.action_space.sample()
        observation, reward, done,truncated, info = env.step(action)
        env.render()
    env.close()
'''