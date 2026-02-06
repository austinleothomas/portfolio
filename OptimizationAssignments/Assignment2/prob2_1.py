# AEROSP 588 Fall 2025 - Assignment 2, Problem 1
# Authored By: Austin Leo Thomas
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- 
# We import modules as needed.
# ------------------------------------------------------------------------------------------- #
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator,FuncFormatter
# ------------------------------------------------------------------------------------------- #


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
# We define a function for implementing fixed-point iteration.
# ------------------------------------------------------------------------------------------- #
def FixedPoint(g,x0,StopCriteria,IterLimit):
    k = 0
    RelDifference = 1
    x = [0] * (IterLimit + 1)
    x[k] = x0
    while RelDifference > StopCriteria:
        x[k+1] = g(x[k])
        k += 1
        if k >= IterLimit:
            print('Fixed-point iteration method did not converge (iteration limit reached).')
            return [x,k]
        RelDifference = np.abs(x[k]-x[k-1])/(1 + np.abs(x[k]))
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
# We solve problem 2.1(a) and 2.1(b).
# ------------------------------------------------------------------------------------------- #
# We define provided values.
e_ProbAB = 0.7
M_ProbAB = np.pi/2

# We define criteria for our numerical solution.
StopCriteria_ProbAB = 1e-16
IterLimit_ProbAB = 50

# We define the initial guess.
E0_ProbAB = 35*np.pi/36

# We wrap the Kepler's equation functions for use in Newton's Method solver.
def f_ProbA(E):
    return KeplerEq(E,e_ProbAB,M_ProbAB)
def fdot_ProbA(E):
    return KeplerDerivative(E,e_ProbAB)

# We wrap the Kepler's equation function for use in fixed-point iteration solver.
def g_ProbB(E):
    return E - KeplerEq(E,e_ProbAB,M_ProbAB)
    
# We format the terminal output and call the Newton's method solver.
print()
print('PROBLEM 2.1(a) SOLUTION...')
[E_A,k_A] = Newt(f_ProbA,fdot_ProbA,E0_ProbAB,StopCriteria_ProbAB,IterLimit_ProbAB,False,0)
print('Solution converged to ' + str(E_A[k_A]) + ' radians after ' + str(k_A) + ' iterations.')
NewtonGamma = np.abs((E_A[k_A - 1] - E_A[k_A])/(E_A[k_A - 2] - E_A[k_A]))
print('Convergence constant is: ' + str(NewtonGamma))
print()

# We format the terminal output and call the fixed-point iteration solver.
print()
print('PROBLEM 2.1(b) SOLUTION:')
[E_B,k_B] = FixedPoint(g_ProbB,E0_ProbAB,StopCriteria_ProbAB,IterLimit_ProbAB)
print('Solution converged to ' + str(E_B[k_B]) + ' radians after ' + str(k_B) + ' iterations.')
FixedPointGamma = np.abs((E_B[k_B - 1] - E_B[k_B])/(E_B[k_B - 2] - E_B[k_B]))
print('Convergence constant is: ' + str(FixedPointGamma))
print()
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define general plot properties.
# ------------------------------------------------------------------------------------------- #
FontSize = 14
FontType = 'Cambria'
PlotColor = '#990e02'
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We solve Problem 2.1(e).
# ------------------------------------------------------------------------------------------- #
# We define e-values.
e_Array = [0,0.1,0.5,0.9]

# We define M-values.
M_Array = np.linspace(0,2*np.pi,100)

# We generate empty arrays for the E-values of each e/M combination.
E_Array = np.empty((len(M_Array),len(e_Array)))

# We define criteria for our numerical solution.
StopCriteria_ProbE = 1e-8
IterLimit_ProbE = 1000

# We define the initial guess.
E0_ProbE = np.pi

# We apply Newton's method for every e/M combination.
for i in range(len(M_Array)):
    for j in range(len(e_Array)):

        # We wrap the Kepler's equation functions for the current e/M combo.
        def f_ProbE(E):
            return KeplerEq(E,e_Array[j],M_Array[i])
        def fdot_ProbE(E):
            return KeplerDerivative(E,e_Array[j])

        # We call on the Newton's method solver.
        [Result,Iter] = Newt(f_ProbE,fdot_ProbE,E0_ProbE,StopCriteria_ProbE,IterLimit_ProbE,
                             False,0)
        E_Array[i,j] = Result[Iter]

