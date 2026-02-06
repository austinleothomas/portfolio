# Unconstrained optimizer function for use in AEROSP 588 by Austin Leo Thomas.
#
# Inputs...
#   Func:       handle to a function of the form f,g = func(x), where f is the function value, g is a
#               numpy array containing the gradient functions, and x are the design variables
#               [function handle]
#   x0:         starting point [ndarray]
#   Tau:        convergence tolerance [float]
#   Options:    a dictionary containing options; autograder will leave this blank [dict]
#
# Outputs...
#   xStar:      optimal design variables [ndarray]
#   fStar:      optimal function value [float]
#   Output:     dictionary containing options, including at the minimum the alias [dict]
#
# ---------------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------------- #
# We import required modules.
# ---------------------------------------------------------------------------------------------------- #
import numpy as np
# ---------------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------------- #
# We define line search methods.
# ---------------------------------------------------------------------------------------------------- #
# We define a line search algorithm to satisfy backtracking conditions.
def BackTrack(Func,State,Options):

    # We unpack the relevant inputs.
    currX = State['currX']
    currVect = State['currVect']
    AlphaInit = Options['AlphaInit']
    Mu1 = Options['Mu1']
    Rho = Options['Rho']

    # We define a function to evaluate Phi and PhiPrime for a given Alpha.
    def Phi(Alpha):
        Phi,PhiPrime = Func(currX + Alpha*currVect)
        PhiPrime = np.dot(PhiPrime.T,currVect)
        State['FunctionCalls'] +=1
        return Phi,PhiPrime

    # We define necessary values for the backtracking loop.
    Alpha = AlphaInit
    PhiAlpha,_ = Phi(Alpha)
    Phi0,PhiPrime0 = Phi(0)

    # We define the brakceting loop.
    while PhiAlpha > Phi0 + Mu1 * Alpha * PhiPrime0:
        Alpha = Rho * Alpha
        PhiAlpha,_ = Phi(Alpha)

    # We return the result
    return Alpha,State

# We define a line search algorithm to satisfy the strong Wolfe conditions.
def StrongWolfe(Func,State,Options):

    # We unpack the relevant inputs.
    currX = State['currX']
    currVect = State['currVect']
    AlphaInit = Options['AlphaInit']
    Mu1 = Options['Mu1']
    Mu2 = Options['Mu2']
    Sigma = Options['Sigma']

    # We define a function to evaluate Phi and PhiPrime for a given Alpha.
    def Phi(Alpha):
        Phi,PhiPrime = Func(currX + Alpha*currVect)
        PhiPrime = np.dot(PhiPrime.T,currVect)
        State['FunctionCalls'] += 1
        return Phi,PhiPrime

    # We define necessary values for the bracketing loop.
    Alpha1 = 0
    Alpha2 = AlphaInit
    Phi0,PhiPrime0 = Phi(0)
    Phi1 = Phi0
    isBracketing = True
    isFirstAttempt = True
    needPinpointing = True
    BracketingKillSwitch = 0

    # We define the bracketing loop.
    while isBracketing and BracketingKillSwitch < 100:

        Phi2,PhiPrime2 = Phi(Alpha2)

        if (Phi2 > Phi0 + Mu1 * Alpha2 * PhiPrime0) or (not isFirstAttempt and Phi2 > Phi1):
            AlphaLow = Alpha1
            AlphaHigh = Alpha2
            isBracketing = False
        if (np.abs(PhiPrime2) <= - Mu2 * PhiPrime0) and isBracketing:
            AlphaStar = Alpha2
            isBracketing = False
            needPinpointing = False
        elif (PhiPrime2 >= 0) and isBracketing:
            AlphaLow = Alpha2
            AlphaHigh = Alpha1
            isBracketing = False
        elif isBracketing:
            Alpha1 = Alpha2
            Alpha2 = Sigma * Alpha2
        if isFirstAttempt:
            isFirstAttempt = False
        BracketingKillSwitch += 1
        
    # We define necessary values for the pinpointing loop.
    PinpointingKillSwitch = 0

    # We define the pinpointing loop.
    while needPinpointing and PinpointingKillSwitch < 100:

        AlphaP = (AlphaLow + AlphaHigh) / 2
        PhiP,PhiPrimeP = Phi(AlphaP)
        PhiLow,_ = Phi(AlphaLow)

        if (PhiP > Phi0 + Mu1 * AlphaP * PhiPrime0) or (PhiP > PhiLow):
            AlphaHigh = AlphaP
        else:
            if np.abs(PhiPrimeP) <= - Mu2 * PhiPrime0:
                AlphaStar = AlphaP
                needPinpointing = False
            elif PhiPrimeP * (AlphaHigh - AlphaLow) >= 0:
                AlphaHigh = AlphaLow
            AlphaLow = AlphaP
        PinpointingKillSwitch += 1
        
    # We print an error message if the pinpointing kill switch is hit.
    if PinpointingKillSwitch >= 100:
        AlphaStar = AlphaP
        
    # We return AlphaStar.
    return AlphaStar,State
