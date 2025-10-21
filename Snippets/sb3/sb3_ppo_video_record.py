import gymnasium as gym
import time
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy

print("[Imports loaded]")

device = "cpu"
gym_id = "CartPole-v1"
seed = 4
run_name = f"{gym_id}__{seed}__{int(time.time())}"

def make_env(gym_id, seed, idx, capture_video, run_name, render_mode="rgb_array"):
    env = gym.make(gym_id, max_episode_steps=10000, render_mode=render_mode)
    env = gym.wrappers.RecordEpisodeStatistics(env)
    if capture_video:
        env = gym.wrappers.RecordVideo(env, f"videos/{run_name}", episode_trigger=lambda x: x % 1 == 0)
    return env

env = make_env(gym_id, 4, 0, False, run_name)  # Change capture_video to False for training
# env reset for a fresh start
observation, info = env.reset()

print("[Start]")

t1 = time.time()

model = PPO("MlpPolicy", env, device=device, verbose=1, seed=seed)
model.learn(total_timesteps=60_000)
print(f"\n[Time with cpu]: {time.time()-t1:.2f}s\n")

# Evaluate the model and capture video
env_eval = make_env(gym_id, 4, 0, True, run_name)  # Change capture_video to True for evaluation
mean_reward, std_reward = evaluate_policy(model, env_eval, n_eval_episodes=10)

env.close()
env_eval.close()

print(f"\n[Mean reward]: {mean_reward:.2f} {std_reward:.2f}\n")
