# Script to solve Problem 3.3 - 3.5 for AEROSP 588, Fall 2025.
# Written by and for Austin Leo Thomas.
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We import required modules.
# ------------------------------------------------------------------------------------------- #
import numpy as np
from scipy.optimize import minimize
from Toolbox.UnconstrainedOptimizer import UnconstrainedOptimizer
import matplotlib.pyplot as plt
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define each function.
# ------------------------------------------------------------------------------------------- #
def SlantedQuadratic(X):
    x1,x2 = X
    Beta = 1.5
    F = x1**2 + x2**2 - Beta * x1 * x2
    delF = np.zeros(2)
    delF[0] = 2 * x1 - Beta * x2
    delF[1] = 2 * x2 - Beta * x1
    return F,delF

def TwoDimRosenbrock(X):
    x1,x2 = X
    F = (1 - x1)**2 + 100 * (x2 - x1**2)**2
    delF = np.zeros(2)
    delF[0] = 2 * x1 - 400 * x1 * (x2 - x1**2) - 2
    delF[1] = 200 * (x2 - x1**2)
    return F,delF
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define necessary values.
# ------------------------------------------------------------------------------------------- #
X0_SlantedQuadratic = [1,2]
X0_TwoDimRosenbrock = [0,0]
Tau = 1e-6
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We call upon various optimization algorithms and record the design variable vectors at
# each iteration.
# ------------------------------------------------------------------------------------------- #
# For Strong Wolfe + Conjugate Gradient...
[
    Points_Slanted_StrongWolfe_ConjugateGradient,
 F_Slanted_StrongWolfe_ConjugateGradient,
 Calls_Slanted_StrongWolfe_ConjugateGradient,
 OptConditions_Slanted
 ] = UnconstrainedOptimizer(
     SlantedQuadratic,
     X0_SlantedQuadratic,
     Tau,
     options = {
         'LineSearchMethod':'Strong Wolfe',
         'DirectionSearchMethod':'Conjugate Gradient',
         'isReturnData':True
         }
)
[
    Points_Rosen_StrongWolfe_ConjugateGradient,
 F_Rosen_StrongWolfe_ConjugateGradient,
 Calls_Rosen_StrongWolfe_ConjugateGradient,
 OptConditions_Rosen
 ] = UnconstrainedOptimizer(
     TwoDimRosenbrock,
     X0_TwoDimRosenbrock,
     Tau,
     options = {
         'LineSearchMethod':'Strong Wolfe',
         'DirectionSearchMethod':'Conjugate Gradient',
         'isReturnData':True
         }
)

# For Strong Wolfe + Steepest Descent...
[
    Points_Slanted_StrongWolfe_SteepestDescent,
 F_Slanted_StrongWolfe_SteepestDescent,
 Calls_Slanted_StrongWolfe_SteepestDescent,
 _
 ] = UnconstrainedOptimizer(
     SlantedQuadratic,
     X0_SlantedQuadratic,
     Tau,
     options = {
         'LineSearchMethod':'Strong Wolfe',
         'DirectionSearchMethod':'Steepest Descent',
         'isReturnData':True
         }
)
[
    Points_Rosen_StrongWolfe_SteepestDescent,
 F_Rosen_StrongWolfe_SteepestDescent,
 Calls_Rosen_StrongWolfe_SteepestDescent,
 _
 ] = UnconstrainedOptimizer(
     TwoDimRosenbrock,
     X0_TwoDimRosenbrock,
     Tau,
     options = {
         'LineSearchMethod':'Strong Wolfe',
         'DirectionSearchMethod':'Steepest Descent',
         'isReturnData':True
         }
)

# For Backtracking + Conjugate Gradient....
[
    Points_Slanted_BackTrack_ConjugateGradient,
 F_Slanted_BackTrack_ConjugateGradient,
 Calls_Slanted_BackTrack_ConjugateGradient,
 _
 ] = UnconstrainedOptimizer(
     SlantedQuadratic,
     X0_SlantedQuadratic,
     Tau,
     options = {
         'LineSearchMethod':'Backtracking',
         'DirectionSearchMethod':'Conjugate Gradient',
         'isReturnData':True
         }
)
[
    Points_Rosen_BackTrack_ConjugateGradient,
 F_Rosen_BackTrack_ConjugateGradient,
 Calls_Rosen_BackTrack_ConjugateGradient,
 _
 ] = UnconstrainedOptimizer(
     TwoDimRosenbrock,
     X0_TwoDimRosenbrock,
     Tau,
     options = {
         'LineSearchMethod':'Backtracking',
         'DirectionSearchMethod':'Conjugate Gradient',
         'isReturnData':True
         }
)