# ---------------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------------- #
# We define search direction determination methods.
# ---------------------------------------------------------------------------------------------------- #
# We define a function to generate the search direction based on the speepest descent method.
def SteepestDescent(Func,State):

    # We unpack the relevant inputs.
    currX = State['currX']

    # We define necessary values.
    _,DelF = Func(currX)
    State['FunctionCalls'] += 1

    # We define the search direction.
    State['currVect'] = -DelF / np.linalg.norm(DelF)

    # We return the search direction vector.
    return State
    
# We define a function to generate the search direction based on the conjugate gradient method.
def ConjugateGradient(Func,State):

    # We unpack the relevant inputs.
    currX = State['currX']
    prevX = State['prevX']
    prevVect = State['prevVect']
    ResetVal = State['ResetVal']

    # We define necessary values.
    _,currDelF = Func(currX)
    _,prevDelF = Func(prevX)
    State['FunctionCalls'] += 2

    # We determine the search direction according to the Fletcher-Reeves formula.
    if ResetVal >= 0.1 or State['iter'] == 0:
        currVect = -currDelF / np.linalg.norm(currDelF)
    else:
        Beta = np.dot(currDelF.T,currDelF) / np.dot(prevDelF.T,prevDelF)
        currVect = -currDelF / np.linalg.norm(currDelF) + Beta * prevVect
        
    # We update the state.
    State['currVect'] = currVect
    State['ResetVal'] = np.abs(np.dot(currDelF.T,prevDelF)) / np.abs(np.dot(currDelF.T,currDelF))

    # We return the search direction vector.
    return State
# ---------------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------------- #
# We define the main function.
# ---------------------------------------------------------------------------------------------------- #
def UnconstrainedOptimizer(Func,x0,Options):

    # We define the output dict object.
    Output = {}

    # We define the default Options values.
    DefaultOptions = {
        'LineSearchMethod':'Strong Wolfe',
        'DirectionSearchMethod':'Conjugate Gradient',
        'Tau':1e-6,
        'AlphaInit':1,
        'Mu1':10e-4,
        'Mu2':0.4,
        'Sigma':2,
        'Rho':0.5,
        'isReturnData':False
    }

    # We configure Options based on default values.
    if Options is None:
        Options = DefaultOptions.copy()
    else:
        for key,value in DefaultOptions.items():
            if key not in Options:
                Options[key] = value

    # We define necessary values given by Options.
    LineSearchStyle = Options['LineSearchMethod']
    DirectionSearchStyle = Options['DirectionSearchMethod']
    isReturnData = Options['isReturnData']
    Tau = Options['Tau']
    
    # We define which line search algorithm we will use.
    def DoLineSearch(LineSearchStyle,Func,State,Options):
        if LineSearchStyle == 'Strong Wolfe':
            return StrongWolfe(Func,State,Options)
        elif LineSearchStyle == 'Backtracking':
            return BackTrack(Func,State,Options)
        else:
            print('Error! Invalid line search method.')
    
    # We define which search direction determination algorithm we will use.
    def GetSearchDirection(DirectionSearchStyle,Func,State):
        if DirectionSearchStyle == 'Conjugate Gradient':
            return ConjugateGradient(Func,State)
        elif DirectionSearchStyle == 'Steepest Descent':
            return SteepestDescent(Func,State)
        else:
            print('Error! Invalid search direction determination method.')
    
    # We define necessary values for the optimization loop.
    State = {
        'FunctionCalls':0,
        'ResetVal':1
    }
    _,State['currDelF'] = Func(x0)
    State['prevVect'] = 0
    PointStorage = [x0]
    OptConditionStorage = []
    Iter = 0

    # We define the optimization loop.
    while (np.max(np.abs(State['currDelF'])) >= Tau) and Iter < 2000:

        # We record the optimality condition value.
        OptConditionStorage.append(np.max(np.abs(State['currDelF'])))

        # We update state values.
        State['currX'] = PointStorage[Iter]
        State['iter'] = Iter
        State['prevX'] = PointStorage[Iter - 1]

        # We obtain a search direction vector.
        State = GetSearchDirection(DirectionSearchStyle,Func,State)

        # We perform a line search.
        AlphaStar,State = DoLineSearch(LineSearchStyle,Func,State,Options)

        # We define the new X-value.
        newX = PointStorage[Iter] + AlphaStar * State['currVect']

        # We update state values.
        _,State['currDelF'] = Func(newX)
        State['prevVect'] = State['currVect']

        # We record the new X-value.
        PointStorage.append(np.copy(newX))

        # We update the iteration counter.
        Iter += 1

    # We record the final optimality condition, which is < Tau.
    OptConditionStorage.append(np.max(np.abs(State['currDelF'])))

    # We define the output variables.
    xStar = PointStorage[-1]
    fStar,_ = Func(xStar)
    State['FunctionCalls'] += 1
    FunctionCalls = State['FunctionCalls']

    # We return the output values.
    if isReturnData:
        return PointStorage,fStar,FunctionCalls,OptConditionStorage
    else:
        return xStar,fStar,Output
# ---------------------------------------------------------------------------------------------------- #