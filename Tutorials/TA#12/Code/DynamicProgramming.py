import numpy as np

def QualityCalc(env, V, s, gamma, a):
    Q = 0
    for succ in range(len(env.P[s][a])):
        p, s_new, R, done = env.P[s][a][succ]
        if done == True: # goal state
            return R
        if p <= 0.0: # invalid action
            return -np.inf 
        else:
            Q += p*(R + gamma*V[s_new]) # update the quality vector for non-terminal states
    return Q

def BellmanUpdate(env, V, s, gamma, policy_extract=False):
    Q = [0]*env.nA # initialize the quality vector
    for a in range(env.nA):
        Q[a] = QualityCalc(env,V,s,gamma,a)
 
    V_new_s = np.max(Q) # Bellman update step

    if policy_extract:
        a_max_s = np.argmax(Q) # Policy extraction
    else:
        a_max_s = None

    return V_new_s, a_max_s

def ValueIteration(env, eps=10**-3, gamma=1, policy_extract=False):
    env.reset()
    V_new = [0]*env.nS # Initialize the value vector to contain only zeroes
    pi_new = [0]*env.nS # Initialize the policy vector to contain only zeroes (for policy extraction)
    
    if gamma == 1 or gamma == 0:
        theta = eps
    else:
        theta = eps*(1-gamma)/gamma

    delta = np.inf # Max. change in the value of any state in an iteration
    while delta >= theta:
        V = np.copy(V_new)
        delta = 0
        pi = np.copy(pi_new)
        for s in range(env.nS): 
            V_new[s], pi_new[s] = BellmanUpdate(env,V,s,gamma,policy_extract=policy_extract)
            if np.linalg.norm(V_new[s] - V[s]) > delta:
                delta = np.linalg.norm(V_new[s] - V[s])

    if policy_extract:
        pi = list(pi)
        pi[5] = 'H'; pi[11] = 'G' 
    else:
        pi = None

    return V, pi

def PolicyEvaluation(env, V, pi, gamma, theta=10**-3):
    delta = np.inf # Max. change in the value of any state in an iteration
    while delta >= theta:
        V_new = [0]*env.nS # re-initialize 
        delta = 0
        for s in range(env.nS):
            for succ in range(len(env.P[s][pi[s]])):
                p, s_new, R, done = env.P[s][pi[s]][succ]
                if done == True: # goal state
                    V_new[s] = R
                    break
                if p <= 0.0: # invalid action
                    break
                else:
                    V_new[s] += p*(R + gamma*V[s_new]) # update the value vector for non-terminal states       
            if np.linalg.norm(V_new[s] - V[s]) > delta:
                delta = np.linalg.norm(V_new[s] - V[s])
        V = np.copy(V_new)
    return V

def PolicyIteration(env, gamma=1):
    env.reset()
    V = [0]*env.nS # Initialize the value vector to contain only zeroes
    pi = np.random.randint(env.nA,size=env.nS) # Randomly initialize the policy vector
    pi = list(pi)

    unchanged = False
    while not unchanged:
        V_new = PolicyEvaluation(env,V,pi,gamma)
        unchanged = True
        for s in range(env.nS):
            V_new_s, a_new_s = BellmanUpdate(env,V_new,s,gamma,policy_extract=True)
            Q_current = QualityCalc(env,V_new,s,gamma,pi[s])
            if V_new_s > Q_current:
                pi[s] = a_new_s
                unchanged = False
        V = np.copy(V_new)

    pi[5] = 'H'; pi[11] = 'G'
    return pi