import matplotlib.pyplot as plt
import math
import random
from functools import lru_cache

def simulationNonNash(n):
    """
    Win when there is at least one race of all zeros
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

"""
Could increase efficiency by removing multiplication p**numOtherRacers
and p**(numOtherRacers - i), and instead just multiply by p**numOtherRacers
in probExactlyNumRacesFilled, but this makes less sense analytically.
If done this way then can more easily build up solution using
dynamic programming instead of cache
"""
@lru_cache(maxsize=None)
def probFilledForSpecificArrangement(numOtherRacers, p, numRacesFilled):
    """
    Helper function for probExactlyNumRacesFilled.
    Place i racers in numRacesFilled - 1 races and remaining numOtherRacers - i racers in last remaining race
    such that each of the numRacesFilled races are filled (race that contains at least one nonzero value).
    numRacesFilled - 1 <= i <= numOtherRacers - 1 since need at least one racer in each race.
    Thus numOtherRacers - i >= 1.
    p = probability of racer dedicating all energy to a certain race
    """
    if numRacesFilled == 1:
        return p**numOtherRacers

    return sum(math.comb(numOtherRacers, i) * probFilledForSpecificArrangement(i, p, numRacesFilled - 1) * p**(numOtherRacers - i) for i in range(numRacesFilled - 1, numOtherRacers))
    
def probExactlyNumRacesFilled(n, numRacesFilled):
    """
    Probability that exactly numRacesFilled races out of n races are filled (race that contains at least one nonzero value)
    """
    numOtherRacers = 3 * n - 1
    p = 1 / n # probability of racer dedicating all energy to a certain race
    return math.comb(n, numRacesFilled) * probFilledForSpecificArrangement(numOtherRacers, p, numRacesFilled)
       
def probNonNash(n):
    """
    P(Win) = P(at least one race with all 0s) = 1 - P(no race with all 0s)
    = 1 - P(all races with nonzeros) = 1 - P(all races filled) (filled not counting nonnash player)
    """
    if n == 1: # must use nash strategy
        return 1 / 3
    return 1 - probExactlyNumRacesFilled(n, n)

def probNash(n):
    """
    0 <= 3n - i <= 3n - 1 racers dedicate all energy to n - 1 races (that you are not in) ((n - 1)/n)**(3 * n - i).
    Remaining 1 <= i <= 3n racers dedicate all energy to last remaining race (that *you are assumed to be in*, calculate probability of winning from this case) (1/n)**(i - 1).
    Ties broken randomly, so you have 1 / i chance of winning in this case.
    Sum over all combinations.
    """
    return sum(math.comb(3 * n - 1, 3 * n - i) * ((n - 1)/n)**(3 * n - i) * (1/n)**(i - 1) * 1/i for i in range(1, 3 * n + 1))

# ALTERNATIVE UNUSED FUNCTIONS BELOW

def probNonNashOld(n):
    """
    1 - P(all races filled) the but the long way
    """
    if n == 1:
        return 1 / 3
    return sum(probExactlyNumRacesFilled(n, i) for i in range(1, n))

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
    N = range(1, 51)
    nashSimulation = [simulationNash(n) for n in N]
    nonNashSimulation = [simulationNonNash(n) for n in N]
    plt.plot(N, nashSimulation)
    plt.plot(N, nonNashSimulation)
    
    # Nash equilibrium
    nashProb = [probNash(n) for n in N]
    
    plt.plot(N, nashProb)
    
    # Nonnash equilibrium
    nonNashProb = [probNonNash(n) for n in N]
    plt.plot(N, nonNashProb)
    
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