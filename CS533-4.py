__author__ = 'Austin'

import random
from mdp import MDP
from sim import Sim
from plan import *


def random_policy(sim):
    rewards = 0
    while not sim.is_trial_over():
        action = random.choice(range(sim.mdp.num_actions))
        rewards += sim.do_action(action)
    return rewards


def safe_policy(sim, p_park):
    rewards = 0
    while not sim.is_trial_over():
        if sim.is_occupied():
            # drive
            rewards += sim.do_action(sim.drive())
        else:
            # randomly decide to park or not
            if random.random() > p_park:
                rewards += sim.do_action(sim.park())
            else:
                rewards += sim.do_action(sim.drive())
    return rewards


def range_policy(sim, near, far):
    """
    Parks if the spot is empty and spot is in [near, far]
    Allows to only go to best spots, or to avoid handicapped
    """
    rewards = 0
    while not sim.is_trial_over():
        if sim.is_occupied():
            # drive
            rewards += sim.do_action(sim.drive())
        else:
            # park if within range
            if near <= sim.get_location() <= far:
                rewards += sim.do_action(sim.park())
            else:
                rewards += sim.do_action(sim.drive())
    return rewards


def run_policy(sim, policy):
    """ Runs policy on sim.
    """
    rewards = 0
    while not sim.is_trial_over() and sim.time < 200:
        rewards += sim.do_action(policy[sim.current])
    return rewards


def adp_rl(mdp, sim, transition_count):
    p_explore = 0.1
    while not sim.is_trial_over():
        old_state = sim.current
        val, policy, iterations = plan(mdp, 0.95, 0.05)
        # take action according to explore/exploit: epsilon-greedy
            # if epsilon
                # random
            # else
                # greedy
        if random.random() < p_explore:
            # choose random action
            action = random.choice(range(sim.get_actions()))
            #print "Random action: " + str(action)
        else:
            # choose policy action
            action = policy[old_state]

        reward = sim.do_action(action)
        new_state = sim.current
        # update model:
            # reward[current] = reward we received on the action
            # transition[action_taken][old_state][new_state] += epsilon
            # somehow remove epsilon from all other transitions like transition[action_taken][old_state][s]
        mdp.rewards[new_state] = reward
        transition_count[action][old_state][new_state] += 1
        mdp = update_transitions(mdp, transition_count)

    return mdp, transition_count


def update_transitions(mdp, transition_count):
    for a in range(mdp.num_actions):
        for s_old in range(mdp.num_states):
            for s_new in range(mdp.num_states):
                mdp.transitions[a][s_old][s_new] = float(transition_count[a][s_old][s_new]) / float(sum(transition_count[a][s_old]))
    return mdp


def average(l):
    return sum(l) / float(len(l))


def generate_blank_mdp(n_actions, n_states):
    rewards = [0 for _ in range(n_states)]
    transitions = [[[1.0 / float(n_states) for _ in range(n_states)] for _ in range(n_states)] for _ in range(n_actions)]

    name = "blank_" + str(n_actions) + "_actions_" + str(n_states) + "_states_mdp"
    with open(name + ".txt", "w") as out_file:
        out_file.write(str(n_states) + "\n")
        out_file.write(str(n_actions) + "\n")
        out_file.write(" ".join([str(x) for x in rewards]))
        out_file.write("\n")
        for a in range(n_actions):
            out_file.write("\n".join([" ".join([str(cell) for cell in line]) for line in transitions[a]]))
            out_file.write("\n")


def part_ii_evaluation():
    random_results_1 = []
    safe_results_1 = []
    range_results_1 = []
    random_results_2 = []
    safe_results_2 = []
    range_results_2 = []

    for i in range(1000):
        print i
        random_results_1.append(random_policy(Sim(MDP("parking_mdp_linear_rewards_n_10.txt"))))
        random_results_2.append(random_policy(Sim(MDP("parking_mdp_quad_rewards_n_10.txt"))))

        safe_results_1.append(safe_policy(Sim(MDP("parking_mdp_linear_rewards_n_10.txt")), 0.5))
        safe_results_2.append(safe_policy(Sim(MDP("parking_mdp_quad_rewards_n_10.txt")), 0.5))

        range_results_1.append(range_policy(Sim(MDP("parking_mdp_linear_rewards_n_10.txt")), 2, 8))
        range_results_2.append(range_policy(Sim(MDP("parking_mdp_quad_rewards_n_10.txt")), 2, 6))

    print average(random_results_1)
    print average(safe_results_1)
    print average(range_results_1)
    print average(random_results_2)
    print average(safe_results_2)
    print average(range_results_2)


def part_iii_evaluations():
    mdp = MDP("blank_2_actions_81_states_mdp.txt")
    results = []
    # prior: assume each transition seen once
    transition_count = [[[0.1 for _ in range(81)] for _ in range(81)] for _ in range(2)]

    for n in range(10):
        print "Big loop " + str(n)
        results.append([])
        for i in range(100):
            print "Training iteration " + str(i)
            mdp, transition_count = adp_rl(mdp, Sim(MDP("parking_mdp_linear_rewards_n_10.txt")), transition_count)
        value_fn, policy, iterations = plan(mdp, 0.99, 0.01)
        print "Value: " + str(value_fn)
        print "Policy: " + str(policy)
        for i in range(100):
            #print "Testing iteration " + str(i)
            reward = run_policy(Sim(MDP("parking_mdp_linear_rewards_n_10.txt")), policy)
            results[n].append(reward)

        print average(results[n])

    for l in results:
        print average(l)


#part_ii_evaluation()
# -31.24, 3.031, 10.885, -36.865, -0.598, 7.027

part_iii_evaluations()