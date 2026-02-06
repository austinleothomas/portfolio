# Script for solving Problem 5.1  of Assignment 5 for U-M Fall 2025 AEROSP 588.
# Authored By: Austin Leo Thomas
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We import modules as needed.
# ---------------------------------------------------------------------------------------------- #
import numpy as np
import matplotlib.pyplot as plt
from Toolbox.MiscModules import GenLogArray,GenErrorPlot
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define the analytic derivative.
# ---------------------------------------------------------------------------------------------- #
def AnalyticDerivative(x):
    ex = np.exp(x)
    sx = np.sin(x)
    cx = np.cos(x)
    Num = ex * (2 * sx ** 3 + 2 * cx ** 3 + 3 * sx * cx ** 2 - 3 * sx ** 2 * cx)
    Den = 2 * (sx ** 3 + cx ** 3) ** 1.5
    fPrime = Num/Den
    return fPrime
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We generate overloaded function definitions. X in each input is a 2-long list, numpy array,
# or tuple. F in each output is a 2-long tuple.
# ---------------------------------------------------------------------------------------------- #
def expOL(X):
    x,xPrime = X
    f = np.exp(x)
    fPrime = xPrime * np.exp(x)
    return f,fPrime

def sinOL(X):
    x,xPrime = X
    f = np.sin(x)
    fPrime = xPrime * np.cos(x)
    return f,fPrime

def cosOL(X):
    x,xPrime = X
    f = np.cos(x)
    fPrime = -1 * xPrime * np.sin(x)
    return f,fPrime

def pwrOL(X,n):
    x,xPrime = X
    f = x ** n
    fPrime = xPrime * n * x**(n-1)
    return f,fPrime

def divOL(Num,Den):
    num,numPrime = Num
    den,denPrime = Den
    f = num / den
    fPrime = (den * numPrime - num * denPrime) / (den ** 2)
    return f,fPrime

def addOL(Term1,Term2):
    first,firstPrime = Term1
    second,secondPrime = Term2
    f = first + second
    fPrime = firstPrime + secondPrime
    return f,fPrime
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We generate function definitions.
# ---------------------------------------------------------------------------------------------- #
def Func(x):
    f = np.exp(x) / np.sqrt(np.sin(x) ** 3 + np.cos(x) ** 3)
    return f

def FuncOL(X):
    f,fPrime = divOL(expOL(X),pwrOL(addOL(pwrOL(sinOL(X),3),pwrOL(cosOL(X),3)),0.5))
    return f,fPrime
# ---------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------------------------------------------- #
# We generate functions to generate forward-, backward-, and central-difference approximations
# as well as a complex step approximation.
# ---------------------------------------------------------------------------------------------- #
def ForwardDif(f,x,h):
    fPrime = (f(x+h) - f(x)) / h
    return fPrime

def BackwardDif(f,x,h):
    fPrime = (f(x) - f(x-h)) / h
    return fPrime

def CentralDif(f,x,h):
    fPrime = (f(x+h) - f(x-h)) / (2*h)
    return fPrime

def ComplexStep(f,x,h):
    fComplex = f(x + h * 1j)
    fPrime = fComplex.imag / h
    return fPrime
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define the x-value of interest and the analytic derivative at this point.
# ---------------------------------------------------------------------------------------------- #
xPOI = 1.5
fPrime_Analytic = AnalyticDerivative(xPOI)
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We generate error values for forward-, backward-, and central-difference approximations as 
# well as the complex-step approximation as functions of h. We print the minimum of these
# results to the terminal for review.
# ---------------------------------------------------------------------------------------------- #
# We initially set the 'best' h-value index for each case as zero, to prevent errors.
hForwardIndex = 0
hBackwardIndex = 0
hCentralIndex = 0
hComplexIndex = 0

# We generate the arrays of h-values.
hArray = GenLogArray(-1,-25,10)

# We generate empty storage arrays for each finite difference approximation.
fPrime_Forward = np.empty_like(hArray)
fPrime_Backward = np.empty_like(hArray)
fPrime_Central = np.empty_like(hArray)
fPrime_Complex = np.empty_like(hArray)

# We generate empty storage arrays for the errors in each finite difference approximation.
errForward = np.empty_like(hArray)
errBackward = np.empty_like(hArray)
errCentral = np.empty_like(hArray)
errComplex = np.empty_like(hArray)

