from fire_ext import FireExtinguisherEnv

from ray.tune.registry import register_env

from ray.rllib.algorithms.dqn.dqn import DQNConfig, DQN
from ray.tune.logger import pretty_print

from ray.rllib.algorithms.algorithm import Algorithm


def env_creator(env_config):
    return FireExtinguisherEnv()  # custom env

register_env("MyFire", env_creator)

config = DQNConfig()
config = config.environment(env="MyFire")
algo = DQN(config=config)

for i in range(100):
    result = algo.train()
    print(f'Done -{i}-')

    
checkpoint_dir = algo.save(r'C:\Users\prabh\Downloads\Reinforcement_Learning\pa5\latest\pol').checkpoint.path
print(f"Checkpoint saved in directory {checkpoint_dir}")