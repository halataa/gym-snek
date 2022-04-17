# gym-snek
snake game implemented in gym for RL purposes. suitable for stable-baslines3
## Some Results
- 10x10 grid
- default sb3 PPO MlpPolicy
- around 100M steps
- 4 cunsecutive frames as observation
## Observation Space
numpy array with shape (l, l, 1), and following values for each pixel:
| location   | pixel value |
|------------|-------------|
| apple      | 255         |
| snake body | 127         |
| snake head | 63          |
| background | 0           |
## Action Space
int with 5 values:
| action     | int |
|------------|-------------|
| right      | 0        |
| up | 1         |
| down | 2          |
| left | 3           |
| no action | 4           |
## Reward
you can modify it as you want but this seems to work well:
- +1 for each action that reduces distance between apple and snake head, -1 otherwise
- -10 for death
- 10*Nth_apple for eating apples
