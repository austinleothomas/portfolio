# ---------------------------------------------------------------------------------------------- #
# Master script for final project.
# U-M AEROSP 588 Fall '25.
# Austin Leo Thomas.
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We import modules as needed.
# ---------------------------------------------------------------------------------------------- #
import matlab.engine
import numpy as np
import math
from datetime import datetime
import sys,os
import time
from scipy.optimize import minimize
import nlopt
from scipy.optimize import direct
from scipy.optimize import differential_evolution
from pyswarm import pso
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define user-controlled booleans and variables to control program functionality.
# ---------------------------------------------------------------------------------------------- #
# We specify which optimization approach to use (select only one).
isRunNelderMead = False
isRunGPS = False
isRunDIRECT = False
isRunGA = False
isRunPSO = False
isRunCG = False
isRunBFGS = False
isRunLBFGS = False
isRunTrustRegion = False

# We specify if we are running MDO.
isRunMDO = False

# We define tunable parameters for various algorithms.
class TuningClass:
    def __init__(self):
        self.MaxEvals = 500     # maximum function evaluations
        self.MaxIters = 5       # maximum iterations
        self.PopSize = 14       # population / swarm size
        self.xTol = 1e-3        # abs. tolerance for change in x-values (grad-free methods)
        self.fTol = 1e-2        # abs. tolerance for change in f-values (grad-free methods)
        self.gaTol = 1e-6       # rel. tolerance (scipy.differential_evolution specifically)
        self.gradTol = 1e-8     # abs. convergence criteria (for grad-based methods)
Parameters = TuningClass()

# We specify a configuration summary and whether we want to display it.
Summary = 'Custom Work'
isDispSummary = True

# We specify if we want to record the start/stop time for the optimization run.
isRunStopWatch = False

# We specify if we want to display the method / parameters to the terminal.
isDispMethod = False
isDispMaxEvals = False
isDispMaxIters = False
isDispPopSize = False
isDispGradFreeTols = False
isDispGeneticTols = False
isDispGradTols = False

# We specify what outputs to print to the terminal.
isDispTime = False
isDispGains = False
isDispEvals = False
isDispIters = False
isDispMsg = False
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define the objective function / first model call function.
# ---------------------------------------------------------------------------------------------- #
def SimFunc(Gains,Grad = None):
    global isFirstCall
    TimeoutValue = 30 if isFirstCall else 5
    isFirstCall = False
    try:
        GainMatrix = matlab.double(list(Gains))
        print('Before Sim:',datetime.now())
        Sim = Eng.AutoPilot(GainMatrix,float(1),nargout = 4,background = True)
        TimeoutClock = time.time()
        while not Sim.done():
            if time.time() - TimeoutClock > TimeoutValue:
                print('Timed Out!')
                print('\n')
                return 100
            time.sleep(0.1)
        StopTime,_,_,_ = Sim.result()
        print('After Sim:',datetime.now())
        print('\n')
        return float(StopTime)
    except Exception as e:
        print('Simulation Failed @',datetime.now())
        print('Exception:',e)
        print('\n')
        return 100
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define the cost function / second model call function.
# ---------------------------------------------------------------------------------------------- #
def CostFunc(StopIndex,ControlHistory):
    ControlArray = np.asarray(ControlHistory)
    dAileron = ControlArray[:StopIndex,7]
    dRudder = ControlArray[:StopIndex,8]
    dElevator = ControlArray[:StopIndex,9]
    AileronCost = np.sum(np.abs(dAileron[1:] - dAileron[:-1]))
    RudderCost = np.sum(np.abs(dRudder[1:] - dRudder[:-1]))
    ElevatorCost = np.sum(np.abs(dElevator[1:] - dElevator[:-1]))
    ControlCost = AileronCost + RudderCost + ElevatorCost
    return float(ControlCost)
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define the Beta update function.
# ---------------------------------------------------------------------------------------------- #
def BetaUpdate(ControlCost):
    BaseCost = 6987.892650621739
    MinBeta = 0.5
    if ControlCost > BaseCost:
        Beta = 1 - (ControlCost - BaseCost) / BaseCost
        if Beta < MinBeta:
            Beta = MinBeta
    else:
        Beta = 1
    return Beta
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define the Gauss-Seidel coupled MDO solver.
# ---------------------------------------------------------------------------------------------- #
def GaussSeidel(Gains):

    # We define the count variable.
    global CountMDO

    # We define tunable parameters.
    BetaTol = 1e-3
    MaxIters = 15
    Beta = float(1)
    RelaxParam = 0.5

    # We execute until convergence.
    for i in range(MaxIters):
        CountMDO += 1
        StopTime,ControlArray,_,StopIndex = Eng.AutoPilot(
            Gains,
            Beta,
            nargout = 4,
            )
        StopIndex = int(np.asarray(StopIndex).squeeze())
        ControlCost = CostFunc(
            StopIndex,
            ControlArray
        )
        RawBeta = float(BetaUpdate(ControlCost))
        NewBeta = Beta + RelaxParam * (RawBeta - Beta)
        if abs(NewBeta - Beta) < BetaTol:
            Beta = NewBeta
            break
        Beta = NewBeta

    # We print the Beta-value.
    print('Beta = ',Beta)
    
    # We return critical values.
    return StopTime
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define the MDO objective function.
# ---------------------------------------------------------------------------------------------- #
def MDO(Gains):
    global isFirstCall
    TimeoutValue = 30 if isFirstCall else 5
    isFirstCall = False
    try:
        GainMatrix = matlab.double(list(Gains))
        Sim = Eng.AutoPilot(GainMatrix,float(1),nargout = 4,background = True)
        TimeoutClock = time.time()
        while not Sim.done():
            if time.time() - TimeoutClock > TimeoutValue:
                print('Timed Out!')
                print('\n')
                return 100
            time.sleep(0.1)
        StopTime = GaussSeidel(Gains)
        return float(StopTime)
    except Exception as e:
        print('Simulation Failed @',datetime.now())
        print('Exception:',e)
        print('\n')
        return 100
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We execute pre-optimization configuration.
# ---------------------------------------------------------------------------------------------- #
# We specify which functionto minimize.
if isRunMDO:
    ObjFunc = MDO
