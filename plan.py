__author__ = 'Austin'

import operator


def bellman_backup(mdp, value_k, discount):
    """
    Given an MDP and its value function with time-to-go k, returns its value function with time-to-go k+1.
    """
    # computing a new value function, ie list over all states
    new_value_fn = []
    actions = []
    for s in range(mdp.num_states):
        # R(s) + max_a[sum_s'(T(s,a,s') dot Vk(s'))]
        action_results = []
        for a in range(mdp.num_actions):
            action_results.append(sum([mdp.transition(s, a, s_next) * value_k[s_next] for s_next in range(mdp.num_states)]))

        max_index, max_value = max(enumerate(action_results), key=operator.itemgetter(1))
        actions.append(max_index)
        new_value_fn.append(mdp.rewards[s] + discount * max_value)

    return new_value_fn, actions


def max_norm(new, old):
    return max([new[i] - old[i] for i in range(0, len(new))])


def plan(mdp, discount, epsilon):
    """
    Main algorithm. The input to your algorithm should be a description of an MDP and
    a time horizon H (positive integer). The output should be an optimal non-stationary value
    function and non-stationary policy for the MDP and time horizon .
    """
    bellman_error = []
    bellman_error.append(max(mdp.rewards))
    policy = []
    iterations = 0
    # initialize at iteration 0 with reward of each state
    value_function = mdp.rewards

    # run once so as to not return empty stuff
    new_values, policy = bellman_backup(mdp, value_function, discount)
    bellman_error.append(max_norm(new_values, value_function))
    value_function = new_values
    iterations += 1

    while bellman_error[len(bellman_error) - 1] > epsilon:
        new_values, policy = bellman_backup(mdp, value_function, discount)
        bellman_error.append(max_norm(new_values, value_function))
        value_function = new_values
        iterations += 1
    # at this point we have the k-th value and policy
    return value_function, policy, iterations