# We iterate through hArray, calculating the error in each finite-difference approximation at
# each h-value. For the complex-step solution, we record the largest h-value offering machine
# precision.
for i,h in enumerate(hArray):

    # We generate approximations.
    fPrime_Forward[i] = ForwardDif(Func,xPOI,h)
    fPrime_Backward[i] = BackwardDif(Func,xPOI,h)
    fPrime_Central[i] = CentralDif(Func,xPOI,h)
    fPrime_Complex[i] = ComplexStep(Func,xPOI,h)

    # We calculate and store the error in these approximations.
    errForward[i] = np.abs(fPrime_Analytic - fPrime_Forward[i]) / np.abs(fPrime_Analytic)
    errBackward[i] = np.abs(fPrime_Analytic - fPrime_Backward[i]) / np.abs(fPrime_Analytic)
    errCentral[i] = np.abs(fPrime_Analytic - fPrime_Central[i]) / np.abs(fPrime_Analytic)
    errComplex[i] = np.abs(fPrime_Analytic - fPrime_Complex[i]) / np.abs(fPrime_Analytic)

    # We check if the complex error is equal to zero, and adjust if so.
    if errComplex[i] == 0:
        errComplex[i] = 1e-16

    # We record the index of potentially ideal h-values for each case.
    if errForward[i] <= errForward[hForwardIndex]:
        hForwardIndex = i
    if errBackward[i] <= errBackward[hBackwardIndex]:
        hBackwardIndex = i
    if errCentral[i] <= errCentral[hCentralIndex]:
        hCentralIndex = i
    if errComplex[i] <= errComplex[hComplexIndex]:
        hComplexIndex = i
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We generate errors plots (modify arguments of GenErroPlot() to create different plots).
# ---------------------------------------------------------------------------------------------- #
GenErrorPlot(
    hArray,
    [errForward,errBackward,errCentral],
    ['Forward-Difference','Backward-Difference','Central-Difference'],
    [1e-25,1e-1],
    [1e-17,1e1],
    'StepSizeStudy_Prob1.svg',
    True,
    True
)
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We run computations for the complex-step method over a much larger range of h-values to detect
# underflow.
# ---------------------------------------------------------------------------------------------- #
# We define a boolean to identify whether or not we have found the underflow onset.
isSearchingUF = True

# We generate the array of h-values.
hArrayUF = GenLogArray(-1,-321,2)

# We generate empty storage arrays for the errors in each finite difference approximation.
errComplexUF = np.empty_like(hArrayUF)

# We iterate through hArrayUF, determining error in the complex-step approximation for each
# h-value in the array.
for i,h in enumerate(hArrayUF):

    # We generate the approximation.
    fPrime_ComplexUF = ComplexStep(Func,xPOI,h)

    # We calculate and store the error in these approximations.
    errComplexUF[i] = np.abs(fPrime_Analytic - fPrime_ComplexUF) / np.abs(fPrime_Analytic)

    # We check if the complex error is equal to zero, and adjust if so.
    if errComplexUF[i] == 0:
        errComplexUF[i] = 1e-16

    # We record the index of h-values which might mark the onset of underflow. We define the
    # criteria for the onset of underflow to be the smallest h-value for which the derivative
    # estimate is accurate to machine precision but all smaller h-values result greater error.
    if errComplexUF[i] == 1e-16 and all(err > 1e-16 for err in errComplexUF[:i]):
        hComplexIndexUF = i
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We compute the derivative at xPOI = 1.5 via operator overloading for forward-mode AD. We also
# compute the relative error in this approximation compared to the analytic result.
# ---------------------------------------------------------------------------------------------- #
_,fPrime_OL = FuncOL((xPOI,1))
errOL = np.abs(fPrime_Analytic - fPrime_OL) / np.abs(fPrime_Analytic)

if errOL == 0:
    errOL = 1e-16
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We print key results to the terminal.
# ---------------------------------------------------------------------------------------------- #
print('\n')
print('Analytic Result')
print('--------------------------------------------------')
print('f\'(x) true value: \t' + str(fPrime_Analytic))
print('\n')
print('Forward-Difference Method')
print('--------------------------------------------------')
print('ideal h-value: \t\t' + str(hArray[hForwardIndex]))
print('best f\'(1.5) estimate: \t' + str(fPrime_Forward[hForwardIndex]))
print('minumum relative error: ' + str(errForward[hForwardIndex]))
print('\n')
print('Backward-Difference Method')
print('--------------------------------------------------')
print('ideal h-value: \t\t' + str(hArray[hBackwardIndex]))
print('best f\'(1.5) estimate: \t' + str(fPrime_Backward[hBackwardIndex]))
print('minumum relative error: ' + str(errBackward[hBackwardIndex]))
print('\n')
print('Central-Difference Method')
print('--------------------------------------------------')
print('ideal h-value: \t\t' + str(hArray[hCentralIndex]))
print('best f\'(1.5) estimate: \t' + str(fPrime_Central[hCentralIndex]))
print('minumum relative error: ' + str(errCentral[hCentralIndex]))
print('\n')
print('Complex-Step Method')
print('--------------------------------------------------')
print('ideal h-value: \t\t' + str(hArray[hComplexIndex]))
print('best f\'(1.5) estimate: \t' + str(fPrime_Complex[hComplexIndex]))
print('minumum relative error: ' + str(errComplex[hComplexIndex]) + ' (MP)')
print('min step w/o underflow: ' + str(hArrayUF[hComplexIndexUF]))
print('\n')
print('Foward-Mode AD Method')
print('--------------------------------------------------')
print('f\'(1.5) estimate: \t' + str(fPrime_OL))
print('relative error: \t' + str(errOL) + ' (MP)')
print('\n')
# ---------------------------------------------------------------------------------------------- #