else:
    ObjFunc = SimFunc

# We configure the MATLAB engine.
Eng = matlab.engine.start_matlab()

# We define the initial gains.
x0 = np.array([1,1.1,1,39.6,6.46,1.03,-0.12])

# We define gain bounds for those that require it.
xBounds = [
    (1e-3,5),
    (1e-3,5.3),
    (1e-3,5),
    (1e-3,99),
    (1e-3,32.3),
    (1e-3,2.575),
    (-0.3,1e-3)
]
xLowerBounds,xUpperBounds = zip(*xBounds)

# We configure terminal outputs.
print('\n')
if isDispSummary:
    print(Summary)
    print('\n')

# We record the start time, if requested.
if isRunStopWatch:
    StartTime = datetime.now()

# We define the first call identifier.
isFirstCall = True

# We define the MDO function call counter.
global CountMDO
CountMDO = 0
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We execute the optimization procedure.
# ---------------------------------------------------------------------------------------------- #
# We configure the Nelder-Mead optimizer, via SciPy's 'minimize' module.
if isRunNelderMead:
    Method = 'Nelder-Mead'
    Result = minimize(
        ObjFunc,
        x0,
        method = 'Nelder-Mead',
        options = {
            'maxfev':Parameters.MaxEvals,
            'xatol':Parameters.xTol,
            'fatol':Parameters.fTol
        }
    )

# We configure the GPS optimizer, via NLopt.
if isRunGPS:
    Method = 'GPS'
    GPS = nlopt.opt(nlopt.GN_ISRES,7)
    GPS.set_lower_bounds(xLowerBounds)
    GPS.set_upper_bounds(xUpperBounds)
    GPS.set_min_objective(ObjFunc)
    GPS.set_maxeval(Parameters.MaxEvals)
    GPS.set_xtol_abs(Parameters.xTol)
    GPS.set_ftol_abs(Parameters.fTol)
    xStar = GPS.optimize(x0)
    fStar = GPS.last_optimum_value()
    Evals = GPS.get_numevals()
    Code = GPS.last_optimize_result()
    if Code == 2 or Code == 4:
        StopMsg = 'Optimization terminated successfully.'
    elif Code == 6:
        StopMsg = 'Maximum number of function evaluations has been reached.'
    else:
        StopMsg = 'Optimization failed. / Unknown termination cause.'

# We configure the DIRECT optimizer., via SciPy's 'direct' module.
if isRunDIRECT:
    Method = 'DIRECT'
    Result = direct(
        ObjFunc,
        xBounds,
        maxfun = Parameters.MaxEvals
    )

