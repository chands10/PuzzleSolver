import matplotlib.pyplot as plt
import math
import numpy as np
import random
from functools import lru_cache

dp = None

def simulationNonNash(n):
    """
    New strategy is to put a nonzero amount of fuel in each race, so you will only win if there is a race that no one else puts any fuel in.
    Your fuel will be less than 1 in each race. Everyone else will put all of their fuel (1) in one race.
    You will win when there is at least one race of all zeros (not counting yourself).
    """
    trials = 1000
    wins = 0
    
    if n == 1: # must use nash strategy
        return 1 / 3
    
    for i in range(trials):
        races = [0] * n
        for j in range(3 * n - 1):
            pick = random.randrange(len(races))
            races[pick] += 1
        if 0 in races:
            wins += 1
    
    return wins / trials

def simulationNash(n):
    """
    Everyone puts all fuel (1) in one race.
    """
    trials = 1000
    wins = 0
        
    # assume you pick last
    for i in range(trials):
        races = [0] * n
        for j in range(3 * n):
            pick = random.randrange(len(races))
            races[pick] += 1
            
        wins += random.random() <= 1 / races[pick]
    
    return wins / trials

def initializeDP(n):
    """
    Initialize DP board
    dp[i,j] represents the number of ways to fill i races using j unique racers
    (filled meaning each race has at least one racer in it)

    The recurrence is correct because the number of ways to fill i races using j unique racers is
    the sum of the number of ways you can choose k of these racers to fill i - 1 races
    (multiplied by the number of ways you can fill these races)
    and have the rest of the j - k racers to fill the last remaining race.
    We must have that k >= i - 1 since i - 1 races would not be able to be filled otherwise.
    Similarly, we must have that j - k >= 1 to fill the last race.
    We can rearrange this to be k <= j - 1. Thus i - 1 <= k <= j - 1$.
    """
    global dp
    dp = np.zeros((n + 1, 3 * n))
    dp[1,:] = 1
    for i in range(2, n + 1):
        for j in range(i, 3 * n): # start at j = i since we need at least i racers to fill i races
            dp[i,j] = sum(math.comb(j, k) * dp[i - 1, k] for k in range(i - 1, j))

def probFilledForSpecificArrangement(numOtherRacers, p, numRacesFilled):
    """
    Helper function for probExactlyNumRacesFilled.
    p = probability of a racer dedicating all fuel to a certain race
    return prob = the probability of getting to this arrangement * the number of ways to fill numRacesFilled races using numOtherRacers racers
    """
    global dp
    return p**numOtherRacers * dp[numRacesFilled, numOtherRacers]
    
def probExactlyNumRacesFilled(n, numRacesFilled):
    """
    Probability that exactly numRacesFilled races out of n races are filled (race that contains at least one nonzero value)
    """
    numOtherRacers = 3 * n - 1
    p = 1 / n # probability of racer dedicating all fuel to a certain race
    return math.comb(n, numRacesFilled) * probFilledForSpecificArrangement(numOtherRacers, p, numRacesFilled)
       
def probNonNash(n):
    """
    New strategy is to put a nonzero amount of fuel in each race, so you will only win if there is a race that no one else puts any fuel in
    P(Win) = P(at least one race with all 0s) = 1 - P(no race with all 0s)
    = 1 - P(all races with nonzeros) = 1 - P(all races filled) (filled not counting nonnash player)
    """
    if n == 1: # must use nash strategy
        return 1 / 3
    return 1 - probExactlyNumRacesFilled(n, n)

def probNash(n):
    """
    0 <= 3n - i <= 3n - 1 racers dedicate all fuel to n - 1 races (that you are not in) shown by ((n - 1)/n)**(3 * n - i).
    The remaining 1 <= i <= 3n racers (including you) dedicate all fuel to last remaining race (that *you are already assumed to be in*) shown by (1/n)**(i - 1).
    The probability of winning in this case is then 1/i, since i - 1 racers were added to your race, and ties are broken randomly.
    Sum over all values of i in your race. i >= 1 since this is your race.
    """
    return sum(math.comb(3 * n - 1, 3 * n - i) * ((n - 1)/n)**(3 * n - i) * (1/n)**(i - 1) * 1/i for i in range(1, 3 * n + 1))

# ALTERNATIVE UNUSED FUNCTIONS BELOW

