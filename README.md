# Visrl
Visrl (pronounced "visceral") is a simple wrapper to analyse and visualise reinforcement learning agents' behaviour in the environment.

## Install
```python
pip install visrl
```

## Usage
```python
import gym
from stable_baselines3 import DQN
from visrl import Visrl

env = gym.make('LunarLander-v2')
agent = DQN('MlpPolicy', env, verbose=1)
agent.learn(total_timesteps=int(2e5))

Visrl(env, agent).run()
```

## Features
- Key-to-action: Set action hotkeys
- Step: Take actions 1 step at a time
- Continue: Return control to agent
- Speed up/slow down: Control frame rate
- Values: Show all relevant values and plot history
- Breakpoint: Run until condition involving values
- Playback/record: Show past frames and actions
