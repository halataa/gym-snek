import random
import numpy as np
import gym
from gym import spaces
import matplotlib.pyplot as plt


class Snek(gym.Env):

    def __init__(self, l:int=10):
        super(Snek, self).__init__()
        self.l = l
        self.infos = {}
        self.reward = 0
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(low=0, high=255, shape=(l,l,1), dtype=np.uint8)
    
    @staticmethod
    def dist(h,a):
        return np.sum(abs(np.subtract(h,a)))
        
    def get_new_apple(self):
        idxs = list(np.ndindex(*self.grid.shape))
        idxs = [idx for idx in idxs if idx not in self.snake_position]
        return random.choice(idxs)
    
    def step(self, action):
        head = list(self.snake_position[0])
        took_action = False
        while not took_action:
            if action == 0:
                head[1] += 1 # right
                took_action = True
            elif action == 1:
                head[0] -= 1 # up
                took_action = True
            elif action == 2:
                head[0] += 1 # down
                took_action = True
            elif action == 3:
                head[1] -= 1 # left
                took_action = True
            elif action == 4:
                action = self.prev_action # no action

        self.prev_action = action
            
        #move and check for apple
        apple_reward = 0
        die_reward = 0
        head = tuple(head)
        self.snake_position.insert(0, head)
        if head == self.apple_position:
            self.apple_position = self.get_new_apple()
            self.prev_dist = np.inf # reset distance
            self.apples_eat += 1
            apple_reward = 10*self.apples_eat
        else:
            self.snake_position.pop()
        
        if head in self.snake_position[1:]:
            die_reward = -10
            self.done = True
            self.infos['death'] = 'self bite'
        # collision with wall
        if any(x==self.l for x in head) or any(x==-1 for x in head):
            die_reward = -10
            self.done = True
            self.snake_position = self.snake_position[1:]
            self.infos['death'] = 'collision with wall'

        self.grid = np.zeros((self.l, self.l),dtype='uint8')
        self.grid[tuple(zip(*self.snake_position))] = 127 # np.array[((y1,y2,...),(x1,x2,...))]
        self.grid[self.snake_position[0]] = 63
        self.grid[tuple(self.apple_position)] = 255
        obs = np.expand_dims(self.grid,axis=-1)
        dist = self.dist(head,self.apple_position)
        if dist < self.prev_dist:
            dreward = 1
        else:
            dreward = -1
        self.prev_dist = dist
        reward = dreward + apple_reward + die_reward
        self.infos['apples_eat'] = self.apples_eat
        
        return obs, reward, self.done, self.infos
        
            
    def reset(self):
        self.done = False
        self.apples_eat = 0
        x = y = self.l // 2
        # Initial Snake and Apple position
        self.grid = np.zeros((self.l, self.l),dtype='uint8')
        self.snake_position = [(y,x),(y,x-1),(y,x-2)]
        self.apple_position = self.get_new_apple()
        self.grid[tuple(zip(*self.snake_position))] = 127 # np.array[((y1,y2,...),(x1,x2,...))]
        self.grid[self.snake_position[0]] = 63
        self.grid[self.apple_position] = 255
        self.reward = 0
        self.prev_action = 0
        self.prev_dist = self.l*2
        obs = np.expand_dims(self.grid,axis=-1)
        return obs  # reward, done, info can't be included
    
    def render(self,mode='rgb_array'):
        if mode == 'rgb_array':
            return self.grid
        elif mode == 'human':
            plt.cla()
            plt.imshow(self.grid)
            plt.draw()
            plt.pause(0.1)

    def play(self):
        """code for manual play"""
        ...

if __name__ == "__main__":
    env = Snek(40)
    env.reset()
    print(env.prev_action)
    done = False
    while not done:
        a = 4
        obs,reward,done,info = env.step(a)
        env.render(mode='human')