@lru_cache(maxsize=None)
def probFilledForSpecificArrangementCache(numOtherRacers, p, numRacesFilled):
    """
    Use recursion + cache
    Helper function for probExactlyNumRacesFilled.
    Place i racers in numRacesFilled - 1 races and the remaining numOtherRacers - i racers in the remaining race
    such that each of the numRacesFilled races are filled (race that contains at least one nonzero value).
    numRacesFilled - 1 <= i <= numOtherRacers - 1 since we need at least one racer in each race.
    Thus numOtherRacers - i >= 1.
    p = probability of a racer dedicating all fuel to a certain race
    """
    if numRacesFilled == 1:
        return p**numOtherRacers

    return sum(math.comb(numOtherRacers, i) * probFilledForSpecificArrangementCache(i, p, numRacesFilled - 1) * p**(numOtherRacers - i) for i in range(numRacesFilled - 1, numOtherRacers))

def probExactlyNumRacesFilledCache(n, numRacesFilled):
    """
    Use recursion + cache
    """
    numOtherRacers = 3 * n - 1
    p = 1 / n # probability of racer dedicating all fuel to a certain race
    return math.comb(n, numRacesFilled) * probFilledForSpecificArrangementCache(numOtherRacers, p, numRacesFilled)

def probNonNashCache(n):
    """
    Use recursion + cache
    """
    if n == 1: # must use nash strategy
        return 1 / 3
    return 1 - probExactlyNumRacesFilledCache(n, n)

def probNonNashOld(n):
    """
    1 - P(all races filled) the but the long way
    """
    if n == 1:
        return 1 / 3
    return sum(probExactlyNumRacesFilledCache(n, i) for i in range(1, n))

def probExactlyNumRacesFilled2(n, numRacesFilled):
    """
    Non-recursive (not counting pos)
    """
    numOtherRacers = 3 * n - 1
    p = 1 / n
    return math.comb(n, numRacesFilled) * math.factorial(numOtherRacers) * p**(numOtherRacers) * sum(1 / math.prod(math.factorial(val) for val in state) for state in pos(numOtherRacers, [0]*numRacesFilled, 0, []))

def probNonNash2(n):
    """
    Non-recursive (much less efficient)
    """
    if n == 1:
        return 1 / 3
    return 1 - probExactlyNumRacesFilled2(n, n)

def probExactlyNumRacesFilledNash(n, numRacesFilled):
    numOtherRacers = 3 * n - 1
    p = 1 / n
    return math.comb(n, numRacesFilled) * math.factorial(numOtherRacers) * p**(numOtherRacers) * sum(1 / math.prod(math.factorial(val) for val in state) * 1 / n * sum(1 / (val + 1) for val in state + (0,) * (n - len(state))) for state in pos(numOtherRacers, [0]*numRacesFilled, 0, []))

def probNash2(n):
    """
    Alternative less efficient way to find nash probability
    """
    return sum(probExactlyNumRacesFilledNash(n, i) for i in range(1, n + 1))

def pos(s, vals, i, r):
    """
    Return list r of possible values of length len(vals) that sum to s,
    such that each value is greater than 0 (order matters)
    """
    if i == len(vals) - 1:
        vals[i] = s
        #print(vals)
        r.append(tuple(vals))
        return r
    
    spotsRemaining = len(vals) - (i + 1)
    maxVal = s - spotsRemaining
    for val in range(1, maxVal + 1):
        vals[i] = val
        pos(s - val, vals, i + 1, r)
    
    return r

if 1 and __name__ == "__main__":
    maxN = 50
    N = range(1, maxN + 1)

    nashSimulation = [simulationNash(n) for n in N]
    nonNashSimulation = [simulationNonNash(n) for n in N]
    plt.plot(N, nashSimulation, label="Nash Simulation")
    plt.plot(N, nonNashSimulation, label="Non-Nash Simulation")
    
    initializeDP(maxN)
    nashProb = [probNash(n) for n in N]
    nonNashProb = [probNonNash(n) for n in N]
    plt.plot(N, nashProb, label="Nash Probability")    
    plt.plot(N, nonNashProb, label="Non-Nash Probability")
    
    plt.legend()
    plt.show()
    
    for i in N:
        if nonNashProb[i - 1] > nashProb[i - 1]:
            print(f"nonNashProb: {nonNashProb[i - 1]}, nashProb: {nashProb[i - 1]}, i={i}")
            break

    """
    print()
    
    b2 = lambda n, p: sum(math.comb(n, i) * p**n for i in range(1, n))
    t2 = lambda n, p: sum(math.comb(n, i) * b2(i, p) * p**(n - i) for i in range(2, n))
    
    print(3 * (1/3)**8 + 3 * b2(8, 1/3))
    print(4 * (1/4)**11 + 6 * b2(11, 1/4) + 4 * t2(11, 1/4))
    """
