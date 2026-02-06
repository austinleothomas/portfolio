# FEA solver for the ten-truss problem defined in Appendix D.2.2 of Engineering Design Optimization.
# For use in solving Problem 5.3 of Assignment 5 for U-M Fall 2025 AEROSP 588.
#
# Authored By: Dr. Martins
# Modified By: Austin Leo Thomas
# ------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------------- #
# We import modules as needed.
import numpy as np
from math import sin,cos
# ------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------------- #
# We define the function for the bar FEA computations. All values in SI units. We have...
#
# Inputs...
#     E: Young's modulus [float]
#     A: cross-sectional area [float]
#     L: bar length [float]
#   Phi: bar orientation in radians [float]
#
# Outputs...
#   K: element stiffness matrix [4 x 4 ndarray]
#   S: element stress matrix [1 x 4 ndarray]
# ------------------------------------------------------------------------------------------------- #
def BarSolver(E,A,L,Phi):

    # We define shortcuts for sine and cosine.
    s = sin(Phi)
    c = cos(Phi)

    # We define the element stiffness matrix.
    k0 = np.array([[c**2,c * s],[c * s,s**2]])
    k1 = np.hstack([k0,-k0])
    K = E * A / L * np.vstack([k1,-k1])

    # We define the element stress matrix.
    S = E / L * np.array([[-c,-s,c,s]])

    # We return the function outputs.
    return K,S
# ------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------------- #
# We define a function to generate global indices given node numbers and the DOF per node.
#
# Inputs...
#   Node: nodal coordinate(s) of interest in the form [float or list]
#    DOF: degrees of freedom of the problem [float]
#
# Outputs...
#   GlobalIndices: indices of the bar of interest in the global matrix [ndarray of length 2]
# ------------------------------------------------------------------------------------------------- #
def GetGlobalIndices(Node,DOF):

    # We generate the empty ndarray for the GlobalIndices output.
    GlobalIndices = np.array([],dtype = int)

    # We compute the appropriate global index for each nodal index.
    for i in range(len(Node)):
        n = Node[i]
        Start = DOF * (n - 1)
        Finish = DOF * n
        GlobalIndices = np.concatenate((GlobalIndices, np.arange(Start,Finish,dtype = int)))

    # We return the result.
    return GlobalIndices
# ------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------------- #
# We define the function for the truss FEA computations. All values in SI units. We have...
#
# Inputs...
#    FirstNodes: indices of the first nodes for each bar [ndarray of length n(bars)]
#   SecondNodes: indices of the second nodes for each bar [ndarray of length n(bars)]
#           Phi: orientation of each bar in radians [ndarray of length n(bars)]
#             A: cross-sectional area of each bar [ndarray of length n(bars)]
#    BarLengths: length of each bar [ndarray of length n(bars)]
#             E: Young's modulus of each bar [ndarray of length n(bars)]
#           Rho: density of each bar [ndarray of length n(bars)]
#            Fx: external force on each node in the x-direction [ndarray of length n(nodes)]
#            Fy: external force on each node in the y-direction [ndarray of length n(nodes)]
#            BC: boolean values for if a node is fixed (True = fixed) [list of length n(nodes)]
#
# Outputs...
#     Mass: mass of the entire structure [float]
#   Stress: stress in each bar [ndarray of length n(bar)]
#
# ------------------------------------------------------------------------------------------------- #
def TrussSolver(FirstNodes,SecondNodes,Phi,A,BarLengths,E,Rho,Fx,Fy,BC):

    # We define the degrees of freedom of the problem
    DOF = 2

    # We pull problem size values from the inputs.
    nNodes = len(Fx)
    nBars = len(A)

    # We define the mass of the structure.
    Mass = np.sum(Rho * A * BarLengths)

    # We define the empty stiffness and stress global matrices, K and S respectively.
    K = np.zeros((DOF * nNodes,DOF * nNodes),dtype = np.result_type(A[0]))
    S = np.zeros((nBars,DOF * nNodes),dtype = np.result_type(A[0]))

    # We populate the stiffness and stress global matrices.
    for i in range(nBars):

        # We compute submatrices for each element.
        SubK,SubS = BarSolver(E[i],A[i],BarLengths[i],Phi[i])

        # We insert these submatrices into the global matrices.
        iGlobal = GetGlobalIndices([FirstNodes[i],SecondNodes[i]],DOF)
        K[np.ix_(iGlobal,iGlobal)] += SubK
        S[i,iGlobal] = SubS

    # We define an empty array of applied loads.
    F = np.zeros((nNodes * DOF,1))

    # We populate the empty array of applied loads.
    for i in range(nNodes):
        iGlobal = GetGlobalIndices([i + 1], DOF)
        F[iGlobal[0]] = Fx[i]
        F[iGlobal[1]] = Fy[i]

    # We eliminate rows / columns in the FEA system.
    iGlobal = np.squeeze(np.where(BC))
    iRemove = GetGlobalIndices(iGlobal + 1,DOF)

    K = np.delete(K,iRemove,axis = 0)
    K = np.delete(K,iRemove,axis = 1)
    F = np.delete(F,iRemove,axis = 0)
    S = np.delete(S,iRemove,axis = 1)

    # We solve the FEA system.
    U = np.linalg.solve(K,F)

    # We compute the stress vector.
    Stress = np.dot(S,U).reshape(nBars)

    # We configure the output dict.
    Solution = {
        'Mass':Mass,
        'Stress':Stress
    }

    return Solution
