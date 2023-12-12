from fire_ext import FireExtinguisherEnv
from ray.tune.registry import register_env
from ray.rllib.algorithms.algorithm import Algorithm


def env_creator(env_config):
    return FireExtinguisherEnv()  # custom env

register_env("MyFire", env_creator)

algo = Algorithm.from_checkpoint(r"C:\Users\prabh\Downloads\Reinforcement_Learning\pa5\latest\pol")

env = FireExtinguisherEnv()

obs,_ = env.reset()

G=0
done=False

while not done:
    action = algo.compute_single_action(obs)
    obs,reward, done, truncated, info = env.step(action)
    G+=reward
    env.render()

print(G)
env.close()