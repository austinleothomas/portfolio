# Script to solve Problem 6.3 for U-M AEROSP 588 Fall 2025.
# Authored By: Austin Leo Thomas
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We import modules as needed.
# ---------------------------------------------------------------------------------------------- #
import numpy as np
from TrajectoryPlotter.GradFreeOptimizer import GradFreeOptimizer as PSO
from TrajectoryPlotter.UnconstrainedOptimizer import UnconstrainedOptimizer
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define the multidimensional Rosenbrock function.
# ---------------------------------------------------------------------------------------------- #
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
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We solve the n-dimensional Rosenbrock function for various n-values with different methods.
# ---------------------------------------------------------------------------------------------- #
# We define the array of reasonable n-values to test.
nArray = [2,4,8,16]

# We define arrays of each relevant value for plotting later on.
PlottingValues_PSO = []
PlottingErrors_PSO = []
PlottingValues_NM = []
PlottingErrors_NM = []
PlottingValues_FD = []
PlottingErrors_FD = []
PlottingValues_BFGS = []
PlottingErrors_BFGS = []

# We define the sampling size for statistical analysis.
N = 10

# # We loop through each n-value.
# for n in nArray:

#     # We define design variable bounds.
#     xLower = -2 * np.ones(n)
#     xUpper = 2 * np.ones(n)

#     # We define Options for the PSO algorithm.
#     Options_PSO = {
#         'Lower Bound':xLower,
#         'Upper Bound':xUpper,
#         'Method':'PSO',
#         'Maximum Iterations':100000000
#     }

#     # We will run the PSO algorithm N times and select the best solution based on the minimal
#     # number of iterations / function calls. We create storage containers for the data.
#     # We generate a list for storing values.
#     xStarStorage_PSO = []
#     fStarStorage_PSO = []
#     IterStorage_PSO = []
#     FuncEvalsStorage_PSO = []
#     PointStorageStorage_PSO = []

#     # We run the PSO algorithm N times.
#     for Sample in range(N):
#         Output_PSO = PSO(Rosen,Options_PSO)
#         xStarStorage_PSO.append(Output_PSO['xStar'].copy())
#         fStarStorage_PSO.append(Output_PSO['fStar'].copy())
#         IterStorage_PSO.append(Output_PSO['Iter'])
#         FuncEvalsStorage_PSO.append(Output_PSO['FuncEvals'])

#     # We generate the mean and standard deviation in each design variable.
#     xStarMean_PSO = []
#     xStarStdDev_PSO = []
#     for xVal in range(len(xStarStorage_PSO[0])):
#         xValStorage_PSO = []
#         for Sample in range(N):
#             xValStorage_PSO.append(xStarStorage_PSO[Sample][xVal])
#         xStarMean_PSO.append(float(np.mean(np.asarray(xValStorage_PSO))))
#         xStarStdDev_PSO.append(float(np.std(np.asarray(xValStorage_PSO))))
    
#     # We generate statistical values for all other PSO results.
#     fStarMean_PSO = np.mean(fStarStorage_PSO)
#     fStarStdDev_PSO = np.std(fStarStorage_PSO)
#     IterMean_PSO = np.mean(IterStorage_PSO)
#     IterStdDev_PSO = np.std(IterStorage_PSO)
#     FuncEvalsMean_PSO = np.mean(FuncEvalsStorage_PSO)
#     FuncEvalsStdDev_PSO = np.std(FuncEvalsStorage_PSO)

#     # We print critical results to the terminal.
#     print('\n')
#     print('----------------------------------------------')
#     print('Problem 6.3(a) - n = 32 + N = 10')
#     print('----------------------------------------------')
#     print('\n')
#     print('=> Mean xStar',xStarMean_PSO)
#     print('=> Std Dev xStar: ',xStarStdDev_PSO)
#     print('=> Mean fStar: ',fStarMean_PSO)
#     print('=> Std Dev fStar: ',fStarStdDev_PSO)
#     print('=> Mean Iter: ',IterMean_PSO)
#     print('=> Std Dev Iter: ',IterStdDev_PSO)
#     print('=> Mean Func Evals: ',FuncEvalsMean_PSO)
#     print('=> Std Dev Func Evals: ',FuncEvalsStdDev_PSO)
#     print('\n')
#     print('----------------------------------------------')
#     print('\n')