# We configure the GA, via SciPy's 'differential_evolution' module.
if isRunGA:
    Method = 'GA'
    Result = differential_evolution(
        ObjFunc,
        xBounds,
        maxiter = Parameters.MaxIters,
        popsize = Parameters.PopSize,
        tol = Parameters.gaTol
    )

# We configure the PSO algorithm, via PySwarm's 'pso' module.
if isRunPSO:
    Method = 'PSO'
    SavedSysConfig = sys.stdout
    sys.stdout = open(os.devnull,'w')
    xStar,fStar = pso(
        ObjFunc,
        xLowerBounds,
        xUpperBounds,
        swarmsize = Parameters.PopSize,
        maxiter = Parameters.MaxIters
    )
    Iters = Parameters.MaxIters
    Evals = (Iters + 1) * Parameters.PopSize
    StopMsg = 'Maximum number of iterations has been reached.'
    sys.stdout.close()
    sys.stdout = SavedSysConfig

# We configure the CG algorithm, via SciPy's 'minimize' module, with finite-difference
# gradient estimation.
if isRunCG:
    Method = 'CG'
    Result = minimize(
        ObjFunc,
        x0,
        method = 'CG',
        options = {
            'maxiter':Parameters.MaxIters,
            'gtol':Parameters.gradTol
        }
    )

# We configure the quasi-Newton BFGS algorithm, via SciPy's 'minimize' module, with finite-
# difference gradient estimation.
if isRunBFGS:
    Method = 'BFGS'
    Result = minimize(
        ObjFunc,
        x0,
        method = 'BFGS',
        options = {
            'maxiter':Parameters.MaxIters,
            'gtol':Parameters.gradTol
        }
    )

# We configure the quasi-Newton L-BFGS-B algorithm, via SciPy's 'minimize' module, with
# finite-difference gradient estimation.
if isRunLBFGS:
    Method = 'L-BFGS-B'
    Result = minimize(
        ObjFunc,
        x0,
        bounds = xBounds,
        method = 'L-BFGS-B',
        options = {
            'maxiter':Parameters.MaxIters,
            'gtol':Parameters.gradTol
        }
    )

# We configure the trust region algorithm, via SciPy's 'minimize' module, with finite-
# difference gradient estimation.
if isRunTrustRegion:
    Method = 'Trust Region'
    Result = minimize(
        ObjFunc,
        x0,
        bounds = xBounds,
        method = 'trust-constr',
        options = {
            'maxiter':Parameters.MaxIters,
            'gtol':Parameters.gradTol
        }
    )
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We execute post-optimization processing.
# ---------------------------------------------------------------------------------------------- #
# We extract results from a Result dict, if one exists.
try:
    Result
    xStar = Result.x
    fStar = Result.fun
    Evals = Result.nfev
    Iters = Result.nit
    StopMsg = Result.message
except:
    pass

# We record the stop time, if requested.
if isRunStopWatch:
    StopTime = datetime.now()
    RunTime = StopTime - StartTime
    print('Run Time:',str(RunTime).split('.')[0],' (' + \
        str(math.floor(RunTime.total_seconds())),'s)')
    print('\n')

# We print configuration information as needed.
if isDispMethod:
    print('Method:',Method)
    print('\n')
if isDispMaxEvals:
    print('Max Function Evals:',Parameters.MaxEvals)
    print('\n')
if isDispMaxIters:
    print('Max Iterations:',Parameters.MaxIters)
    print('\n')
if isDispPopSize:
    print('Population / Swarm Size:',Parameters.PopSize)
    print('\n')
if isDispGradFreeTols:
    print('Abs. x-Tolerance:',Parameters.xTol)
    print('\n')
    print('Abs. f-Tolerance:',Parameters.fTol)
    print('\n')
if isDispGeneticTols:
    print('Genetic Algorithm Tolerance:',Parameters.gaTol)
    print('\n')
if isDispGradTols:
    print('Abs. Gradient Tolerance:',Parameters.gradTol)
    print('\n')

# We print results as needed.
if isDispTime:
    print('Optimum Flight Time:',fStar,' s')
    print('\n')
if isDispGains:
    print('Optimum Gains:',xStar)
    print('\n')
if isDispEvals:
    if isRunMDO:
        print('Function Evals:',CountMDO)
        print('\n')
    else:
        print('Function Evals:',Evals)
        print('\n')
if isDispIters:
    try:
        print('Iterations:',Iters)
        print('\n')
    except:
        print('Iteration count not available.')
        print('\n')
if isDispMsg:
    print(StopMsg)
    print('\n')
# ---------------------------------------------------------------------------------------------- #