# ------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------------- #
# We define the function for the FEA procedure. We have...
#
# Inputs...
#             A: cross-sectional area of all the bars [ndarray of length 10]
#    GradMethod: gradient type specification (optional, nominally 'FD') [string]
#                   'FD' = finite difference
#                   'CS' = complex step
#                   'DT' = direct method
#                   'AJ' = adjoint method
#                   'AD' = automatic differentiaion (extra credit)
#   isAggregate: aggregation determination (optional, nominally False) [boolean]
#                   If True, function returns the KS-aggregated stress constraint. If False,
#                   the function does not aggregate and returns all stress values. Implementation
#                   of the True case is optional (extra credit).
#
# Outputs...
#     Mass: mass of the entire structure [float]
#   Stress: if Aggregate == False, stress of each bar [ndarray of length 10]
#           if Aggregate == True, KS-aggregated stress value [float]
#     dMdA: derivative of Mass with respect to each A [ndarray of length 10]
#     dSdA: if Aggregate == False, dSdA[i,j] is the derivative of Stress[i] with respect to A[j]
#               [10 x 10 ndarray]
#           if Aggregate == True, dSdA[j] is the derivative of the KS-aggregated stress with
#               respect to A[j]
#
# Indexing of Nodes...
#
# wall > 1 ---------- 2 ---------- 3
#          ++      ++ | ++      ++ |
#            ++  ++   |   ++  ++   |
#              ++     |     ++     |
#            ++  ++   |   ++  ++   |
#          ++      ++ | ++      ++ |
# wall > 4 ---------- 5 ---------- 6
#
# ---------------------------------------------------------------------------------------------- #
def TenBarTrussFEA(A,Options):

    # We define the default Options values.
    DefaultOptions = {
        'GradMethod':'FD',
        'isAggregate':False,
        'hFD':5e-6,
        'hCS':1e-200
    }

    # We configure Options based on default values.
    if Options is None:
        Options = DefaultOptions.copy()
    else:
        for key,value in DefaultOptions.items():
            if key not in Options:
                Options[key] = value

    # We define the nodes of each bar by [node1,node2].
    NodalDef = [
        [1,2],
        [2,3],
        [4,5],
        [5,6],
        [2,5],
        [3,6],
        [1,5],
        [2,4],
        [2,6],
        [3,5]
    ]

    # We define arrays of the 1st and 2nd nodes of each bar.
    FirstNodes = []
    SecondNodes = []
    for bar in NodalDef:
        FirstNodes.append(bar[0])
        SecondNodes.append(bar[1])

    # We define an array of bar orientations.
    Phi = np.deg2rad(np.array([0,0,0,0,-90,-90,-45,-135,-45,-135]))

    # We define an array of bar lengths.
    L = 10
    Diag = L * np.sqrt(2)
    BarLengths  = np.array([L,L,L,L,L,L,Diag,Diag,Diag,Diag])
    
    # We define an array of bar Young's moduli.
    E = np.ones(10) * 70 * 10**9
    
    # We define an array of bar densities.
    Rho = np.ones(10) * 2720
    
    # We define arrays of the external loads on each node.
    P = 5 * 10**5
    Fx = np.zeros(6)
    Fy = np.array([0,0,0,0,-P,-P])
    
    # boundary condition (set True for clamped nodes)
    # We define boundary conditions for each node (True indicates the node is fixed absolutely).
    BC = [True,False,False,True,False,False]

    # We call on the TrussSolver function to compute the mass and stress of the structure.
    TrussSolution = TrussSolver(FirstNodes,SecondNodes,Phi,A,BarLengths,E,Rho,Fx,Fy,BC)

    # We construct empty numpy arrays for our derivatives.
    dMdA = np.zeros(len(A),dtype = np.float64)
    dSdA = np.zeros((len(A),len(A)),dtype = np.float64)

    # We compute derivatives depending on the method directed in Options.
    if Options['GradMethod'] == 'FD':
        h = Options['hFD']
        for j in range(len(A)):
            A_pos = np.array(A,dtype = np.float64)
            A_neg = np.array(A,dtype = np.float64)
            A_pos[j] += h
            A_neg[j] -= h
            Sol_pos = TrussSolver(FirstNodes,SecondNodes,Phi,A_pos,BarLengths,E,Rho,Fx,Fy,BC)
            Sol_neg = TrussSolver(FirstNodes,SecondNodes,Phi,A_neg,BarLengths,E,Rho,Fx,Fy,BC)
            dMdA[j] = (Sol_pos['Mass'] - Sol_neg['Mass']) / (2 * h)
            dSdA[:,j] = (Sol_pos['Stress'] - Sol_neg['Stress']) / (2 * h)
    elif Options['GradMethod'] == 'CS':
        h = Options['hCS']
        for j in range(len(A)):
            A_cs = np.array(A,dtype = np.complex128)
            A_cs[j] += 1j * h
            Sol_cs = TrussSolver(FirstNodes,SecondNodes,Phi,A_cs,BarLengths,E,Rho,Fx,Fy,BC)
            dMdA[j] = np.imag(Sol_cs['Mass']) / h
            dSdA[:,j] = np.imag(Sol_cs['Stress']) / h
    elif Options['GradMethod'] == 'DT':
        U0 = None
        DOF = 2
        nNodes = len(Fx)
        nBars = len(A)
        K = np.zeros((DOF * nNodes,DOF * nNodes))
        S = np.zeros((nBars,DOF * nNodes))
        for i in range(nBars):
            SubK,SubS = BarSolver(E[i],A[i],BarLengths[i],Phi[i])
            iGlobal = GetGlobalIndices([FirstNodes[i],SecondNodes[i]],DOF)
            K[np.ix_(iGlobal,iGlobal)] += SubK
            S[i,iGlobal] = SubS
        iGlobal = np.squeeze(np.where(BC))
        iRemove = GetGlobalIndices(iGlobal + 1,DOF)
        K_red = np.delete(K,iRemove,axis = 0)
        K_red = np.delete(K_red,iRemove,axis = 1)
        F_red = np.zeros((nNodes * DOF,1))
        for i in range(nNodes):
            iGlobal = GetGlobalIndices([i + 1],DOF)
            F_red[iGlobal[0]] = Fx[i]
            F_red[iGlobal[1]] = Fy[i]
        F_red = np.delete(F_red,iRemove,axis = 0)
        S_red = np.delete(S,iRemove,axis = 1)
        U0 = np.linalg.solve(K_red,F_red)
        dMdA = Rho * BarLengths
        for j in range(nBars):
            dKdAj = np.zeros_like(K)
            SubK,SubS = BarSolver(E[j],1.0,BarLengths[j],Phi[j])
            iGlobal = GetGlobalIndices([FirstNodes[j],SecondNodes[j]],DOF)
            dKdAj[np.ix_(iGlobal,iGlobal)] += SubK
            dKdAj_red = np.delete(dKdAj,iRemove,axis = 0)
            dKdAj_red = np.delete(dKdAj_red,iRemove,axis = 1)
            dUdAj = np.linalg.solve(K_red,-np.dot(dKdAj_red,U0))
            for i in range(nBars):
                dSdA[i,j] = np.dot(S_red[i,:],dUdAj).real
    elif Options['GradMethod'] == 'AJ':
        DOF = 2
        nNodes = len(Fx)
        nBars = len(A)
        K = np.zeros((DOF * nNodes,DOF * nNodes))
        S = np.zeros((nBars,DOF * nNodes))
        for i in range(nBars):
            SubK,SubS = BarSolver(E[i],A[i],BarLengths[i],Phi[i])
            iGlobal = GetGlobalIndices([FirstNodes[i],SecondNodes[i]],DOF)
            K[np.ix_(iGlobal,iGlobal)] += SubK
            S[i,iGlobal] = SubS
        iGlobal = np.squeeze(np.where(BC))
        iRemove = GetGlobalIndices(iGlobal + 1,DOF)
        K_red = np.delete(K,iRemove,axis = 0)
        K_red = np.delete(K_red,iRemove,axis = 1)
        F_red = np.zeros((nNodes * DOF,1))
        for i in range(nNodes):
            iGlobal = GetGlobalIndices([i + 1],DOF)
            F_red[iGlobal[0]] = Fx[i]
            F_red[iGlobal[1]] = Fy[i]
        F_red = np.delete(F_red,iRemove,axis = 0)
        S_red = np.delete(S,iRemove,axis = 1)
        U0 = np.linalg.solve(K_red,F_red)
        Stress0 = np.dot(S_red,U0).reshape(nBars)
        dMdA = Rho * BarLengths
        for i in range(nBars):
            RHS = S_red[i,:].reshape(-1,1)
            Lambda_i = np.linalg.solve(K_red.T,RHS)
            for j in range(nBars):
                dKdAj = np.zeros((DOF * nNodes,DOF * nNodes))
                SubK,SubS = BarSolver(E[j],1.0,BarLengths[j],Phi[j])
                iGlobal = GetGlobalIndices([FirstNodes[j],SecondNodes[j]],DOF)
                dKdAj[np.ix_(iGlobal,iGlobal)] += SubK
                dKdAj_red = np.delete(dKdAj,iRemove,axis = 0)
                dKdAj_red = np.delete(dKdAj_red,iRemove,axis = 1)
                Term = np.dot(Lambda_i.T,np.dot(dKdAj_red,U0))
                dSdA[i,j] = -Term.item()

    # We configure the output dict.
    TenBarSolution = {
        'Mass':TrussSolution['Mass'],
        'Stress':TrussSolution['Stress'],
        'dMdA':dMdA,
        'dSdA':dSdA
    }
    
    return TenBarSolution
# ------------------------------------------------------------------------------------------------- #