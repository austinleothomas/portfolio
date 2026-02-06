# Gradient-Free Optimization Package
# Authored By: Austin Leo Thomas
# ---------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------------------------------------------- #
# We import modules as needed.
# ---------------------------------------------------------------------------------------------- #
import numpy as np
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define the PSO algorithm.
# ---------------------------------------------------------------------------------------------- #
def PSO(Func,Options):

    # We unpack Options values.
    xLow = Options['Lower Bound']
    xHigh = Options['Upper Bound']
    Alpha = Options['Inertia Parameter']
    BetaMax = Options['Maximum Self Influence Parameter']
    GammaMax = Options['Maximum Social Influence Parameter']
    DeltaMax = Options['Maximum Step Size']
    IterLimit = Options['Maximum Iterations']
    ConvCrit = Options['Convergence Criteria']
    RelTol = Options['Convergence Relative Tolerance']

    # We initialize State values.
    State = {
        'Iter':0,
        'currX':np.zeros((10 * len(xLow),len(xLow))),
        'nextX':np.zeros((10 * len(xLow),len(xLow))),
        'currDelX':np.zeros((10 * len(xLow),len(xLow))),
        'nextDelX':np.zeros((10 * len(xLow),len(xLow))),
        'currFuncVals':np.zeros((10 * len(xLow),1)),
        'BestFuncVals':np.zeros((10 * len(xLow),1)),
        'BestLocalPoints':np.zeros((10 * len(xLow),len(xLow))),
        'IterWithoutImprovement':0,
        'FuncEvalCount':0,
        'prevBestSwarmVal':None
    }

    # We randomly initialize X and DelX values.
    for Point in range(State['currX'].shape[0]):
        for xVal in range(State['currX'].shape[1]):
            State['currX'][Point,xVal] = np.random.uniform(xLow[xVal],xHigh[xVal])
            State['currDelX'][Point,xVal] = np.random.uniform(-np.abs(DeltaMax),np.abs(DeltaMax))

    # We generate a point storage list.
    PointStorage = []
    
    # We run the optimization loop.
    while (State['IterWithoutImprovement'] < ConvCrit) and (State['Iter'] < IterLimit):

        # We define the best individual and global points.
        for Point in range(len(State['currFuncVals'])):

            # We update the current point's current function value.
            State['currFuncVals'][Point],_ = Func(State['currX'][Point,:])
            State['FuncEvalCount'] += 1

            # We check if the current point's current function value is its best value.
            if State['Iter'] == 0:
                State['BestFuncVals'][Point] = State['currFuncVals'][Point].copy()
                State['BestLocalPoints'][Point,:] = State['currX'][Point,:].copy()
            if State['currFuncVals'][Point] < State['BestFuncVals'][Point]:
                State['BestFuncVals'][Point] = State['currFuncVals'][Point].copy()
                State['BestLocalPoints'][Point,:] = State['currX'][Point,:].copy()

            # We check if the current point's current function value is the swarm's best value.
            if Point == 0:
                State['currBestSwarmVal'] = State['currFuncVals'][Point].copy()
                State['currBestSwarmPoint'] = State['currX'][Point,:].copy()
            if State['currFuncVals'][Point] < State['currBestSwarmVal']:
                State['currBestSwarmVal'] = State['currFuncVals'][Point].copy()
                State['currBestSwarmPoint'] = State['currX'][Point,:].copy()

        # We create an empty array to store each new point.
        TempPointStorage = []
        
        # We generate new points.
        for Point in range(len(State['currFuncVals'])):

            # We stochastically generate Beta and Gamma values.
            Beta = np.random.uniform(0,BetaMax)
            Gamma = np.random.uniform(0,GammaMax)

            # We pull values from State.
            currDelX = State['currDelX'][Point,:].copy()
            currBestLocalPoint = State['BestLocalPoints'][Point,:].copy()
            currBestSwarmPoint = State['currBestSwarmPoint'].copy()
            currX = State['currX'][Point,:].copy()

            # We define empty arrays for the update values.
            nextDelX = np.zeros((len(xLow)))
            nextX = np.zeros((len(xLow)))

            # We add the currX to PointStorage.
            TempPointStorage.append(currX)
            # PointStorage.append(State['currX'].copy())

            # We iterate through each design variable for the update.
            for xVal in range(len(nextDelX)):

                # We define the change in each design variable.
                nextDelX[xVal] = Alpha * currDelX[xVal] + \
                    Beta * (currBestLocalPoint[xVal] - currX[xVal]) + \
                        Gamma * (currBestSwarmPoint[xVal] - currX[xVal])
                
                # We ensure this change is within the maximum allowable range.
                nextDelX[xVal] = max(min(nextDelX[xVal],DeltaMax),-DeltaMax)

                # We add this change to the current design variable value.
                nextX[xVal] = currX[xVal] + nextDelX[xVal]

                # We ensure this value is within the acceptable range of design variables.
                nextX[xVal] = max(min(nextX[xVal],xHigh[xVal]),xLow[xVal])

            # We update the State dict.
            State['nextDelX'][Point,:] = nextDelX
            State['nextX'][Point,:] = nextX

        # We add the current array of points to PointStorage.
        PointStorage.append(TempPointStorage.copy())

        # We check if the current best swarm value matches the previous best swarm value.
        if State['Iter'] != 0 and np.isclose(State['currBestSwarmVal'],State['prevBestSwarmVal'],
                                             rtol = RelTol):
            State['IterWithoutImprovement'] += 1
        else:
            State['IterWithoutImprovement'] = 0

        # We update State values.
        State['currX'] = State['nextX'].copy()
        State['currDelX'] = State['nextDelX'].copy()
        State['prevBestSwarmVal'] = State['currBestSwarmVal'].copy()
        State['Iter'] += 1

        # We check if the number of function calls has grown excessive.
        if State['FuncEvalCount'] >= 20000000000:
            break

    # We compile the Output dict.
    Output = {
        'xStar':State['currBestSwarmPoint'],
        'fStar':State['currBestSwarmVal'],
        'Iter':State['Iter'],
        'FuncEvals':State['FuncEvalCount'],
        'PointStorage':PointStorage
    }

    # We return the Output dict.
    return Output
# ---------------------------------------------------------------------------------------------- #
            


# ---------------------------------------------------------------------------------------------- #
# We write the dispatch function.
# ---------------------------------------------------------------------------------------------- #
def GradFreeOptimizer(Func,Options):

    # We define the default Options values.
    DefaultOptions = {
        'Method':'PSO',
        'Inertia Parameter':1,
        'Maximum Self Influence Parameter':2,
        'Maximum Social Influence Parameter':2,
        'Maximum Step Size':((np.min(Options['Upper Bound']) - np.min(Options['Lower Bound'])) / 100),
        'Maximum Iterations':50000,
        'Convergence Criteria':3,
        'Convergence Relative Tolerance':1e-5
    }

    # We configure Options based on default values.
    for Key,Value in DefaultOptions.items():
        if Key not in Options:
            Options[Key] = Value

    # We dispatch the appropriate optimizer.
    if Options['Method'] == 'PSO':
        return PSO(Func,Options)
# ---------------------------------------------------------------------------------------------- #