# We define specific plot properties.
FigName_E = 'prob2_1_PlotE.svg'

# We generate the plot.
for index,e in enumerate(e_Array):
    plt.plot(M_Array,E_Array[:,index],label = 'e = ' + str(e))
plt.xlim([M_Array[0],M_Array[-1]])
plt.ylim([0,2*np.pi])
ax = plt.gca()
ax.set_xticks(np.arange(0,2*np.pi + 0.01,np.pi/2))
ax.set_yticks(np.arange(0,2*np.pi + 0.01,np.pi/2))
ax.set_xticklabels([r'$0$',r'$\frac{\pi}{2}$',r'$\pi$',r'$\frac{3\pi}{2}$',r'$2\pi$'],
                   fontsize = FontSize)
ax.set_yticklabels([r'$0$',r'$\frac{\pi}{2}$',r'$\pi$',r'$\frac{3\pi}{2}$',r'$2\pi$'],
                   fontsize = FontSize)
plt.xlabel('M',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
plt.ylabel('E',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
plt.legend(prop = {'family':FontType,'size':FontSize})
plt.savefig(FigName_E,bbox_inches = 'tight')
plt.clf()
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We solve Problem 2.1(f).
# ------------------------------------------------------------------------------------------- #
# We generate a range of M-values near pi/2.
M_Array_ProbF = np.linspace(np.pi/2 - 0.01,np.pi/2 + 0.01,100)

# We define the e-value.
eVal_ProbF = 0.7

# We define the convergence tolerance, stop criteria, and iteration limit.
Tolerance_ProbF = 0.01
StopCriteria_ProbF = 0
IterLimit_ProbF = 100

# We create an empty E-solution array.
E_Array_ProbF = [0] * len(M_Array_ProbF)

# We apply Newton's method.
for i in range(len(M_Array_ProbF)):

    # We wrap the Kepler's equation functions for the current M-value.
    def f_ProbF(E):
        return KeplerEq(E,eVal_ProbF,M_Array_ProbF[i])
    def fdot_ProbF(E):
        return KeplerDerivative(E,eVal_ProbF)
    
    # We define a random initial guess near the current M-value.
    currE0_ProbF = np.random.uniform(M_Array_ProbF[i] - 0.5,M_Array_ProbF[i] + 0.5)

    # We call on the Newton's method solver.
    [Result_ProbF,Iter_ProbF] = Newt(f_ProbF,fdot_ProbF,currE0_ProbF,StopCriteria_ProbF,
                         IterLimit_ProbF,True,Tolerance_ProbF)
    E_Array_ProbF[i] = Result_ProbF[Iter_ProbF]

# We define specific plot properties.
FigName_F = 'prob2_1_PlotF.svg'

# We generate the plot.
plt.plot(M_Array_ProbF,E_Array_ProbF)
plt.xlim([np.pi/2 - 0.01,np.pi/2 + 0.01])
plt.ylim([0.995 * E_Array_ProbF[0],1.005 * E_Array_ProbF[-1]])
ax = plt.gca()
ax.set_xticks([np.pi/2 - 0.01,np.pi/2,np.pi/2 + 0.01])
ax.set_yticks([0.995 * E_Array_ProbF[0],np.median(E_Array_ProbF),1.005 * E_Array_ProbF[-1]])
ax.set_xticklabels([r'$\frac{\pi}{2} - 0.01$',r'$\frac{\pi}{2}$',r'$\frac{\pi}{2} + 0.01$'],
                   fontsize = FontSize)
ax.set_yticklabels([f"{0.995 * E_Array_ProbF[0]:.3g}",f"{np.median(E_Array_ProbF):.3g}",
                    f"{1.005 * E_Array_ProbF[-1]:.3g}"],fontsize = FontSize)
plt.xlabel('M',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
plt.ylabel('E',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
plt.savefig(FigName_F,bbox_inches = 'tight')
plt.clf()
# ------------------------------------------------------------------------------------------- #