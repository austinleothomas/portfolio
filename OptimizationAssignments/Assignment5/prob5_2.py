# Script for solving Problem 5.2  of Assignment 5 for U-M Fall 2025 AEROSP 588.
# Authored By: Austin Leo Thomas
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We import modules as needed.
# ---------------------------------------------------------------------------------------------- #
import numpy as np
# ---------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------- #
# We define a function for implementing Newton's method.
# ------------------------------------------------------------------------------------------- #
def Newt(f,fdot,x0,StopCriteria,IterLimit,isTolerance,Tolerance):
    k = 0
    RelDifference = 1
    x = [0] * (IterLimit + 1)
    x[k] = x0
    while RelDifference > StopCriteria:
        x[k+1] = x[k] - f(x[k])/fdot(x[k])
        k += 1
        if k >= IterLimit:
            print('Newton\'s method did not converge (iteration limit reached).')
            return [x,k]
        RelDifference = np.abs(x[k]-x[k-1])/(1 + np.abs(x[k]))
        if isTolerance and np.abs(f(x[k])) < Tolerance:
            print('Convergence tolerance met at ' + str(k) + ' iterations.')
            return [x,k]
    return [x,k]
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define Kepler's equation as a residual and the derivative of this residual with respect
# to eccentric anomaly, E.
# ------------------------------------------------------------------------------------------- #
def KeplerEq(E,e,M):
    Residual = E - e*np.sin(E) - M
    return Residual

def KeplerDerivative(E,e):
    Residual = 1 - e*np.cos(E)
    return Residual
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define e- and M-values.
# ------------------------------------------------------------------------------------------- #
e = 0.8
Mvals = [np.pi / 3 , np.pi / 2 , 3 * np.pi / 4]
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define the analytic df/dM expression.
# ------------------------------------------------------------------------------------------- #
def AnalyticDerivative(E):
    Sol = 1 / (1 - e * np.cos(E)) - 1
    return Sol
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define the f(E,M).
# ------------------------------------------------------------------------------------------- #
def Func(E,M):
    f = E - M
    return f
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We evaluate E at all M-values, including perturbed M-values.
# ------------------------------------------------------------------------------------------- #
# We define the step size.
h = 5e-6

# We create empty arrays to populate with these E-values.
Evals = np.zeros_like(Mvals)
Evals_PosPerturb = np.zeros_like(Mvals)
Evals_NegPerturb = np.zeros_like(Mvals)

# We create empty arrays for the perturbed M-values.
M_PosPerturb = np.empty_like(Mvals)
M_NegPerturb = np.empty_like(Mvals)

for i in range(len(Mvals)):

    # We perturb the M-value.
    M_PosPerturb[i] = Mvals[i] + h
    M_NegPerturb[i] = Mvals[i] - h

    # We wrap the Kepler's equation functions for use in Newton's method solver.
    def KepWrapper(E):
        return KeplerEq(E,e,Mvals[i])
    def KepWrapper_PosPerturb(E):
        return KeplerEq(E,e,M_PosPerturb[i])
    def KepWrapper_NegPerturb(E):
        return KeplerEq(E,e,M_NegPerturb[i])
    def KepDerivativeWrapper(E):
        return KeplerDerivative(E,e)
    
    # We call on the Newton's method solver for the exact and perturbed M-values.
    [E_Result,k_Result] = Newt(
        KepWrapper,
        KepDerivativeWrapper,
        np.pi,
        1e-12,
        1000,
        False,
        0
    )
    [E_Result_PosPerturb,k_Result_PosPerturb] = Newt(
        KepWrapper_PosPerturb,
        KepDerivativeWrapper,
        np.pi,
        1e-12,
        1000,
        False,
        0
    )
    [E_Result_NegPerturb,k_Result_NegPerturb] = Newt(
        KepWrapper_NegPerturb,
        KepDerivativeWrapper,
        np.pi,
        1e-12,
        1000,
        False,
        0
    )

    # We populate the E-values storage arrays.
    Evals[i] = E_Result[k_Result]
    Evals_PosPerturb[i] = E_Result_PosPerturb[k_Result_PosPerturb]
    Evals_NegPerturb[i] = E_Result_NegPerturb[k_Result_NegPerturb]
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We evaluate the derivatives at each value.
# ------------------------------------------------------------------------------------------- #
# We create empty arrays for the results.
AnalyticResults = np.empty_like(Mvals)
ApproxResults = np.empty_like(Mvals)

# We iterate for each M-value.
for i in range(len(Mvals)):

    # We calculate the analytic derivative.
    AnalyticResults[i] = AnalyticDerivative(Evals[i])

    # We calculate the approximate derivative via central-difference.
    ApproxResults[i] = (Func(Evals_PosPerturb[i],M_PosPerturb[i]) - \
                        Func(Evals_NegPerturb[i],M_NegPerturb[i])) / (2 * h)
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We print results to the terminal.
# ------------------------------------------------------------------------------------------- #
print('\n')
print('For M = pi/3...')
print('Analytic Solution = ' + str(AnalyticResults[0]))
print('Approximate Solution = ' + str(ApproxResults[0]))
print('\n')
print('For M = pi/2...')
print('Analytic Solution = ' + str(AnalyticResults[1]))
print('Approximate Solution = ' + str(ApproxResults[1]))
print('\n')
print('For M = 3 * pi/4...')
print('Analytic Solution = ' + str(AnalyticResults[2]))
print('Approximate Solution = ' + str(ApproxResults[2]))
print('\n')
# ------------------------------------------------------------------------------------------- #