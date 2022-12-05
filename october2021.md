Nash Strategy:
$$P(N) = \sum_{i = 1}^{3N} \left(\binom{3N - 1}{3N - i} \left(\frac{N - 1}{N} \right)^{3N - i} \left(\frac{1}{N} \right)^{i - 1} \left(\frac{1}{i} \right) \right)$$
$0 \leq 3N - i \leq 3N - 1$ racers dedicate all fuel to $N - 1$ races (that you are not in) shown by $\left(\frac{N - 1}{N} \right)^{3N - i}$.  
The remaining $1 \leq i \leq 3N$ racers (including you) dedicate all fuel to last remaining race (that *you are already assumed to be in*) shown by $\left(\frac{1}{N} \right)^{i - 1}$.  
The probability of winning in this case is then $\frac{1}{i}$, since $i - 1$ racers were added to your race, and ties are broken randomly.  
Sum over all values of $i$ in your race. $i \geq 1$ since this is your race.

Non-Nash Strategy:
$$probFilledForSpecificArrangement(numOtherRacers, p, numRacesFilled = 1) = p^{numOtherRacers}$$
$$probFilledForSpecificArrangement(numOtherRacers, p, numRacesFilled > 1) = \sum_{i = numRacesFilled - 1}^{numOtherRacers - 1} \binom{numOtherRacers}{i} \cdot probFilledForSpecificArrangement(i, p, numRacesFilled - 1) \cdot p^{numOtherRacers - i}$$
$$probExactlyNumRacesFilled(N, numRacesFilled) = \binom{N}{numRacesFilled} \cdot probFilledForSpecificArrangement(3N - 1, \frac{1}{N}, numRacesFilled)$$
$$P(N) = 1 - probExactlyNumRacesFilled(N, N)$$  
The new strategy is to put a nonzero amount of fuel in each race, so you will only win if there is a race that no one else puts any fuel in.  
Your fuel will be less than 1 in each race. Everyone else will put all of their fuel (1) in one race.  
You will win when there is at least one race of all zeros (not counting yourself).  
So $P(\text{Win}) = P(\text{at least one race with all 0s})$  
$ = 1 - P(\text{no race with all 0s})$  
$ = 1 - P(\text{all races with nonzeros})$  
$ = 1 - P(\text{all races filled})$  
where a race is *filled* if at least one racer (not counting yourself) dedicates all energy to this race.  

$probExactlyNumRacesFilled(N, numRacesFilled)$ is the probability that exactly $numRacesFilled$ races out of $N$ races are filled.  

$probFilledForSpecificArrangement(numOtherRacers, p, numRacesFilled)$ is a helper function for $probExactlyNumRacesFilled$.  
Place $i$ racers in $numRacesFilled - 1$ races and the remaining $numOtherRacers - i$ racers in the last remaining race such that each of the $numRacesFilled$ races are filled.  
$numRacesFilled - 1 \leq i \leq numOtherRacers - 1$ since we need at least one racer in each race.  
Thus $numOtherRacers - i \geq 1$.  
$p$ is the probability of a racer dedicating all fuel to a certain race.  

We could increase the efficiency of this function by removing the multiplication $p^{numOtherRacers}$ and $p^{numOtherRacers - i}$, and instead just multiply once by $p^{numOtherRacers}$ in $probExactlyNumRacesFilled$, but this makes less sense analytically.  
If done this way then we can more easily build up a solution using dynamic programming instead of a cache.  
We can rewrite $probExactlyNumRacesFilled$ to be non-recursive based on the equations above, but this function is much slower to run this way compared to the recursive way (due to caching).  
Let $S$ be the set of all ordered sets whose $numRacesFilled$ integer elements are all greater than or equal to 1 and sum to $3N - 1$ (given that order matters).  
$$S = \{S_i : S_i = \{s_{ij} : 1 \leq j \leq numRacesFilled, s_{ij} \geq 1, \sum_{s \in S_i} s = 3N - 1\}\}$$
$S$ is equivalent to all of the ways that all of the other $3N - 1$ racers could fill $numRacesFilled$ races (this part does use recursion to find).
$$probExactlyNumRacesFilled(N, numRacesFilled) = \binom{N}{numRacesFilled} \sum_{S_i \in S} \left(\frac{numRacesFilled!}{\prod_{s \in S_i} s!} \cdot \left(\frac{1}{N} \right)^{3N - 1} \right)$$
$$ = \binom{N}{numRacesFilled} \cdot numRacesFilled! \cdot \left(\frac{1}{N} \right)^{3N - 1} \sum_{S_i \in S} \frac{1}{\prod_{s \in S_i} s!}$$
Note in the first equations we have $p = \frac{1}{N}$ and $numOtherRacers = 3N - 1$.  
The first equation can reduce to this equation, since the first equation is multiplying many combinations together, and simplifying these multiplications just results to this equation.
