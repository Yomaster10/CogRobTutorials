import time
import numpy as np
import matplotlib.pyplot as plt

def ConvergenceCheck(env, pi, method='MC', gamma=1, eps=10**-1, alpha=0.5):
    V = [0]*env.nS
    converged = False; num_episodes = 2

    start_time = time.time()
    while not converged:
        if method=='MC':
            V_new = MC_Estimation(env, pi, num_episodes=num_episodes)
        elif method=='TD0':
            V_new = TD0(env, pi, alpha=alpha, gamma=gamma, num_episodes=num_episodes)
        elif method=='ADP':
             T,R = ADP(env, pi, num_episodes=num_episodes)
             V_new = ADP_PolicyEval(T, R, pi, gamma=gamma)
        
        if np.linalg.norm(np.subtract(V_new, V), ord=2) < eps:
            converged = True
            break
        V = np.copy(V_new)
        num_episodes += 1
    tot_time = time.time() - start_time
        
    print(f"{method}-Estimation converged after {num_episodes} episodes, which took {tot_time:.2f} seconds.\n")
    print(f"{method}-Estimated Value Vector:\n", np.reshape(V_new,(3,4)),"\n")

    return V_new, num_episodes

def MC_Estimation(env, pi, num_episodes=100, every_time=True):
    N = [0]*env.nS
    Returns = [0]*env.nS
    for _ in range(num_episodes):
        env.reset() # start a new episode
        results = []; done = False
        while not done:
            state = env.s
            if state==5 or state==11: # terminal states
                action = 0
            else:
                action = pi[state] # choose action according to policy
            _, reward, done, _ = env.step(action)
            results.append((state,reward))
 
        G = 0
        visited = [False]*env.nS # Used in First-Time MC
        for t in range(len(results)-1,-1,-1):
            G += results[t][1]

            if every_time: # Every-Time MC
                Returns[results[t][0]] = Returns[results[t][0]] + G
                N[results[t][0]] += 1
            else: # First-Time MC
                if not visited[results[t][0]]:
                    Returns[results[t][0]] = Returns[results[t][0]] + G
                    N[results[t][0]] += 1
                    visited[results[t][0]] = True
    
    V_mc = [Returns[s]/N[s] if N[s]>0 else 0 for s in range(env.nS)]
    return V_mc

def TD0(env, pi, alpha=0.5, gamma=1, num_episodes=100, adaptive=False):
    V_TD = [0]*env.nS # initialize the value vector arbitrarily, ensuring that V=0 for all terminal states

    N = [0]*env.nS
    for e in range(num_episodes):
        env.reset() # start a new episode
        
        done = False
        while not done:
            s = env.s
            if s==5 or s==11: # terminal states
                action = 0
            else:
                action = pi[s] # choose action according to policy
            new_s, R, done, _ = env.step(action)

            if adaptive==True:
                N[s] += 1
                alpha = 1/N[s]
                #print(alpha)

            if done:
                V_TD[s] += alpha*(R - V_TD[s])
            else:
                V_TD[s] += alpha*(R + gamma*V_TD[new_s] - V_TD[s])

    return V_TD

def ADP(env, pi, num_episodes=100):
    N = [0]*env.nS # number of visits to a state
    R = [0]*env.nS # estimated reward model
    T = {s:{} for s in range(env.nS)} # estimated transition model

    for _ in range(num_episodes):
        env.reset() # start a new episode
        done = False
        while not done:
            s = env.s
            a = pi[s] # choose action according to policy
            
            if a not in T[s]:
                T[s][a] = {}

            if s==5 or s==11: # terminal states
                action = 0
            else:
                action = a # choose action according to policy
            
            new_s, reward, done, _ = env.step(action)
           
            N[s] += 1
            R[s] += reward
            
            if new_s not in T[s][a]:
                T[s][a][new_s] = 0

            T[s][a][new_s] += 1

    R = [R[s]/N[s] if N[s]>0 else 0 for s in range(len(R))]
    T = {s:{a:{new_s:T[s][a][new_s]/N[s] if N[s]>0 else 0 for new_s in T[s][a]} for a in T[s]} for s in T}
    return T, R

def ADP_PolicyEval(T, R, pi, gamma=1, theta=10**-3):
    delta = np.inf # Max. change in the value of any state in an iteration
    V = [0]*len(R) # Initialize the value vector to contain only zeroes

    while delta >= theta:
        V_new = [0]*len(R) # Re-initialize 
        delta = 0
        for s in range(len(R)):
            reward = R[s] 
            if s==5 or s==11:
                V_new[s] = reward
            else:
                if pi[s] in T[s]:
                    for new_s in T[s][pi[s]]:
                        p = T[s][pi[s]][new_s]
                        V_new[s] += p*(reward + gamma*V[new_s]) # update the value vector for non-terminal states  
                     
            if np.linalg.norm(V_new[s] - V[s]) > delta:
                delta = np.linalg.norm(V_new[s] - V[s])
        V = np.copy(V_new)

    return V

def Plot_MSEvEpisodes(env, pi, V_opt, method='MC', gamma=1, alpha=0.5):
    episodes = np.linspace(10,1000,10,dtype=int)
    error = np.zeros_like(episodes,dtype=float)

    for i, e in enumerate(episodes):
        res = []
        for _ in range(100):
            if method=='MC':
                V_new = MC_Estimation(env, pi, num_episodes=e)
            elif method=='TD0':
                V_new = TD0(env, pi, alpha=alpha, gamma=gamma, num_episodes=e)
            elif method=='ADP':
                T,R = ADP(env, pi, num_episodes=e)
                V_new = ADP_PolicyEval(T, R, pi, gamma=gamma)
            res.append(np.linalg.norm(np.subtract(V_new,V_opt),ord=2) / len(episodes))
        error[i] = np.mean(res)
    
    plt.rcParams["figure.figsize"] = plt.rcParamsDefault["figure.figsize"]
    plt.plot(episodes,error)
    plt.xlabel('Episodes')
    plt.ylabel('MSE')
    plt.title(f'MSE of {method}-Estimated Value Vector as a Function of the Number of Episodes');
    return error