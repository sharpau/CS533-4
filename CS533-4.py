__author__ = 'Austin'

import random
from mdp import MDP
from sim import Sim


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


def ADP_RL(mdp, sim):
    while not sim.is_trial_over():
        # plan(mdp, discount, epsilon)
        # take action according to explore/exploit: epsilon-greedy
            # if epsilon
                # random
            # else
                # greedy
        # update model:
            # reward[current] = reward we received on the action
            # transition[action_taken][old_state][new_state] += epsilon
            # somehow remove epsilon from all other transitions like transition[action_taken][old_state][s]


def average(l):
    return sum(l) / float(len(l))


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
    # mdp = create_blank_mdp()
    results = []

    for n in range(10):
        results.append([])
        for i in range(1000):
            #mdp = ADP_RL(mdp, Sim(MDP("parking_mdp_linear_rewards_n_10.txt")))
        # policy = plan(mdp, reward_fn, discount, epsilon)
        for i in range(1000):
            # reward = run_policy(policy, Sim(MDP("parking_mdp_linear_rewards_n_10.txt")))
            # results[n].append(reward)

    for l in results:
        print average(l)


#part_ii_evaluation()
# -31.24, 3.031, 10.885, -36.865, -0.598, 7.027


