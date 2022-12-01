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
