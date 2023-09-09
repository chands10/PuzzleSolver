We will find a solution by first considering 1D and 2D
# 1D
We can assume that a point is first chosen such that $0 \leq x \leq 1$. This will be one point of the line segment that we draw. For symmetry reasons, we can assume that this is the left endpoint of the line segment (the line segment will be drawn to the right of this point). We want to find the probability that the right endpoint of the line segment with length $d$ will lie between $1 \leq x \leq 2$. Given a left endpoint at $x$ and a length $d$, we can easily find this probability since we know that the right endpoint is at $x + d$.  
Thus $P(x, d) = \begin{cases}1 & 1 \leq x + d \leq 2\\0 & \text{otherwise}\end{cases}$  
Let's assume $d = 0.2$. Then $x \geq 0.8$ for $P(x, d) = 1$. Since $0 \leq x \leq 1$, we have that $P(x, d) = 1$ when $0.8 \leq x \leq 1$.  
If $d = 1.2$, then $0 \leq x \leq 0.8$ for $P(x, d) = 1$.  
Through experimentation, we can see that $P(d) = \begin{cases}d & 0 \leq d \leq 1\\2 - d & 1 \leq d \leq 2\\0 & \text{otherwise}\end{cases}$  
Thus $P(d)$ is maximized at $d = 1$ with $P(1) = 1$.  

For a more analytical approach as we would have to do in higher dimensions, we can rearrange $P(x, d) = \begin{cases}1 & \max(0, 1 - d) \leq x \leq \min(1, 2 - d)\\0 & \text{otherwise}\end{cases}$    
$P(d) = \frac{\int_0^1 P(x, d) dx}{\int_0^1 dx} = \frac{\int_0^1 P(x, d) dx}{1} = \int_0^1 P(x, d) dx = E(d)$  
$P(d) = \int_0^1 P(x, d) dx = \int_{\max(0, 1 - d)}^{\min(1, 2 - d)} dx = \min(1, 2 - d) - \max(0, 1 - d)$  
From this equation we can see that when $0 \leq d \leq 1$ we have that $P(d) = 1 - (1 - d) = d$  
And that when $1 \leq d \leq 2$ we have that $P(d) = (2 - d) - 0 = 2 - d$  
Finally when $d > 2$ $P(d)$ becomes negative which is not valid. In this case we should have $P(d) = 0$. We saw from our bounds $\max(0, 1 - d) \leq x \leq \min(1, 2 - d)$. When $d > 2$ this bound is not valid ($0 \leq x \leq 2 - d$).  
Thus we have the same equations that we found above.
