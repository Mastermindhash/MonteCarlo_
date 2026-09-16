# Monte-Carlo Estimator 

This project implements composed uncertainty computation using the Monte-Carlo method, in accordance with the GUM (Guide to the Expression of Uncertainty in Measurement) framework studied as part of the CPGE (MPSI) curriculum.

The Monte-Carlo method is particularly valuable because it allows the propagation of uncertainty through arbitrary functions, even when the relationship between the measured quantities and the result is non-linear. For such cases, the analytical approach based on partial derivatives (as described in the GUM) quickly becomes tedious to apply and impractical to automate. This implementation aims to make composed uncertainty computation systematic and reusable, regardless of the complexity of the underlying function.
