# Script for solving Problem 5.3  of Assignment 5 for U-M Fall 2025 AEROSP 588.
# Authored By: Austin Leo Thomas
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We import modules as needed.
# ---------------------------------------------------------------------------------------------- #
import numpy as np
from truss import TenBarTrussFEA
from Toolbox.MiscModules import GenLogArray,GenErrorPlot
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We generate our A-array.
# ---------------------------------------------------------------------------------------------- #
A = np.ones((10,1))
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We compute derivatives via all methods.
# ---------------------------------------------------------------------------------------------- #
fdSol = TenBarTrussFEA(A,{'GradMethod':'FD'})
csSol = TenBarTrussFEA(A,{'GradMethod':'CS'})
dtSol = TenBarTrussFEA(A,{'GradMethod':'DT'})
ajSol = TenBarTrussFEA(A,{'GradMethod':'AJ'})
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We calculate the maximum absolute error in each method, assuming the DT method provides an
# exact derivative.
# ---------------------------------------------------------------------------------------------- #
fdError = fdSol['dSdA'] - dtSol['dSdA']
csError = csSol['dSdA'] - dtSol['dSdA']
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We print results to the terminal.
# ---------------------------------------------------------------------------------------------- #
np.set_printoptions(precision = 0,suppress = True)

print('\n')
print('For FD...')
print(np.round(fdSol['dSdA'],0))
print('\n')
print('For CS...')
print(np.round(csSol['dSdA'],0))
print('\n')
print('For DT...')
print(np.round(dtSol['dSdA'],0))
print('\n')
print('For AJ...')
print(np.round(ajSol['dSdA'],0))
print('\n')
print('Max. FD Error...')
print(np.max(fdError))
print('\n')
print('Max. CS Error...')
print(np.max(csError))
print('\n')
# ---------------------------------------------------------------------------------------------- #