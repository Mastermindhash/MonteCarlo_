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


## Architecture

This implementation follows a three-layer object-oriented design.

The first layer is the Measurement class, which represents a single measurement as a value paired with its standard uncertainty. This encapsulation is valuable because it decouples how an uncertainty was obtained (through statistical analysis of a series, or through an instrument's stated precision) from how it is later used — in particular, by the Monte-Carlo estimator, which only needs a value and an uncertainty, regardless of their origin.

The second layer is the MeasurementSerie class, which represents a statistical series of repeated measurements and implements the usual statistical methods (mean, variance, standard deviation) needed to compute a Type A uncertainty. Separating this logic into its own class is valuable because it isolates the statistical computation itself from how the resulting uncertainty is later used.

The third and central layer is the MonteCarloEstimator class, which implements the Monte-Carlo simulation itself. Given a list of Measurement instances (each possibly originating from a MeasurementSerie, via Type A estimation, or from a direct Type B estimation) and a function f combining them, it estimates the resulting composed uncertainty by repeated random sampling. This is the central class of the project: it is what allows uncertainty propagation through arbitrary — including non-linear — functions, without requiring an analytical derivation.


## Validation

To validate the Monte-Carlo estimator, its result was compared against the
analytical formula based on partial derivatives (GUM section on composed
uncertainties, general case):

$$u(y) = \sqrt{\sum_{i=1}^{n} \left(\frac{\partial f}{\partial x_i} u(x_i)\right)^2}$$

For the parallel resistance example ($R_{eq} = \frac{R_1 R_2}{R_1+R_2}$):

$$\frac{\partial R_{eq}}{\partial R_1} = \frac{R_2^2}{(R_1+R_2)^2}, \quad
\frac{\partial R_{eq}}{\partial R_2} = \frac{R_1^2}{(R_1+R_2)^2}$$

| Method              | R_eq (Ω) | u(R_eq) (Ω) |
|---------------------|----------|-------------|
| Analytical (partial derivatives) | *TODO* | *TODO* |
| Monte-Carlo (N = 100 000)        | *TODO* | *TODO* |

The two methods agree within *TODO*%, confirming the correctness of the
Monte-Carlo implementation.

## Limitations

- Only uniform distributions are supported for Type B uncertainty; other
  distributions (e.g. Gaussian) would require extending the sampling logic
  in `MonteCarloEstimator`.
- No explicit error handling for edge cases (e.g. a series of size 1, or
  division by zero within `f`).
- The order of `Measurement` instances passed to `MonteCarloEstimator`
  must match the argument order expected by `f`; no validation is
  performed on this correspondence.


## Usage

Requires `numpy`.

\`\`\`python
from monte_carlo import Measurement, MeasurementSerie, MonteCarloEstimator

# Type A: repeated measurements
r1_series = MeasurementSerie([220.4, 219.8, 220.1, 220.6, 219.9, 220.3])
R1 = r1_series.to_measurement()

# Type B: single reading with known instrument precision
R2 = Measurement(value=330.0, uncertainty=1.5 / (3 ** 0.5))

f = lambda r1, r2: (r1 * r2) / (r1 + r2)
estimator = MonteCarloEstimator(f=f, N=100_000, measurement_list=[R1, R2])
u_Req = estimator.estimate()
\`\`\`




































































