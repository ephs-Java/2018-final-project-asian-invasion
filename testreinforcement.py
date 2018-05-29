import gym
import keras.optimizers
import numpy as np
from keras import Sequential
from keras.layers import Dense

env = gym.make("Acrobot-v1")
env.reset()

state_size = 1
action_size = 1
learning_rate = 0.2
gamma = 0.1
model = Sequential()
# 'Dense' is the basic form of a neural network layer
# Input Layer of state size(4) and Hidden Layer with 24 nodes
model.add(Dense(24, input_dim=state_size, activation='relu'))
# Hidden layer with 24 nodes
model.add(Dense(24, activation='relu'))
# Output Layer with # of actions: 2 nodes (left, right)
model.add(Dense(action_size, activation='linear'))

model.compile(loss='mse',
              optimizer=keras.optimizers.Adam(lr=learning_rate))

if __name__ == "__main__":
    for _ in range(1000):
        env.render()
        next_state, reward, done, info = env.step(env.action_space.sample())  # take a random action

        target = reward + gamma * np.amax(model.predict(next_state))

        model.fit(next_state, reward, epochs=1, verbose=0)