# For Bactracking + Steepest Descent...
[
    Points_Slanted_BackTrack_SteepestDescent,
 F_Slanted_BackTrack_SteepestDescent,
 Calls_Slanted_BackTrack_SteepestDescent,
 _
 ] = UnconstrainedOptimizer(
     SlantedQuadratic,
     X0_SlantedQuadratic,
     Tau,
     options = {
         'LineSearchMethod':'Backtracking',
         'DirectionSearchMethod':'Steepest Descent',
         'isReturnData':True
         }
)
[
    Points_Rosen_BackTrack_SteepestDescent,
 F_Rosen_BackTrack_SteepestDescent,
 Calls_Rosen_BackTrack_SteepestDescent,
 _
 ] = UnconstrainedOptimizer(
     TwoDimRosenbrock,
     X0_TwoDimRosenbrock,
     Tau,
     options = {
         'LineSearchMethod':'Backtracking',
         'DirectionSearchMethod':'Steepest Descent',
         'isReturnData':True
         }
)
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define dispatcher functions to allow for passage of our functions to scipy.optimize, then
# we implement scipy.optimize.
# ------------------------------------------------------------------------------------------- #
# We define the function value wrapper.
def FuncDispatch(Func):
    def FuncWrapper(X):
        F,_ = Func(X)
        return F
    return FuncWrapper

# We define the gradient value wrapper.
def GradDispatch(Func):
    def GradWrapper(X):
        _,delF = Func(X)
        return delF
    return GradWrapper

# We implement scipy.minimize and save values.
Slanted_OTS_Result = minimize(
    FuncDispatch(SlantedQuadratic),
    X0_SlantedQuadratic,
    jac = GradDispatch(SlantedQuadratic),
    method = 'CG'
    )