# We execute the same procedure for the other methods.
for n in nArray:

    # We define the initial guess.
    x0 = -2 * np.ones(n)

    # We define CG Options.
    Options_Grad_D = {
        'isReturnData':True
    }

    # We call upon the CG optimizer.
    PointStorage_D,fStar_D,FuncEvals_D,_ = UnconstrainedOptimizer(
        Rosen,
        x0,
        Options_Grad_D
    )

    # We print critical results to the terminal.
    print('\n')
    print('----------------------------------------------')
    print('Problem 6.3(d) - n = ',n)
    print('----------------------------------------------')
    print('\n')
    print('=> xStar: ',PointStorage_D[-1])
    print('=> fStar: ',fStar_D)
    print('=> Func Evals: ',FuncEvals_D)
    print('\n')
    print('----------------------------------------------')

    # We define a dispatch functions.
    def Func(X):
        F,_ = Rosen(X)
        return F
    
    # We pass to SciPy's finite difference solver.
    Result_FD = minimize(
        Func,
        x0,
        method = 'L-BFGS-B',
        jac = None,
        options = {'disp':False}
    )

    # We print critical results to the terminal.
    print('\n')
    print('----------------------------------------------')
    print('Problem 6.3(c) - n = ',n)
    print('----------------------------------------------')
    print('\n')
    print('=> xStar: ',Result_FD.x)
    print('=> fStar: ',Result_FD.fun)
    print('=> Func Evals: ',Result_FD.nfev)
    print('\n')
    print('----------------------------------------------')

    # We pass to SciPy's Nelder-Mead solver.
    Result_NM = minimize(
        Func,
        x0,
        method = 'Nelder-Mead',
        options = {'disp':False}
    )

    # We print critical results to the terminal.
    print('\n')
    print('----------------------------------------------')
    print('Problem 6.3(b) - n = ',n)
    print('----------------------------------------------')
    print('\n')
    print('=> xStar: ',Result_NM.x)
    print('=> fStar: ',Result_NM.fun)
    print('=> Func Evals: ',Result_NM.nfev)
    print('\n')
    print('----------------------------------------------')
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We plot.
# ---------------------------------------------------------------------------------------------- #
# We define plot properties.
    FontSize = 12
    FontType = 'Cambria'
    LineColors = ['#b31919','#0a820e','#072587','#ab0a95']
    LineWidth = 1

# We define ordinate values. Note: I hard-code the FuncEval results here because running all of
# this script at once would take over an hour -- I evaluated everything piecewise but obviously
# can't save values between program executions. So I just hard-coded it. Forgive me.
OrdinateVals = [[195716,915042,3346928,3800888],
                [149,570],
                [102,245,684,2057],
                [6833,40176,29159,29884]
                ]

# We define legend labels.
LegendLabels = ['PSO','NM','FD','CG']

# We plot.
for i,Data in enumerate(OrdinateVals):
    if i != 1:
        plt.plot(
            nArray,
            Data,
            color = LineColors[i],
            linewidth = LineWidth,
            label = LegendLabels[i]
        )
    else:
        plt.plot(
            [2,4],
            Data,
            color = LineColors[i],
            linewidth = LineWidth,
            label = LegendLabels[i]
        )

# We configure plot.
plt.xscale('log')
plt.yscale('log')
ax = plt.gca()
ax.xaxis.set_major_locator(ticker.FixedLocator(nArray))
ax.set_xticklabels([str(n) for n in nArray])
ax.xaxis.set_minor_locator(ticker.NullLocator())
plt.xticks(fontsize = FontSize,fontname = FontType)
plt.yticks(fontsize = FontSize,fontname = FontType)
plt.xlabel(r'function dimensionality, n',fontsize = FontSize,fontname = FontType,
            fontstyle = 'italic')
plt.ylabel(r'function evaluations',fontsize = FontSize,fontname = FontType,
           fontstyle = 'italic')
plt.legend(loc ='upper left')
plt.savefig('Prob_6_3_Plot.svg',bbox_inches = 'tight')
plt.show()
plt.clf()
# ---------------------------------------------------------------------------------------------- #