__author__ = 'Austin'

from mdp import MDP
import random

class Sim(object):
    def __init__(self, mdp):
        self.mdp = mdp
        # current state
        self.current = 0

    def get_actions(self):
        return self.mdp.num_actions

    def do_action(self, action):
        # get distribution of result states from current state + action
        outcomes = self.mdp.transitions[action][self.current]
        # random from 0 to 1
        p = random.random()
        sum = 0
        next_state = -1
        # find the next state
        for i in range(outcomes):
            if sum < p < sum + outcomes[i]:
                next_state = i
                break
            sum += outcomes[i]

        # which of these should be returned?
        self.current = next_state
        return self.mdp.rewards[self.current]