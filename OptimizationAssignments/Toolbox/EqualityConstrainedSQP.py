# This script comprises a function to implement an equality-constrained SQP method.
# --------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------#
# We import modules as needed.
# --------------------------------------------------------------------------------------------#
import numpy as np
from UnconstrainedOptimizer import BackTrack as LineSearch
# --------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------#
# We define a function for computing a damped BFGS update.
# --------------------------------------------------------------------------------------------#
def DampedBFGS(State):

    # We unpack necessary values from the State dict.
    H = State['prevApproxHessian']
    S = State['prevS']
    Y = State['prevY']

    # We define Theta.
    if np.dot(S.T,Y) >= 0.2 * np.dot(S.T,np.dot(H,S)):
        Theta = 1
    else:
        Theta = (0.8 * np.dot(S.T,np.dot(H,S))) / (np.dot(S.T,np.dot(H,S)) - np.dot(S.T,Y))

    # We define R.
    R = Theta * Y + (1 - Theta) * (H @ S)

    # We define the new Hessian.
    if (R @ S) > 0:
        newHessian = H - (H @ S[:,None] @ S[None,:] @ H) / float(S @ H @ S) \
                        + (R[:,None] @ R[None,:]) / float(R @ S)
    else:
        newHessian = np.eye(len(State['currX']))

    # We return the new Hessian.
    return newHessian
# --------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------#
# We define a function for solving the QP subproblem.
# --------------------------------------------------------------------------------------------#
def QP(State):
    
    # We unpack necessary values from the State dict.
    Hessian = State['currApproxHessian']
    Jacobian = State['currJacH']
    DelL = State['currDelL']
    H = State['currH']

    # We define the Hessian size.
    n = Hessian.shape[0]

    if Jacobian.ndim == 1:
        m = 1
    else:
        m = Jacobian.shape[0]
    
    # We generate useful versions of the Jacobian to generate the KKT matrix.
    if Jacobian.ndim == 1:
        UpperRight = Jacobian.reshape(-1,1)
        LowerLeft = Jacobian.reshape(1,-1)
    else:
        UpperRight = Jacobian.T
        LowerLeft = Jacobian

    # We construct the KKT matrix.
    TopRow = np.hstack((Hessian,UpperRight))
    BottomRow = np.hstack((LowerLeft,np.zeros((m,m))))
    KKT = np.vstack((TopRow,BottomRow))

    # We construct the RHS vector.
    if Jacobian.ndim == 1:
        RHS = np.hstack((np.ravel(-DelL),np.ravel(-H)))
        RHS = np.ravel(RHS)
    else:
        RHS = np.hstack((-np.asarray(DelL[0]).flatten(),-np.asarray(H).flatten()))

    # We solve the linear system.
    Solution = np.linalg.solve(KKT,RHS)

    # We process results.
    pX = Solution[:n]
    pLambda = Solution[n:]

    # We return results.
    return pX,pLambda
# --------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------#
# We define a function to generate a merit function.
# --------------------------------------------------------------------------------------------#
def GenerateMeritFunc(Func,Cons,Mu):
    def MeritFunc(X):
        F,DelF = Func(X)
        H,DelH = Cons(X)
        H = np.asarray(H).flatten()
        normH = np.linalg.norm(np.atleast_1d(H),ord = 2)
        MeritFuncVal = F + Mu * normH
        DelMeritFunc = np.zeros(np.size(X))
        for i in range(len(DelMeritFunc)):
            if normH == 0:
                DelMeritFunc[i] = DelF[i]
            elif DelH.ndim == 1:
                DelMeritFunc[i] = DelF[i] + Mu * H * DelH[i] / normH
            else:
                DelMeritFunc[i] = DelF[i] + Mu * np.dot(H,DelH[:,i]) / normH
        return MeritFuncVal,DelMeritFunc
    return MeritFunc
# --------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------#
# We define the primary function.
# --------------------------------------------------------------------------------------------#
def EqualityConstrainedSQP(Func,Cons,x0,Options):

    # We define the default Options values.
    DefaultOptions = {
        'TauOptimality':1e-6,
        'TauFeasibility':1e-6,
        'AlphaInit':1,
        'Mu':10,
        'Mu1':10e-4,
        'Mu2':0.4,
        'Rho':0.5
    }

    # We configure Options based on default values.
    if Options is None:
        Options = DefaultOptions.copy()
    else:
        for key,value in DefaultOptions.items():
            if key not in Options:
                Options[key] = value
    
    # We define necessary values given by Options.
    TauOptimality = Options['TauOptimality']
    TauFeasibility = Options['TauFeasibility']

    # We define the State dict.
    State = {}

    # We compute Iter 0 State values.
    State['FunctionCalls'] = 0
    State['currX'] = x0
    State['currLambda'] = 0
    State['currF'],State['currDelF'] = Func(State['currX'])
    State['currH'],State['currJacH'] = Cons(State['currX'])
    State['FunctionCalls'] += 1
    State['currDelL'] = State['currDelF'] + State['currLambda'] * State['currJacH']

    # We define values necessary for the optimization loop.
    PointStorage = [x0]
    OptConditionStorage = [np.max(np.abs(State['currDelF']))]
    Iter = 0

    # We define the merit function for the line search.
    MeritFunc = GenerateMeritFunc(Func,Cons,Options['Mu'])

    # We define the optimization loop.
    while ((np.max(np.abs(State['currDelL'])) > TauOptimality) or 
           (np.max(np.abs(State['currH'])) > TauFeasibility)) and Iter < 2000:
        
        # we define the approximate Lagrangian Hessian.
        if not Iter % 10:
            State['currApproxHessian'] = np.eye(len(State['currX']))
        else:
            State['currApproxHessian'] = DampedBFGS(State)

        # We perform quadratic programming and line search.
        State['currVect'],pLambda = QP(State)
        Alpha,State = LineSearch(MeritFunc,State,Options)

        # We compute next-iteration values.
        nextLambda = State['currLambda'] + pLambda
        nextX = State['currX'] + Alpha * State['currVect']
        nextF,nextDelF = Func(nextX)
        nextH,nextJacH = Cons(nextX)
        State['FunctionCalls'] += 1
        nextDelL = nextDelF + nextJacH.T * nextLambda

        # We compute and configure current-iteration s- and y-values.
        currS = nextX - State['currX']
        currY = nextDelL - (State['currDelF'] + State['currJacH'].T * nextLambda)
        currS = np.asarray(currS).reshape(-1)
        currY = np.asarray(currY).reshape(-1)

        # We update storage lists.
        PointStorage.append(np.copy(nextX))
        OptConditionStorage.append(np.max(np.abs(nextDelF)))

        # We update State values to reflect the next iteration.
        State.update({
            'currX':nextX,
            'currLambda':nextLambda,
            'currF':nextF,
            'currDelF':nextDelF,
            'currH':nextH,
            'currJacH':nextJacH,
            'currDelL':nextDelL,
            'prevS':currS,
            'prevY':currY,
            'prevApproxHessian':State['currApproxHessian']
        })

        # We update Iter.
        Iter += 1
    
    # We compute final values.
    xStar = State['currX']
    fStar,_ = Func(xStar)
    hStar,_ = Cons(xStar)

    # We update the output dict.
    Output = {
        'xStar':xStar,
        'fStar':fStar,
        'hStar':hStar,
        'Iterations':Iter,
        'FunctionCalls':State['FunctionCalls'],
        'PointStorage':PointStorage,
        'OptConditionStorage':OptConditionStorage
        }

    # We return the output dict.
    return Output
# --------------------------------------------------------------------------------------------#