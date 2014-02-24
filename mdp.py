__author__ = 'Austin'


class MDP(object):
    def show(self):
        print self.name
        print "Actions: " + str(self.num_actions)
        print "States: " + str(self.num_states)
        print "Rewards: " + str(self.rewards)
        for i in range(self.num_actions):
            print "Action " + str(i) + " transitions: "
            print str(self.transitions[i])

    def transition(self, start_state, action, end_state):
        return self.transitions[action][start_state][end_state]

    def __init__(self, filename):
        self.name = filename
        self.transitions = []

        with open(filename, "r") as in_file:
            self.num_states = int(in_file.readline().strip())
            self.num_actions = int(in_file.readline().strip())

            # reward: next line of file, split on space, convert to ints
            self.rewards = [float(x) for x in in_file.readline().strip().split()]

            for i in range(self.num_actions):
                # read in transition probability matrix
                matrix = []
                for j in range(self.num_states):
                    matrix.append([float(x) for x in in_file.readline().strip().split()])
                self.transitions.append(matrix)

        assert(self.num_states == len(self.rewards))
        assert(self.num_actions == len(self.transitions))
        for m in self.transitions:
            assert(self.num_states == len(m))
            for t in m:
                assert(self.num_states == len(t))