import pprint
from math import inf

# fill results array in with probabilities of side1 making it to the next round by considering each team in side1 playing each team in side2 using dynamic programming
# pr[i, j] = pr[i, j - 1] * sum_{k \in possible teams can face in round j} [k / (i + k) * pr[k, j - 1]]
def play(side1, side2, results):
    for team1, p1 in side1:
        newProb = 0
        for team2, p2 in side2:
            newProb += team2 / (team1 + team2) * p2
        
        newProb *= p1
        results.append((team1, newProb))

# helper function for findProbWinning
# teams in probs[idx] will be playing teams in probs[idx + 1]
# return probabilities after these teams play each other
def merge(probs, idx):
    side1 = probs[idx] # teams on one side of bracket that have already played each other
    side2 = probs[idx + 1] # teams on other side of bracket that have already played each other
    
    results = []    
    play(side1, side2, results) # update probabilities for each team in side1 after playing each team in side2
    play(side2, side1, results) # update probabilities for each team in side2 after playing each team in side1
    
    return results

"""
Dynamic programming algorithm

Subproblem: pr[i, j] = probability that team i wins in round j

Reucrrence:
Base Case: pr[i, 0] = 1
pr[i, j] = pr[i, j - 1] * sum_{k \in possible teams can face in round j} [k / (i + k) * pr[k, j - 1]]

The probability that team i wins in round j is the probability that team i makes it to round j (pr[i, j - 1]) multiplied by the probability that team i wins against their opponent in round j (sum_{k} [...])

The probability that team i wins against their opponent in round j is the sum over k of the probability that team i beats team k (which is k / (i + k)) multiplied by the probability that team k makes it to round j (pr[k, j - 1])

This algorithm will iterate through one round at a time, reducing the need for a 2 dimensional array.

Requires a bracket that is a power of 2 in length
""" 
def findProbWinning(bracket):
    # probs will be a list of lists of tuples. The tuples represents a team and its probability of making it to that round. The most inner list contains all of the teams that have already faced each other. Lists here that are adjacent to each other (in pairs of 2s) will face each other in the next round
    probs = [[(b, 1)] for b in bracket] # base case. List of lists of length 1
    while len(probs) > 1: # log_2(n) iterations.
        newProbs = [0] * (len(probs) // 2)
        for j in range(0, len(probs), 2): # merge like in merge sort
            newProbs[j // 2] = merge(probs, j)
        
        probs = newProbs
    
    probs = probs[0] # inner list will be length n
    probs = {pair[0]: pair[1] for pair in probs} # convert to dictionary
    return probs
            

if __name__ == "__main__":
    bracket = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
    team = 2
    
    pp = pprint.PrettyPrinter()
    
    probs = findProbWinning(bracket)
    
    print("Before Swap:")
    print(bracket)
    pp.pprint(probs)
    
    initialProb = probs[team]
    best = (-inf, None) # best increase, team to swap
    
    # consider all pairs where swapping two teams makes a difference in the bracket
    for i in range(len(bracket)):
        for j in range(i + 1, len(bracket)):
            if i % 2 == 0 and j == i + 1: # makes no difference in bracket
                continue
            
            bracket[i], bracket[j] = bracket[j], bracket[i] # swap teams
            newProbs = findProbWinning(bracket)
            bracket[i], bracket[j] = bracket[j], bracket[i] # unswap teams

            current = (newProbs[team] - initialProb, (i, j))
            best = max(best, current)
    
    increase, (i, j) = best
    
    print()
    print("Swap teams {} and {} to increase team {}'s probability of winning by {:.4f}".format(bracket[i], bracket[j], team, increase))
    print()
    
    # find optimal solution for team
    bracket[i], bracket[j] = bracket[j], bracket[i] # swap teams
    newProbs = findProbWinning(bracket)

    print("After Swap:")
    print(bracket)
    pp.pprint(newProbs)
    
    bracket[i], bracket[j] = bracket[j], bracket[i] # unswap teams
    