TwoDimRosenbrock_OTS_Result = minimize(
    FuncDispatch(TwoDimRosenbrock),
    X0_TwoDimRosenbrock,
    jac = GradDispatch(TwoDimRosenbrock),
    method = 'CG'
    )
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We print to the command window.
# ------------------------------------------------------------------------------------------- #
print('-------------------------------------------------------------------------')
print('\n')
print('Slanted Optimum Point | Strong Wolfe + Conjugate Gradient: \n')
print(Points_Slanted_StrongWolfe_ConjugateGradient[-1].round(decimals = 3))
print('\n')
print('Slanted Optimum Value | Strong Wolfe + Conjugate Gradient: \n')
print(round(F_Slanted_StrongWolfe_ConjugateGradient,3))
print('\n')
print('Slanted Function Calls | Strong Wolfe + Conjugate Gradient: \n')
print(Calls_Slanted_StrongWolfe_ConjugateGradient)
print('\n')
print('Rosenbrock Optimum Point | Strong Wolfe + Conjugate Gradient: \n')
print(Points_Rosen_StrongWolfe_ConjugateGradient[-1].round(decimals = 3))
print('\n')
print('Rosenbrock Optimum Value | Strong Wolfe + Conjugate Gradient: \n')
print(round(F_Rosen_StrongWolfe_ConjugateGradient,3))
print('\n')
print('Rosenbrock Function Calls | Strong Wolfe + Conjugate Gradient: \n')
print(Calls_Rosen_StrongWolfe_ConjugateGradient)
print('\n')
print('-------------------------------------------------------------------------')
print('\n')
print('Slanted Optimum Point | Strong Wolfe + Steepest Descent: \n')
print(Points_Slanted_StrongWolfe_SteepestDescent[-1].round(decimals = 3))
print('\n')
print('Slanted Optimum Value | Strong Wolfe + Steepest Descent: \n')
print(round(F_Slanted_StrongWolfe_SteepestDescent,3))
print('\n')
print('Slanted Function Calls | Strong Wolfe + Steepest Descent: \n')
print(Calls_Slanted_StrongWolfe_SteepestDescent)
print('\n')
print('Rosenbrock Optimum Point | Strong Wolfe + Steepest Descent: \n')
print(Points_Rosen_StrongWolfe_SteepestDescent[-1].round(decimals = 3))
print('\n')
print('Rosenbrock Optimum Value | Strong Wolfe + Steepest Descent: \n')
print(round(F_Rosen_StrongWolfe_SteepestDescent,3))
print('\n')
print('Rosenbrock Function Calls | Strong Wolfe + Steepest Descent: \n')
print(Calls_Rosen_StrongWolfe_SteepestDescent)
print('\n')
print('-------------------------------------------------------------------------')
print('\n')
print('Slanted Optimum Point | Back Track + Conjugate Gradient: \n')
print(Points_Slanted_BackTrack_ConjugateGradient[-1].round(decimals = 3))
print('\n')
print('Slanted Optimum Value | Back Track + Conjugate Gradient: \n')
print(round(F_Slanted_BackTrack_ConjugateGradient,3))
print('\n')
print('Slanted Function Calls | Back Track + Conjugate Gradient: \n')
print(Calls_Slanted_BackTrack_ConjugateGradient)
print('\n')
print('Rosenbrock Optimum Point | Back Track + Conjugate Gradient: \n')
print(Points_Rosen_BackTrack_ConjugateGradient[-1].round(decimals = 3))
print('\n')
print('Rosenbrock Optimum Value | Back Track + Conjugate Gradient: \n')
print(round(F_Rosen_BackTrack_ConjugateGradient,3))
print('\n')
print('Rosenbrock Function Calls | Back Track + Conjugate Gradient: \n')
print(Calls_Rosen_BackTrack_ConjugateGradient)
print('\n')
print('-------------------------------------------------------------------------')
print('\n')
print('Slanted Optimum Point | Back Track + Steepest Descent: \n')
print(Points_Slanted_BackTrack_SteepestDescent[-1].round(decimals = 3))
print('\n')
print('Slanted Optimum Value | Back Track + Steepest Descent: \n')
print(round(F_Slanted_BackTrack_SteepestDescent,3))
print('\n')
print('Slanted Function Calls | Back Track + Steepest Descent: \n')
print(Calls_Slanted_BackTrack_SteepestDescent)
print('\n')
print('Rosenbrock Optimum Point | Back Track + Steepest Descent: \n')
print(Points_Rosen_BackTrack_SteepestDescent[-1].round(decimals = 3))
print('\n')
print('Rosenbrock Optimum Value | Back Track + Steepest Descent: \n')
print(round(F_Rosen_BackTrack_SteepestDescent,3))
print('\n')
print('Rosenbrock Function Calls | Back Track + Steepest Descent: \n')
print(Calls_Rosen_BackTrack_SteepestDescent)
print('\n')
print('-------------------------------------------------------------------------')
print('\n')
print('Slanted Optimum Point | SciPy CG Optimizer: \n')
print(Slanted_OTS_Result.x.round(decimals = 3))
print('\n')
print('Slanted Optimum Value | SciPy CG Optimizer: \n')
print(round(Slanted_OTS_Result.fun,3))
print('\n')
print('Slanted Function Calls | SciPy CG Optimizer: \n')
print(Slanted_OTS_Result.nfev)
print('\n')
print('Rosenbrock Optimum Point | SciPy CG Optimizer: \n')
print(TwoDimRosenbrock_OTS_Result.x.round(decimals = 3))
print('\n')
print('Rosenbrock Optimum Value | SciPy CG Optimizer: \n')
print(round(TwoDimRosenbrock_OTS_Result.fun,3))
print('\n')
print('Rosenbrock Function Calls | SciPy CG Optimizer: \n')
print(TwoDimRosenbrock_OTS_Result.nfev)
print('\n')
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define a function to generate the convergence plot.
# ------------------------------------------------------------------------------------------- #
def GenerateConvergencePlot(OrdinateVals,FileName):

    # We define properties of the plot.
    FontSize = 12
    FontType = 'Cambria'
    LineColor = '#b31919'
    LineWidth = 1

    # We define the abscissa values.
    AbscissaVals = range(len(OrdinateVals))

    # We generate the plot.
    plt.plot(AbscissaVals,OrdinateVals,color = LineColor,linewidth = LineWidth)
    plt.yscale('log')
    plt.xticks(fontsize = FontSize,fontname = FontType)
    plt.yticks(fontsize = FontSize,fontname = FontType)
    plt.xlabel('iterations',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
    plt.ylabel(r"$\left\| \nabla f \right\|_\infty$",fontsize = FontSize,
               fontname = FontType,fontstyle = 'italic')
    plt.savefig(FileName,bbox_inches = 'tight')
    plt.clf()
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We generate convergence plots for the Strong Wolfe + Conjugate Gradient solutions.
# ------------------------------------------------------------------------------------------- #
GenerateConvergencePlot(OptConditions_Slanted,'SlantedConvergencePlot.svg')
GenerateConvergencePlot(OptConditions_Rosen,'RosenConvergencePlot.svg')
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define a function to generate the path plot.
# ------------------------------------------------------------------------------------------- #
def GeneratePathPlot(X1,X2,F,ContourLevels,Points,x1Lim,x2Lim,FileName):
    
    # We define properties of the plot.
    FontSize = 11
    FontType = 'Cambria'
    LineColor = '#b31919'
    LineWidth = 1

    # We convert the collection of points to an array.
    Array = np.array(Points)

    # We create the contour plot.
    plt.contour(X1,X2,F,cmap = 'Blues_r',levels = ContourLevels,zorder = 1)
    plt.plot(Array[:,0],Array[:,1],color = LineColor,linewidth = LineWidth,zorder = 2)

    # We create annotations for the plot.
    plt.annotate(
        r'$x_0$',
        xy = (Array[0,0],Array[0,1]),
        xytext = (-20,0),
        textcoords = 'offset points',
        fontsize = FontSize,
        fontname = FontType,
        bbox = dict(
            boxstyle = 'round,pad = 0.1',
            fc = 'white',
            ec = 'white'
        )
    )
    plt.annotate(
        r'$x^*$',
        xy = (Array[-1,0],Array[-1,1]),
        xytext = (-20,0),
        textcoords = 'offset points',
        fontsize = FontSize,
        fontname = FontType,
        bbox = dict(
            boxstyle = 'round,pad = 0.1',
            fc = 'white',
            ec = 'white'
        )
    )
    
    # We finish configuring and saving the plot.
    plt.xlim(x1Lim)
    plt.ylim(x2Lim)
    plt.xticks(fontsize = FontSize,fontname = FontType)
    plt.yticks(fontsize = FontSize,fontname = FontType)
    plt.xlabel(r'$x_1$',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
    plt.ylabel(r'$x_2$',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
    plt.savefig(FileName,bbox_inches = 'tight')
    plt.clf()
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We generate path plots for the Strong Wolfe + Conjugate Gradient solutions.
# ------------------------------------------------------------------------------------------- #
# We generate x1, x2, and f values for the slanted quadratic.
x1_Slanted = np.linspace(-1,3,100)
x2_Slanted = np.linspace(-1,3,100)
F_Slanted = np.zeros((len(x1_Slanted),len(x2_Slanted)))
for i in range(len(x1_Slanted)):
    for j in range(len(x2_Slanted)):
        F_Slanted[i,j],_ = SlantedQuadratic((x1_Slanted[i],x2_Slanted[j]))

# We generate plotting values for the slanted quadratic.
Contours_Slanted = np.linspace(-5,20,30)
x1Bounds_Slanted = [x1_Slanted[0],x1_Slanted[-1]]
x2Bounds_Slanted = [x2_Slanted[0],x2_Slanted[-1]]
FileName_Slanted = 'SlantedPathPlot.svg'

# We generate x1, x2, and f values for the two-dimensional Rosenbrock function.
x1_Rosen = np.linspace(-0.25,1.25,100)
x2_Rosen = np.linspace(-0.25,1.25,100)
F_Rosen = np.zeros((len(x1_Rosen),len(x2_Rosen)))
for i in range(len(x1_Rosen)):
    for j in range(len(x2_Rosen)):
        F_Rosen[i,j],_ = TwoDimRosenbrock((x1_Rosen[i],x2_Rosen[j]))

# We generate plotting values for the two-dimensional Rosenbrock function.
Contours_Rosen = np.linspace(-5,100,20)
x1Bounds_Rosen = [x1_Rosen[0],x1_Rosen[-1]]
x2Bounds_Rosen = [x2_Rosen[0],x2_Rosen[-1]]
FileName_Rosen = 'RosenPathPlot.svg'

# We generate plots for both functions.
GeneratePathPlot(
    x1_Slanted,
    x2_Slanted,
    F_Slanted,
    Contours_Slanted,
    Points_Slanted_StrongWolfe_ConjugateGradient,
    x1Bounds_Slanted,
    x2Bounds_Slanted,
    FileName_Slanted
)
GeneratePathPlot(
    x1_Rosen,
    x2_Rosen,
    F_Rosen,
    Contours_Rosen,
    Points_Rosen_StrongWolfe_ConjugateGradient,
    x1Bounds_Rosen,
    x2Bounds_Rosen,
    FileName_Rosen
)
# ------------------------------------------------------------------------------------------- #