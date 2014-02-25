__author__ = 'Austin'

import random

class Sim(object):
    def __init__(self, mdp):
        self.mdp = mdp
        # current state
        self.current = 0
        # number of parking spots
        self.n = (mdp.num_states - 1) / 8

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
        for i in range(len(outcomes)):
            if sum < p < sum + outcomes[i]:
                next_state = i
                break
            sum += outcomes[i]

        # which of these should be returned?
        self.current = next_state
        return self.mdp.rewards[self.current]


    # the below functions are domain knowledge of the MDP.
    # should probably be in a subclass of Sim, but oh well.
    def drive(self):
        return 0

    def park(self):
        return 1

    def get_location(self):
        """ Parking spot number, from 1 to n
        """
        if self.current < 4 * self.n:
            # A side
            return self.n - self.current / 4
        else:
            # B side
            return (self.current - 4 * (self.n - 1)) / 4


    def is_occupied(self):
        """ Is the spot we're at occupied?
        """
        return (self.current % 4 == 1) or (self.current % 4 == 2)

    def is_trial_over(self):
        """ Have we parked? I.E. is current state the terminal state
        """
        return self.current == self.mdp.num_states - 1