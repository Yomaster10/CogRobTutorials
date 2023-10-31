import gym
import numpy as np

def redefine_prob_model(env,prob=0.6):
     desc = ["SFFF", "FHFF", "FFFG"]
     allowable_actions = [[(1,2),(0,1,2),(0,1,2),(0,1)],
                          [(1,2,3),'H',(0,1,2,3),(0,1,3)],
                          [(2,3),(0,2,3),(0,2,3),'G']]
     action_effects = {0:-1,1:4,2:1,3:-4}
     
     for i in range(len(desc)):
          for j in range(len(desc[0])):
               state = 4*i + j
               env.P[state] = {}

               if desc[i][j] == "G":
                    for a in range(4):
                         env.P[state][a] = [(1.0, state, 1, True)]
                    continue
               elif desc[i][j] == "H":
                    for a in range(4):
                         env.P[state][a] = [(1.0, state, -1, True)]
                    continue

               for a in range(4):
                    env.P[state][a] = [(0.0, state, 0, False)]

               acts = allowable_actions[i][j]
               for a in acts:
                    env.P[state][a] = [(prob, state + action_effects[a], 0, False)]
                    if a % 2 == 0:
                         perp = [1,3]
                    else:
                         perp = [0,2]
                    perp_acts = []
                    count = 0
                    for p in perp:
                         if p in acts:
                              count += 1
                              perp_acts.append(p)
                    for c in range(count):
                         act = perp_acts[c]
                         env.P[state][a].append(((1-prob)/count, state + action_effects[act], 0, False))
     return

def show_policy(policy):
    a2w = {'0':'<', '1':'v', '2':'>', '3':'^', 'H': 'H', 'G' : 'G'}
    policy_arrows = [a2w[str(x)] for x in policy]
    print("Policy:\n", np.array(policy_arrows).reshape([-1, 4]))
    return

def get_action(env, s, pi=None, random=True):
    if random:
        allowable_actions = [(1,2),(0,1,2),(0,1,2),(0,1),(1,2,3),'H',(0,1,2,3),(0,1,3),(2,3),(0,2,3),(0,2,3),'G']
        valid_actions = allowable_actions[env.s]
        if valid_actions == 'H' or valid_actions == 'G':
            return 0
        action = np.random.choice(valid_actions)
        return action
    
    if pi[s] == 'G' or pi[s] == 'H':
        action = 0 
    else:
        action = pi[s]
    return action

def evaluate(env, agent='Random', pi=None):
    policies = {'BFS': [1,2,1,1,1,'H',1,1,2,2,2,'G'], 'Optimal' : [2,2,2,1,1,'H',2,1,2,2,2,'G']}
    if agent in policies:
        pi = policies[agent]

    successes = 0; total_reward = 0
    min_steps = 1000; max_steps = 0
    steps_list = []
    for _ in range(1000): # 1000 episodes
        s = env.reset()
        steps = 0
        for _ in range(10000): # Run an episode until terminal state or 10,000 actions done
            steps += 1

            if agent=='Random':
                action = get_action(env, s)
            else:
                action = get_action(env, s, pi=pi, random=False)
            
            s, reward, done, _ = env.step(action)
            if done:
                total_reward += reward
                if reward == 1:
                    if steps < min_steps:
                        min_steps = steps
                    if steps > max_steps:
                        max_steps = steps
                    steps_list.append(steps)
                    successes += 1 # Count the number of episodes in which the goal was successfully reached
                break
            
    print('----------------------------------------------')
    print(f"{agent} agent successfully reached the goal in {successes:.0f} out of 1000 episodes and received an average reward of {total_reward/1000:.03f} using this policy.\n")
    if agent != 'Random':
        show_policy(pi)
        print()
    print(f"{agent} agent took an average of {np.mean(steps_list):.0f} steps to reach the goal.")
    print('----------------------------------------------')
    env.close()
    return

def EnvPrep(p=0.6):
    desc = ["SFFF", "FHFF", "FFFG"]
    env = gym.make('FrozenLake-v1', desc=desc, is_slippery=True)
    redefine_prob_model(env,p)
    env.reset()
    return env