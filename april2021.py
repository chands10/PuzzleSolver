import pprint
from math import inf

# helper function for merge
# fill results array in with probabilities of side1 making it to the next round by considering each team in side1 playing each team in side2 using dynamic programming
# pr[i, j] = pr[i, j - 1] * sum_{k \in possible teams can face in round j} [k / (i + k) * pr[k, j - 1]]
def play(side1, side2, results):
    for team1, p1 in side1.items():
        newProb = 0
        # sum_{k \in possible teams can face in round j} [k / (i + k) * pr[k, j - 1]]
        for team2, p2 in side2.items():
            newProb += team2 / (team1 + team2) * p2
        
        newProb *= p1 # multiply by pr[i, j - 1]
        results[team1] = newProb
        

# helper function for findProbWinning
# sides are lists of teams who would meet in the next round of the bracket
# each team in the list has played each other team in the same list
# return probabilities after these teams play each other
def merge(side1, side2):    
    results = {}    
    play(side1, side2, results) # update probabilities for each team in side1 after playing each team in side2
    play(side2, side1, results) # update probabilities for each team in side2 after playing each team in side1
    
    return results


"""
Requires a bracket that has a length = n which is a power of 2
Return a dictionary that contains the probability of a team (key) winning in its value
Variable elimination (dynamic programming) + divide and conquer algorithm

Subproblem: pr[i, j] = probability that team i wins in round j

Reucrrence:
Base Case: pr[i, 0] = 1
pr[i, j] = pr[i, j - 1] * sum_{k \in possible teams can face in round j} [k / (i + k) * pr[k, j - 1]]

Return pr[team, log_2(n)]

The probability that team i wins in round j is the probability that team i makes it to round j (pr[i, j - 1]) multiplied by the probability that team i wins against their opponent in round j (sum_{k} [...])

The probability that team i wins against their opponent in round j is the sum over k of the probability that team i beats team k (which is k / (i + k)) multiplied by the probability that team k makes it to round j (pr[k, j - 1])

This algorithm will iterate through one round at a time, reducing the need for a 2 dimensional array.

The number of possible teams a team can face in round j is 2^(j - 1) < n. We can use divide and conquer to solve this.

By the Master Theorem we have that we are solving a = 2 subproblems of size n / b = n / 2 and then combining these answers in O(n^d) = O(n^2) time. Thus a = b = d = 2 and 2 > log_2(2) so the running time of this function is O(n^2) 
""" 
def findProbWinning(bracket):
    # probs will be a list of dictionaries. The dictionaries contain a team (key) and its probability of making it to that round (value). Each dictionary in the list contains all of the teams that have already faced each other. Dictionaries here that are adjacent to each other (in pairs of 2s) will face each other in the next round
    probs = [{b: 1} for b in bracket] # base case. List of lists of length 1
    while len(probs) > 1: # log_2(n) iterations.
        newProbs = [0] * (len(probs) // 2)
        for j in range(0, len(probs), 2): # merge like in merge sort
            newProbs[j // 2] = merge(probs[j], probs[j + 1])
        
        probs = newProbs
    
    probs = probs[0] # inner dictionary will be length n
    return probs
            

if __name__ == "__main__":
    # bracket must have length that is a power of 2
    bracket = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
    team = 2 # team to find the best outcome of a swap for
    
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
    print("Swap teams {} and {} to increase team {}'s probability of winning by {:.5f}%".format(bracket[i], bracket[j], team, increase * 100))
    print()
    
    # find optimal solution for team
    bracket[i], bracket[j] = bracket[j], bracket[i] # swap teams
    newProbs = findProbWinning(bracket)

    print("After Swap:")
    print(bracket)
    pp.pprint(newProbs)
    
    bracket[i], bracket[j] = bracket[j], bracket[i] # unswap teams
    