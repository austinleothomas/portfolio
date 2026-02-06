# Script to solve Problem 6.2 for U-M AEROSP 588 Fall 2025.
# Authored By: Austin Leo Thomas
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We import modules as needed.
# ---------------------------------------------------------------------------------------------- #
import numpy as np
from Toolbox.GradFreeOptimizer import GradFreeOptimizer as Optimize
from Toolbox.OptimizationModules import MultiParticlePlotter
from Toolbox.UnconstrainedOptimizer import UnconstrainedOptimizer
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define the bean function.
# ---------------------------------------------------------------------------------------------- #
def BeanFunc(X):
    x1,x2 = X
    F = (1 - x1)**2 + (1 - x2)**2 + 0.5 * (2 * x2 - x1**2)**2
    DelF = np.zeros(2)
    DelF[0] = -2 * (1 - x1) - 2 * x1 * (2 * x2 - x1**2)
    DelF[1] = -2 * (1 - x2) + 2 * ( 2 * x2 - x1**2)
    return F,DelF
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define the noisy bean function.
# ---------------------------------------------------------------------------------------------- #
def NoisyBeanFunc(X,NoiseMag):
    FuncNoise = np.random.normal(loc = 0,scale = NoiseMag)
    GradNoise = np.zeros(2)
    GradNoise[0] = np.random.normal(loc = 0,scale = NoiseMag)
    GradNoise[1] = np.random.normal(loc = 0,scale = NoiseMag)
    F,DelF = BeanFunc(X)
    nF = F + FuncNoise
    nDelF = DelF + GradNoise
    return nF,nDelF
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define the checkered bean function.
# ---------------------------------------------------------------------------------------------- #
def CheckeredBeanFunc(X,StepMag):
    x1,x2 = X
    DeltaF = StepMag * np.ceil(np.sin(np.pi * x1) * np.sin(np.pi * x2))
    F,DelF = BeanFunc(X)
    cF = F + DeltaF
    cDelF = DelF
    return cF,cDelF
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define the function described in Problem 6.2(d).
# ---------------------------------------------------------------------------------------------- #
def Func(X):
    x1,x2,x3 = X
    F = np.abs(x1) + 2 * np.abs(x2) + x3**2
    DelF = np.zeros(3)
    if x1 >= 0:
        DelF[0] = 1
    else:
        DelF[0] = -1
    if x2 > 0:
        DelF[1] = 1
    else:
        DelF[1] = -1
    DelF[2] = 2 * x3
    return F,DelF
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We compute n samples of the PSO solution, making note of the best and worst (measured by the
# number of iterations required for convergence) solutions. From this we conduct statistical
# analysis of the results to provide a solution for Problem 6.2(a). We also generate plots of
# critical generations for the best and worst optimization cycles.
# ---------------------------------------------------------------------------------------------- #
# We define the n-value for the statistical study.
n_A = 2

# We define the lower and upper bounds of the problem exploration.
LowerBounds_A = [-3,-3]
UpperBounds_A = [3,3]

# We define the Options for the Optimizer.
Options_A = {
    'Lower Bound':LowerBounds_A,
    'Upper Bound':UpperBounds_A,
    'Method':'PSO'
}

# We generate a list for storing values.
xStarStorage_A = []
fStarStorage_A = []
IterStorage_A = []
FuncEvalsStorage_A = []
PointStorageStorage_A = []

# We generate the n = 30 optimization samples.
for i in range(n_A):
    Output = Optimize(BeanFunc,Options_A)
    xStarStorage_A.append(Output['xStar'].copy())
    fStarStorage_A.append(Output['fStar'].copy())
    IterStorage_A.append(Output['Iter'])
    FuncEvalsStorage_A.append(Output['FuncEvals'])
    PointStorageStorage_A.append(Output['PointStorage'].copy())

# We obtain the mean and uncertainty of each optimal design variable.
xStarMean_A = np.zeros_like(xStarStorage_A[0])
xStarStdDev_A = np.zeros_like(xStarStorage_A[0])
for i in range(len(xStarMean_A)):
    SampledVariables = np.zeros(n_A)
    for j in range(n_A):
        SampledVariables[j] = xStarStorage_A[j][i]
    xStarMean_A[i] = np.mean(SampledVariables)
    xStarStdDev_A[i] = np.std(SampledVariables)

# We obtain the mean and uncertainty of all other sampled variables.
fStarMean_A = np.mean(fStarStorage_A)
fStarStdDev_A = np.std(fStarStorage_A)
IterMean_A = np.mean(IterStorage_A)
IterStdDev_A = np.std(IterStorage_A)
FuncEvalsMean_A = np.mean(FuncEvalsStorage_A)
FuncEvalsStdDev_A = np.std(FuncEvalsStorage_A)

# We identify the index of the best and worst optimization cycles.
MinIndex_A = np.argmin(IterStorage_A)
MaxIndex_A = np.argmax(IterStorage_A)

# We print critical results to the terminal.
print('\n')
print('----------------------------------------------')
print('Problem 6.2(a) Critical Results')
print('----------------------------------------------')
print('\n')
print('BEST RESULT...')
print('=> xStar: ',xStarStorage_A[MinIndex_A])
print('=> fStar: ',fStarStorage_A[MinIndex_A])
print('=> Iter: ',IterStorage_A[MinIndex_A])
print('=> Func Evals: ',FuncEvalsStorage_A[MinIndex_A])
print('\n')
print('STATISTICAL RESULTS (n = 30)...')
print('=> Mean xStar',xStarMean_A)
print('=> Std Dev xStar: ',xStarStdDev_A)
print('=> Mean fStar: ',fStarMean_A)
print('=> Std Dev fStar: ',fStarStdDev_A)
print('=> Mean Iter: ',IterMean_A)
print('=> Std Dev Iter: ',IterStdDev_A)
print('=> Mean Func Evals: ',FuncEvalsMean_A)
print('=> Std Dev Func Evals: ',FuncEvalsStdDev_A)
print('\n')
print('----------------------------------------------')

# We configure plotting features for the bean function.
Contours_A = np.linspace(-20,100,30)
CritIters_A = [0,10,25,50,75,100,500,1000,5000,10000,50000]

# We define values for the contour plot.
X1 = np.linspace(LowerBounds_A[0],UpperBounds_A[0],100)
X2 = np.linspace(LowerBounds_A[1],UpperBounds_A[1],100)
F = np.zeros((len(X1),len(X2)))
for i in range(len(X1)):
    for j in range(len(X2)):
        F[j,i],_ = BeanFunc((X1[i],X2[j]))

# We offer data for these best and worst cases to the plotting function.
MultiParticlePlotter(
    X1,
    X2,
    F,
    PointStorageStorage_A[MinIndex_A],
    Contours_A,
    IterStorage_A[MinIndex_A],
    CritIters_A,
    LowerBounds_A,
    UpperBounds_A,
    'Prob_6_2_WorstCasePlot',
    True,
    False,
    False
)
MultiParticlePlotter(
    X1,
    X2,
    F,
    PointStorageStorage_A[MaxIndex_A],
    Contours_A,
    IterStorage_A[MaxIndex_A],
    CritIters_A,
    LowerBounds_A,
    UpperBounds_A,
    'Prob_6_2_BestCasePlot',
    True,
    False,
    False
)
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# For various noise levels, we apply the gradient-free approach (n = 10) and a gradient-based
# approach (n = 10). For each noise value, statistical values are derived for the gradient-free
# approach and printed to the terminal alongside comparable values for the gradient-based
# approach.
# ---------------------------------------------------------------------------------------------- #
# We define the noise levels of interest.
NoiseLevels_B = [1e-4]

# We define the statistical n-value.
n_B = 1

# We define the lower and upper bounds of the problem exploration.
LowerBounds_B = [-3,-3]
UpperBounds_B = [3,3]

# We define the Options for both optimizers.
Options_Grad_B = {
    'isReturnData':True
}
Options_Free_B = {
    'Lower Bound':LowerBounds_B,
    'Upper Bound':UpperBounds_B,
    'Maximum Iterations':10000,
    'Method':'PSO'
}

# We iterate through each noise level, optimize, and print results to the terminal.
for NoiseLevel in NoiseLevels_B:

    # We dispatch for the current noisy function.
    DispatchFunc_B = lambda X: NoisyBeanFunc(X,NoiseLevel)

    # We define storage containers for statistically-relevant values for the gradient-based approach.
    x1Vals_Grad_B = []
    x2Vals_Grad_B = []
    fStarVals_Grad_B = []
    FuncEvalsVals_Grad_B = []

    # We define storage containers for statistically-relevant values for the gradient-free approach.
    x1Vals_Free_B = []
    x2Vals_Free_B = []
    fStarVals_Free_B = []
    FuncEvalsVals_Free_B = []

    # We iterate through the sampling instances.
    for Sample in range(n_B):

        # We generate a random initial guess for the gradient-based method.
        x1_Init = np.random.uniform(LowerBounds_B[0],UpperBounds_B[0])
        x2_Init = np.random.uniform(LowerBounds_B[1],UpperBounds_B[1])
        X0 = (x1_Init,x2_Init)

        # We run the gradient-based approach.
        PointStorage_Grad,fStar_Grad,FuncEvals_Grad,_ = UnconstrainedOptimizer(
            DispatchFunc_B,
            X0,
            Options_Grad_B
        )

        # We store data for the gradient-based approach.
        x1Vals_Grad_B.append(PointStorage_Grad[-1][0])
        x2Vals_Grad_B.append(PointStorage_Grad[-1][1])
        fStarVals_Grad_B.append(fStar_Grad)
        FuncEvalsVals_Grad_B.append(FuncEvals_Grad)

        # We run the gradient-free approach.
        Output_Free = Optimize(
            DispatchFunc_B,
            Options_Free_B
        )

        # We store data for the gradient-free approach.
        x1Vals_Free_B.append(Output_Free['xStar'][0].copy())
        x2Vals_Free_B.append(Output_Free['xStar'][1].copy())
        fStarVals_Free_B.append(Output_Free['fStar'].copy())
        FuncEvalsVals_Free_B.append(Output_Free['FuncEvals'])

    # We compute statistical values for the gradient-based method.
    xStarMean_Grad_B = []
    xStarMean_Grad_B.append(float(np.mean(x1Vals_Grad_B)))
    xStarMean_Grad_B.append(float(np.mean(x2Vals_Grad_B)))
    xStarStdDev_Grad_B = []
    xStarStdDev_Grad_B.append(float(np.std(x1Vals_Grad_B)))
    xStarStdDev_Grad_B.append(float(np.std(x2Vals_Grad_B)))
    fStarMean_Grad_B = np.mean(fStarVals_Grad_B)
    fStarStdDev_Grad_B = np.std(fStarVals_Grad_B)
    FuncEvalsMean_Grad_B = np.mean(FuncEvalsVals_Grad_B)
    FuncEvalsStdDev_Grad_B = np.std(FuncEvalsVals_Grad_B)

    # We compute statistical values for the gradient-free method.
    xStarMean_Free_B = []
    xStarMean_Free_B.append(float(np.mean(x1Vals_Free_B)))
    xStarMean_Free_B.append(float(np.mean(x2Vals_Free_B)))
    xStarStdDev_Free_B = []
    xStarStdDev_Free_B.append(float(np.std(x1Vals_Free_B)))
    xStarStdDev_Free_B.append(float(np.std(x2Vals_Free_B)))
    fStarMean_Free_B = np.mean(fStarVals_Free_B)
    fStarStdDev_Free_B = np.std(fStarVals_Free_B)
    FuncEvalsMean_Free_B = np.mean(FuncEvalsVals_Free_B)
    FuncEvalsStdDev_Free_B = np.std(FuncEvalsVals_Free_B)

    # We print critical results to the terminal.
    print('\n')
    print('----------------------------------------------')
    print('Problem 6.2(b) - Noise of ',str(NoiseLevel))
    print('----------------------------------------------')
    print('\n')
    print('GRAD-BASED RESULTS...')
    print('=> Mean xStar',xStarMean_Grad_B)
    print('=> Std Dev xStar: ',xStarStdDev_Grad_B)
    print('=> Mean fStar: ',fStarMean_Grad_B)
    print('=> Std Dev fStar: ',fStarStdDev_Grad_B)
    print('=> Mean Func Evals: ',FuncEvalsMean_Grad_B)
    print('=> Std Dev Func Evals: ',FuncEvalsStdDev_Grad_B)
    print('\n')
    print('GRAD-FREE RESULTS...')
    print('=> Mean xStar',xStarMean_Free_B)
    print('=> Std Dev xStar: ',xStarStdDev_Free_B)
    print('=> Mean fStar: ',fStarMean_Free_B)
    print('=> Std Dev fStar: ',fStarStdDev_Free_B)
    print('=> Mean Func Evals: ',FuncEvalsMean_Free_B)
    print('=> Std Dev Func Evals: ',FuncEvalsStdDev_Free_B)
    print('\n')
    print('----------------------------------------------')
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# For various step sizes, we apply the gradient-free approach (n = 10) and a gradient-based
# approach (n = 10). For each step size, statistical values are derived for the gradient-free
# approach and printed to the terminal alongside comparable values for the gradient-based
# approach.
# ---------------------------------------------------------------------------------------------- #
# We define the noise levels of interest.
StepMags_C = [4]

# We define the statistical n-value.
n_C = 2

# We define the lower and upper bounds of the problem exploration.
LowerBounds_C = [-3,-3]
UpperBounds_C = [3,3]

# We define the Options for both optimizers.
Options_Grad_C = {
    'isReturnData':True
}
Options_Free_C = {
    'Lower Bound':LowerBounds_C,
    'Upper Bound':UpperBounds_C,
    'Maximum Iterations':10000,
    'Method':'PSO'
}

# We iterate through each noise level, optimize, and print results to the terminal.
for StepMag in StepMags_C:

    # We dispatch for the current noisy function.
    DispatchFunc_C = lambda X: CheckeredBeanFunc(X,StepMag)

    # We define storage containers for statistically-relevant values for the gradient-based approach.
    x1Vals_Grad_C = []
    x2Vals_Grad_C = []
    fStarVals_Grad_C = []
    FuncEvalsVals_Grad_C = []

    # We define storage containers for statistically-relevant values for the gradient-free approach.
    x1Vals_Free_C = []
    x2Vals_Free_C = []
    fStarVals_Free_C = []
    FuncEvalsVals_Free_C = []

    # We iterate through the sampling instances.
    for Sample in range(n_C):

        # We generate a random initial guess for the gradient-based method.
        x1_Init = np.random.uniform(LowerBounds_C[0],UpperBounds_C[0])
        x2_Init = np.random.uniform(LowerBounds_C[1],UpperBounds_C[1])
        X0 = (x1_Init,x2_Init)

        # We run the gradient-based approach.
        PointStorage_Grad,fStar_Grad,FuncEvals_Grad,_ = UnconstrainedOptimizer(
            DispatchFunc_C,
            X0,
            Options_Grad_C
        )

        # We store data for the gradient-based approach.
        x1Vals_Grad_C.append(PointStorage_Grad[-1][0])
        x2Vals_Grad_C.append(PointStorage_Grad[-1][1])
        fStarVals_Grad_C.append(fStar_Grad)
        FuncEvalsVals_Grad_C.append(FuncEvals_Grad)

        # We run the gradient-free approach.
        Output_Free = Optimize(
            DispatchFunc_C,
            Options_Free_C
        )

        # We store data for the gradient-free approach.
        x1Vals_Free_C.append(Output_Free['xStar'][0].copy())
        x2Vals_Free_C.append(Output_Free['xStar'][1].copy())
        fStarVals_Free_C.append(Output_Free['fStar'].copy())
        FuncEvalsVals_Free_C.append(Output_Free['FuncEvals'])

    # We compute statistical values for the gradient-based method.
    xStarMean_Grad_C = []
    xStarMean_Grad_C.append(float(np.mean(x1Vals_Grad_C)))
    xStarMean_Grad_C.append(float(np.mean(x2Vals_Grad_C)))
    xStarStdDev_Grad_C = []
    xStarStdDev_Grad_C.append(float(np.std(x1Vals_Grad_C)))
    xStarStdDev_Grad_C.append(float(np.std(x2Vals_Grad_C)))
    fStarMean_Grad_C = np.mean(fStarVals_Grad_C)
    fStarStdDev_Grad_C = np.std(fStarVals_Grad_C)
    FuncEvalsMean_Grad_C = np.mean(FuncEvalsVals_Grad_C)
    FuncEvalsStdDev_Grad_C = np.std(FuncEvalsVals_Grad_C)

    # We compute statistical values for the gradient-free method.
    xStarMean_Free_C = []
    xStarMean_Free_C.append(float(np.mean(x1Vals_Free_C)))
    xStarMean_Free_C.append(float(np.mean(x2Vals_Free_C)))
    xStarStdDev_Free_C = []
    xStarStdDev_Free_C.append(float(np.std(x1Vals_Free_C)))
    xStarStdDev_Free_C.append(float(np.std(x2Vals_Free_C)))
    fStarMean_Free_C = np.mean(fStarVals_Free_C)
    fStarStdDev_Free_C = np.std(fStarVals_Free_C)
    FuncEvalsMean_Free_C = np.mean(FuncEvalsVals_Free_C)
    FuncEvalsStdDev_Free_C = np.std(FuncEvalsVals_Free_C)

    # We print critical results to the terminal.
    print('\n')
    print('----------------------------------------------')
    print('Problem 6.2(c) - Step of ',str(StepMag))
    print('----------------------------------------------')
    print('\n')
    print('GRAD-BASED RESULTS...')
    print('=> Mean xStar',xStarMean_Grad_C)
    print('=> Std Dev xStar: ',xStarStdDev_Grad_C)
    print('=> Mean fStar: ',fStarMean_Grad_C)
    print('=> Std Dev fStar: ',fStarStdDev_Grad_C)
    print('=> Mean Func Evals: ',FuncEvalsMean_Grad_C)
    print('=> Std Dev Func Evals: ',FuncEvalsStdDev_Grad_C)
    print('\n')
    print('GRAD-FREE RESULTS...')
    print('=> Mean xStar',xStarMean_Free_C)
    print('=> Std Dev xStar: ',xStarStdDev_Free_C)
    print('=> Mean fStar: ',fStarMean_Free_C)
    print('=> Std Dev fStar: ',fStarStdDev_Free_C)
    print('=> Mean Func Evals: ',FuncEvalsMean_Free_C)
    print('=> Std Dev Func Evals: ',FuncEvalsStdDev_Free_C)
    print('\n')
    print('----------------------------------------------')
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# For various step sizes, we apply the gradient-free approach (n = 10) and a gradient-based
# approach (n = 10). For each step size, statistical values are derived for the gradient-free
# approach and printed to the terminal alongside comparable values for the gradient-based
# approach.
# ---------------------------------------------------------------------------------------------- #
# We define the statistical n-value.
n_D = 10

# We define the lower and upper bounds of the problem exploration.
LowerBounds_D = [-3,-3,3]
UpperBounds_D = [3,3,3]

# We define the Options for both optimizers.
Options_Grad_D = {
    'isReturnData':True
}
Options_Free_D = {
    'Lower Bound':LowerBounds_D,
    'Upper Bound':UpperBounds_D,
    'Maximum Iterations':10000,
    'Method':'PSO'
}

# We define storage containers for statistically-relevant values for the gradient-based approach.
x1Vals_Grad_D = []
x2Vals_Grad_D = []
fStarVals_Grad_D = []
FuncEvalsVals_Grad_D = []

# We define storage containers for statistically-relevant values for the gradient-free approach.
x1Vals_Free_D = []
x2Vals_Free_D = []
fStarVals_Free_D = []
FuncEvalsVals_Free_D = []

# We iterate through the sampling instances.
for Sample in range(n_D):

    # We generate a random initial guess for the gradient-based method.
    x1_Init = np.random.uniform(LowerBounds_D[0],UpperBounds_D[0])
    x2_Init = np.random.uniform(LowerBounds_D[1],UpperBounds_D[1])
    x3_Init = np.random.uniform(LowerBounds_D[2],UpperBounds_D[2])
    X0 = (x1_Init,x2_Init,x3_Init)

    # We run the gradient-based approach.
    PointStorage_Grad,fStar_Grad,FuncEvals_Grad,_ = UnconstrainedOptimizer(
        Func,
        X0,
        Options_Grad_D
    )

    # We store data for the gradient-based approach.
    x1Vals_Grad_D.append(PointStorage_Grad[-1][0])
    x2Vals_Grad_D.append(PointStorage_Grad[-1][1])
    fStarVals_Grad_D.append(fStar_Grad)
    FuncEvalsVals_Grad_D.append(FuncEvals_Grad)

    # We run the gradient-free approach.
    Output_Free = Optimize(
        Func,
        Options_Free_D
    )

    # We store data for the gradient-free approach.
    x1Vals_Free_D.append(Output_Free['xStar'][0].copy())
    x2Vals_Free_D.append(Output_Free['xStar'][1].copy())
    fStarVals_Free_D.append(Output_Free['fStar'].copy())
    FuncEvalsVals_Free_D.append(Output_Free['FuncEvals'])

# We compute statistical values for the gradient-based method.
xStarMean_Grad_D = []
xStarMean_Grad_D.append(float(np.mean(x1Vals_Grad_D)))
xStarMean_Grad_D.append(float(np.mean(x2Vals_Grad_D)))
xStarStdDev_Grad_D = []
xStarStdDev_Grad_D.append(float(np.std(x1Vals_Grad_D)))
xStarStdDev_Grad_D.append(float(np.std(x2Vals_Grad_D)))
fStarMean_Grad_D = np.mean(fStarVals_Grad_D)
fStarStdDev_Grad_D = np.std(fStarVals_Grad_D)
FuncEvalsMean_Grad_D = np.mean(FuncEvalsVals_Grad_D)
FuncEvalsStdDev_Grad_D = np.std(FuncEvalsVals_Grad_D)

# We compute statistical values for the gradient-free method.
xStarMean_Free_D = []
xStarMean_Free_D.append(float(np.mean(x1Vals_Free_D)))
xStarMean_Free_D.append(float(np.mean(x2Vals_Free_D)))
xStarStdDev_Free_D = []
xStarStdDev_Free_D.append(float(np.std(x1Vals_Free_D)))
xStarStdDev_Free_D.append(float(np.std(x2Vals_Free_D)))
fStarMean_Free_D = np.mean(fStarVals_Free_D)
fStarStdDev_Free_D = np.std(fStarVals_Free_D)
FuncEvalsMean_Free_D = np.mean(FuncEvalsVals_Free_D)
FuncEvalsStdDev_Free_D = np.std(FuncEvalsVals_Free_D)

# We print critical results to the terminal.
print('\n')
print('----------------------------------------------')
print('Problem 6.2(d)')
print('----------------------------------------------')
print('\n')
print('GRAD-BASED RESULTS...')
print('=> Mean xStar',xStarMean_Grad_D)
print('=> Std Dev xStar: ',xStarStdDev_Grad_D)
print('=> Mean fStar: ',fStarMean_Grad_D)
print('=> Std Dev fStar: ',fStarStdDev_Grad_D)
print('=> Mean Func Evals: ',FuncEvalsMean_Grad_D)
print('=> Std Dev Func Evals: ',FuncEvalsStdDev_Grad_D)
print('\n')
print('GRAD-FREE RESULTS...')
print('=> Mean xStar',xStarMean_Free_D)
print('=> Std Dev xStar: ',xStarStdDev_Free_D)
print('=> Mean fStar: ',fStarMean_Free_D)
print('=> Std Dev fStar: ',fStarStdDev_Free_D)
print('=> Mean Func Evals: ',FuncEvalsMean_Free_D)
print('=> Std Dev Func Evals: ',FuncEvalsStdDev_Free_D)
print('\n')
print('----------------------------------------------')
# ---------------------------------------------------------------------------------------------- #