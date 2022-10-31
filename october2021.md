Nash Strategy:
$$P(N) = \sum_{i = 1}^{3N} \left( \binom{3N - 1}{3N - i} \left(\frac{N - 1}{N} \right)^{3N - i} \left(\frac{1}{N} \right)^{i - 1} \left(\frac{1}{i} \right) \right)$$
Non-Nash Strategy:
$$probFilledForSpecificArrangement(numOtherRacers, p, numRacesFilled = 1) = p^{numOtherRacers}$$
$$probFilledForSpecificArrangement(numOtherRacers, p, numRacesFilled > 1) = \sum_{i = numRacesFilled - 1}^{numOtherRacers - 1} \binom{numOtherRacers}{i} \cdot probFilledForSpecificArrangement(i, p, numRacesFilled - 1) \cdot p^{numOtherRacers - i}$$
$$probExactlyNumRacesFilled(N, numRacesFilled) = \binom{N}{numRacesFilled} \cdot probFilledForSpecificArrangement(3N - 1, 1 / N, numRacesFilled)$$
$$P(N) = 1 - probExactlyNumRacesFilled(N, N)$$
