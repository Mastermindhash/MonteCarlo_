# Monte-Carlo Estimator 

This project implements composed uncertainty computation using the Monte-Carlo method, in accordance with the GUM (Guide to the Expression of Uncertainty in Measurement) framework studied as part of the CPGE (MPSI) curriculum.

The Monte-Carlo method is particularly valuable because it allows the propagation of uncertainty through arbitrary functions, even when the relationship between the measured quantities and the result is non-linear. For such cases, the analytical approach based on partial derivatives (as described in the GUM) quickly becomes tedious to apply and impractical to automate. This implementation aims to make composed uncertainty computation systematic and reusable, regardless of the complexity of the underlying function.


## Theoretical Foundations

This project relies on standard statistical formulas, following the GUM
(Guide to the Expression of Uncertainty in Measurement) framework.

### Mean and standard uncertainty (Type A)

For a series of N independent measurements $\{x_1, ..., x_N\}$ of the same
quantity, the mean is given by:

$$\bar{x} = \frac{1}{N}\sum_{i=1}^{N} x_i$$

The standard uncertainty $u(x)$ is estimated as the sample standard
deviation, using Bessel's correction ($N-1$ instead of $N$) to account for
the fact that the mean itself is estimated from the same data:

$$u(x) = \sqrt{\frac{1}{N-1}\sum_{i=1}^{N} (x_i - \bar{x})^2}$$

The uncertainty on the mean itself follows from the fact that averaging
reduces variability by a factor of $\sqrt{N}$:

$$u(\bar{x}) = \frac{u(x)}{\sqrt{N}}$$

### Type B uncertainty

When no variability can be observed (e.g. a single reading, or an
instrument's stated precision), the uncertainty is instead estimated from
an interval $[x-\Delta, x+\Delta]$ in which the true value is assumed to
lie with certainty. Assuming a uniform distribution over this interval,
the standard uncertainty is:

$$u(x) = \frac{\Delta}{\sqrt{3}}$$

The $\sqrt{3}$ factor comes from the standard deviation of a uniform
distribution over an interval of half-width $\Delta$.

### Composed uncertainty via Monte-Carlo

For a quantity $y = f(x_1, x_2, ..., x_n)$ resulting from several
measurements, each with its own standard uncertainty, the Monte-Carlo
method estimates $u(y)$ by simulating N random draws of each $x_i$
(uniformly distributed within its own interval), applying $f$ to each
draw, and computing the standard deviation of the resulting distribution
of $y$ values.
