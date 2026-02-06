# Script to solve Problem 3.6 for AEROSP 588, Fall 2025.
# Written by and for Austin Leo Thomas.
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We import required modules.
# ------------------------------------------------------------------------------------------- #
import numpy as np
from Toolbox.UnconstrainedOptimizer import UnconstrainedOptimizer
import matplotlib.pyplot as plt
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define the function.
# ------------------------------------------------------------------------------------------- #
def Rosen(X):
    X = np.asarray(X)
    n = X.size
    F = np.sum(100 * (X[1:] - X[:-1]**2)**2 + (1 - X[:-1])**2)
    delF = np.zeros_like(X)
    delF[0] = -400 * X[0] * (X[1] - X[0]**2) - 2 * (1 - X[0])
    for i in range(1,n-1):
        delF[i] = 200 * (X[i] - X[i-1]**2) - 400 * X[i] * (X[i+1] - X[i]**2) - 2 * (1 - X[i])
    delF[-1] = 200 * (X[-1] - X[-2]**2)

    return F,delF
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# For increasing n-values, we try to optimize the Rosenbrock function. We use an intial
# guess of the origin for each iteration.
# ------------------------------------------------------------------------------------------- #
# We create storage objects.
IterStorage = []
nStorage = []
fStorage = []

# We define necessary values
Tau = 1e-3
isContinue = True
n = 2

# We define the optimizer options.
Options = {
    'isReturnData':True
}

# We solve.
while isContinue:
    x0 = np.zeros(n)
    Points,F,_,OptCondition = uncon_optimizer(
        Rosen,
        x0,
        Tau,
        Options
    )
    if (OptCondition[-1] > Tau):
        isContinue = False
    else:
        Iter = len(Points) - 1
        IterStorage.append(Iter)
        nStorage.append(n)
        fStorage.append(F)
        n = 2 * n
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define a function to generate the computational cost plot.
# ------------------------------------------------------------------------------------------- #
def GenerateCostPlot(AbscissaVals,OrdinateVals,FileName):

    # We define properties of the plot.
    FontSize = 12
    FontType = 'Cambria'
    LineColor = '#b31919'
    LineWidth = 1

    # We generate the plot.
    plt.plot(AbscissaVals,OrdinateVals,color = LineColor,linewidth = LineWidth)
    plt.xlim([AbscissaVals[0],AbscissaVals[-1]])
    plt.xticks(AbscissaVals,fontsize = FontSize,fontname = FontType)
    plt.yticks(fontsize = FontSize,fontname = FontType)
    plt.xlabel('n-value',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
    plt.ylabel('iterations',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
    plt.savefig(FileName,bbox_inches = 'tight')
    plt.clf()
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We generate the plot.
# ------------------------------------------------------------------------------------------- #
GenerateCostPlot(nStorage,IterStorage,'CostPlot.svg')
# ------------------------------------------------------------------------------------------- #