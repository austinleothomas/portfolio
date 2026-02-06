# AEROSP 588 Fall 2025 - Assignment 2, Problem 3
# Authored By: Austin Leo Thomas
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- 
# We import modules as needed.
# ------------------------------------------------------------------------------------------- #
import numpy as np
import matplotlib.pyplot as plt
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define our backtracking line search algorithm.
# ------------------------------------------------------------------------------------------- #
def BackTrack(Func,GradFunc,X0,DirectionVect,AlphaInit,Rho,mu1):

    # We establish values.
    Alpha = AlphaInit
    Phi0 = Func(X0)
    PhiPrime0 = np.dot(GradFunc(X0),DirectionVect)
    Phi = Func(X0 + Alpha * DirectionVect)

    # We establish storage lists.
    PointStorage = [X0]
    AlphaStorage = [Alpha]

    # We implement a kill switch to prevent infinite looping.
    KillSwitch = 0

    # We iterate the backtracking algorithm.
    while Phi > Phi0 + mu1 * Alpha * PhiPrime0 and KillSwitch < 100:
        Alpha *= Rho
        X = X0 + Alpha * DirectionVect
        Phi = Func(X)
        AlphaStorage.append(np.copy(Alpha))
        KillSwitch += 1

    # We populate the point storage list.
    for Alpha in AlphaStorage:
        currX = X0 + Alpha * DirectionVect
        PointStorage.append(np.copy(currX))

    # We return the storage lists.
    return [AlphaStorage,PointStorage]
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define our strong Wolfe line search algorithm.
# ------------------------------------------------------------------------------------------- #
def StrongWolfe(Func,GradFunc,X0,DirectionVect,AlphaInit,mu1,mu2,Sigma):

    # We establish storage lists.
    PointStorage = [X0]
    AlphaStorage = [AlphaInit]

    # We establish values for bracketing
    Alpha1 = 0
    Alpha2 = AlphaInit
    Phi0 = Func(X0)
    PhiPrime0 = np.dot(GradFunc(X0),DirectionVect)
    Phi1 = Phi0
    PhiPrime1 = PhiPrime0
    isBracketing = True
    isPinpointing = False
    isFirstAttempt = True
    needPinpointing = True
    BracketingKillSwitch = 0

    # We implement bracketing.
    while isBracketing and BracketingKillSwitch < 100:
        Phi2 = Func(X0 + Alpha2 * DirectionVect)
        PhiPrime2 = np.dot(GradFunc(X0 + Alpha2 * DirectionVect),DirectionVect)
        if (Phi2 > Phi0 + mu1 * Alpha2 * PhiPrime0) or (not isFirstAttempt and Phi2 > Phi1):
            AlphaLow = Alpha1
            PhiLow = Phi1
            PhiPrimeLow = PhiPrime1
            AlphaHigh = Alpha2
            PhiHigh = Phi2
            isBracketing = False
        if (np.abs(PhiPrime2) <= -1 * mu2 * PhiPrime0) and isBracketing:
            isBracketing = False
            needPinpointing = False
        elif (PhiPrime2 >= 0) and isBracketing:
            AlphaLow = Alpha2
            PhiLow = Phi2
            PhiPrimeLow = PhiPrime2
            AlphaHigh = Alpha1
            PhiHigh = Phi1
            isBracketing = False
        elif isBracketing:
            Alpha1 = Alpha2
            Alpha2 = Sigma * Alpha2
        isFirstAttempt = False
        BracketingKillSwitch += 1
        AlphaStorage.append(np.copy(Alpha2))

    # We establish values for pinpointing.
    PinpointingKillSwitch = 0
    isPinpointing = needPinpointing

    # We implement pinpointing.
    while isPinpointing and PinpointingKillSwitch < 100:
        AlphaP = (2 * AlphaLow * (PhiHigh - PhiLow) + PhiPrimeLow * \
                  (AlphaLow**2 - AlphaHigh**2))/(2 * (PhiHigh - PhiLow + PhiPrimeLow * \
                                                      (AlphaLow - AlphaHigh)))
        PhiP = Func(X0 + AlphaP * DirectionVect)
        PhiPrimeP = np.dot(GradFunc(X0 + AlphaP * DirectionVect),DirectionVect)
        if (PhiP > Phi0 + mu1 * AlphaP * PhiPrime0) or (PhiP > PhiLow):
            AlphaHigh = AlphaP
            PhiHigh = PhiP
        else:
            if np.abs(PhiPrimeP) <= -1 * mu2 * PhiPrime0:
                isPinpointing = False
            elif PhiPrimeP * (AlphaHigh - AlphaLow) >= 0:
                AlphaHigh = AlphaLow
            AlphaLow = AlphaP
        PinpointingKillSwitch += 1
        AlphaStorage.append(np.copy(AlphaP))

    # We populate the point storage list.
    for Alpha in AlphaStorage:
        currX = X0 + Alpha * DirectionVect
        PointStorage.append(np.copy(currX))

    # We return the storage lists.
    return [AlphaStorage,PointStorage]
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define a line search plotting function.
# ------------------------------------------------------------------------------------------- #
def PlotLineSearch(AbscissaVals,fOrdinateVals,phiOrdinateVals,AbscissaPointVals,
                   OrdinatePointVals,xLim,xTicks,yLim,yTicks,FileName):
    
    # We define key plot parameters.
    FontSize = 12
    FontType = 'Cambria'
    PointStyle = 'o'
    phiColor = '#b31919'
    PointSize = 12
    fColor = '#1e26b3'
    LineWidth = 1

    # We plot.
    plt.plot(AbscissaVals,fOrdinateVals,linewidth = LineWidth,color = fColor,
             label = r'$f(\alpha)$',zorder = 1)
    plt.plot(AbscissaVals,phiOrdinateVals,linewidth = LineWidth,color = phiColor,
             label = r'$\phi(\alpha)$',zorder = 2)
    plt.scatter(AbscissaPointVals,OrdinatePointVals,color = fColor,s = PointSize,
                marker = PointStyle,zorder = 3)
    plt.xlim(xLim)
    plt.xticks(xTicks)
    plt.ylim(yLim)
    plt.yticks(yTicks)
    plt.xlabel(r'$\alpha$',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
    plt.ylabel(r'$f$',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
    plt.legend()
    plt.savefig(FileName,bbox_inches = 'tight')
    plt.clf()
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define a contour plot w/ iteration path plotting function.
# ------------------------------------------------------------------------------------------- #
def PlotContourWithPath(X1,X2,F,ContourLevels,Points,x1Lim,x2Lim,FileName):
    
    # We define properties of the plot.
    FontSize = 12
    FontType = 'Cambria'
    PointStyle = 'ko-'
    PointSize = 4
    LineWidth = 1
    LabelFontSize = 8
    LabelColor = 'black'

    # We convert the collection of points to an array.
    Array = np.array(Points)
    CritPoint = Array[-1]

    # We create the contour plot.
    plt.contour(X1,X2,F,cmap = 'Blues_r',levels = ContourLevels,zorder = 1)
    plt.plot(Array[:,0],Array[:,1],PointStyle,markersize = PointSize,
             linewidth = LineWidth,zorder = 2)
    plt.annotate(r'$x*$',xy = (CritPoint[0],CritPoint[1]),fontsize = LabelFontSize,
                 xytext = (10,-10),textcoords = 'offset points',ha = 'center',
                 va = 'center',color = LabelColor,bbox = dict(facecolor = 'white',
                                                              edgecolor = 'none',
                                                              boxstyle = 'round',
                                                              pad = 0.1
                                                              ))
    
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
# We apply both algorithms to Example 4.8 and compare results.
# ------------------------------------------------------------------------------------------- #
# We define the function.
def Func_Ex8(X):
    x1,x2 = X
    f = 0.1*x1**6 - 1.5*x1**4 + 5*x1**2 + 0.1*x2**4 + 3*x2**2 - 9*x2 + 0.5*x1*x2
    return f

# We define the gradient function.
def GradFunc_Ex8(X):
    x1,x2 = X
    fx1 = 0.6*x1**5 - 6*x1**3 + 10*x1 + 0.5*x2
    fx2 = 0.4*x2**3 + 6*x2 - 9 + 0.5*x1
    return np.array([fx1,fx2])

# We define constant parameters per Example 4.8.
X0_Ex8 = np.array([-1.25,1.25])
P_Ex8 = np.array([4,0.75])
mu1_Ex8 = 1e-4
Rho_Ex8 = 0.7
AlphaInitLarge_Ex8 = 1.2
AlphaInitSmall_Ex8 = 0.05

# We define constant parameters per Example 4.9.
mu2_Ex9 = 0.9
Sigma_Ex9 = 2

# We call upon the backtracking line search function for the large AlphaInit value.
[AlphaValsLarge_Ex8,XValsLarge_Ex8] = BackTrack(Func_Ex8,
                                                GradFunc_Ex8,
                                                X0_Ex8,
                                                P_Ex8,
                                                AlphaInitLarge_Ex8,
                                                Rho_Ex8,
                                                mu1_Ex8
                                                )

# We call upon the backtracking line search function for the small AlphaInit value.
[AlphaValsSmall_Ex8,XValsSmall_Ex8] = BackTrack(Func_Ex8,
                                                GradFunc_Ex8,
                                                X0_Ex8,
                                                P_Ex8,
                                                AlphaInitSmall_Ex8,
                                                Rho_Ex8,
                                                mu1_Ex8
                                                )

# We call upon the strong Wolfe line search function for the large AlphaInit value.
[AlphaValsLarge_Ex9,XValsLarge_Ex9] = StrongWolfe(Func_Ex8,
                                                  GradFunc_Ex8,
                                                  X0_Ex8,
                                                  P_Ex8,
                                                  AlphaInitLarge_Ex8,
                                                  mu1_Ex8,
                                                  mu2_Ex9,
                                                  Sigma_Ex9
                                                  )

# We call upon the strong Wolfe line search function for the small AlphaInit value.
[AlphaValsSmall_Ex9,XValsSmall_Ex9] = StrongWolfe(Func_Ex8,
                                                  GradFunc_Ex8,
                                                  X0_Ex8,
                                                  P_Ex8,
                                                  AlphaInitSmall_Ex8,
                                                  mu1_Ex8,
                                                  mu2_Ex9,
                                                  Sigma_Ex9
                                                  )

# We define f and phi function values along the path, for plotting purposes.
AbscissaVals_Ex8 = np.linspace(0,1.2,100)
fOrdinateVals_Ex8 = [0] * len(AbscissaVals_Ex8)
phiOrdinateVals_Ex8 = [0] * len(AbscissaVals_Ex8)
for i,Alpha in enumerate(AbscissaVals_Ex8):
    fOrdinateVals_Ex8[i] = Func_Ex8(X0_Ex8 + Alpha * P_Ex8)
    phiOrdinateVals_Ex8[i] = [Func_Ex8(X0_Ex8) + mu1_Ex8 * Alpha * 
                              np.dot(GradFunc_Ex8(X0_Ex8),P_Ex8)]

# We evaluate f at the alpha-values of each backtracking iteration.
ScatterFuncValsLarge_Ex8 = [0] * len(AlphaValsLarge_Ex8)
ScatterFuncValsSmall_Ex8 = [0] * len(AlphaValsSmall_Ex8)
for i in range(len(AlphaValsLarge_Ex8)):
    ScatterFuncValsLarge_Ex8[i] = Func_Ex8(XValsLarge_Ex8[i+1])
for i in range(len(AlphaValsSmall_Ex8)):
    ScatterFuncValsSmall_Ex8[i] = Func_Ex8(XValsSmall_Ex8[i+1])

# We evaluate f at the alpha-values of each strong Wolfe iteration.
AlphaValsLarge_Ex9.insert(3,AlphaValsSmall_Ex9[5])
XValsLarge_Ex9.insert(4,XValsSmall_Ex9[6])
del AlphaValsSmall_Ex9[5]
del XValsSmall_Ex9[6]
ScatterFuncValsLarge_Ex9 = [0] * len(AlphaValsLarge_Ex9)
ScatterFuncValsSmall_Ex9 = [0] * len(AlphaValsSmall_Ex9)
for i in range(len(AlphaValsLarge_Ex9)):
    ScatterFuncValsLarge_Ex9[i] = Func_Ex8(XValsLarge_Ex9[i+1])
for i in range(len(AlphaValsSmall_Ex9)):
    ScatterFuncValsSmall_Ex9[i] = Func_Ex8(XValsSmall_Ex9[i+1])

# We define paramaters for plot generation for this problem.
xLim_Ex8 = [0,1.2]
xTicks_Ex8 = np.arange(0,1.2,0.2)
yLim_Ex8 = [-10,30]
yTicks_Ex8 = np.arange(-10,30,10)

# We generate plots.
PlotLineSearch(AbscissaVals_Ex8,
               fOrdinateVals_Ex8,
               phiOrdinateVals_Ex8,
               AlphaValsSmall_Ex8,
               ScatterFuncValsSmall_Ex8,
               xLim_Ex8,
               xTicks_Ex8,
               yLim_Ex8,
               yTicks_Ex8,
               'prob2_3_Ex8_BackTrack_Small.svg'
               )
PlotLineSearch(AbscissaVals_Ex8,
               fOrdinateVals_Ex8,
               phiOrdinateVals_Ex8,
               AlphaValsLarge_Ex8,
               ScatterFuncValsLarge_Ex8,
               xLim_Ex8,
               xTicks_Ex8,
               yLim_Ex8,
               yTicks_Ex8,
               'prob2_3_Ex8_BackTrack_Large.svg'
               )
PlotLineSearch(AbscissaVals_Ex8,
               fOrdinateVals_Ex8,
               phiOrdinateVals_Ex8,
               AlphaValsLarge_Ex9,
               ScatterFuncValsLarge_Ex9,
               xLim_Ex8,
               xTicks_Ex8,
               yLim_Ex8,
               yTicks_Ex8,
               'prob2_3_Ex9_StrongWolfe_Large.svg'
               )
PlotLineSearch(AbscissaVals_Ex8,
               fOrdinateVals_Ex8,
               phiOrdinateVals_Ex8,
               AlphaValsSmall_Ex9,
               ScatterFuncValsSmall_Ex9,
               xLim_Ex8,
               xTicks_Ex8,
               yLim_Ex8,
               yTicks_Ex8,
               'prob2_3_Ex9_StrongWolfe_Small.svg'
               )

# We define value arrays for the contour plot.
x1Bounds_Ex8 = [-4,4]
x2Bounds_Ex8 = [0,2.5]
x1_Ex8 = np.linspace(x1Bounds_Ex8[0],x1Bounds_Ex8[1],1000)
x2_Ex8 = np.linspace(x2Bounds_Ex8[0],x2Bounds_Ex8[1],1000)
X1_Ex8,X2_Ex8 = np.meshgrid(x1_Ex8,x2_Ex8)
X_Ex8 = X1_Ex8,X2_Ex8
F_Ex8 = Func_Ex8(X_Ex8)

# We define parameters for the contour plots.
ContourLevels_Ex8 = np.linspace(-25,25,30)

# We generate contour plots.
PlotContourWithPath(X1_Ex8,
                    X2_Ex8,
                    F_Ex8,
                    ContourLevels_Ex8,
                    XValsLarge_Ex8,
                    x1Bounds_Ex8,
                    x2Bounds_Ex8,
                    'prob2_3_Ex8_BackTrack_Large_Contour.svg'
                    )
PlotContourWithPath(X1_Ex8,
                    X2_Ex8,
                    F_Ex8,
                    ContourLevels_Ex8,
                    XValsSmall_Ex8,
                    x1Bounds_Ex8,
                    x2Bounds_Ex8,
                    'prob2_3_Ex8_BackTrack_Small_Contour.svg'
                    )
PlotContourWithPath(X1_Ex8,
                    X2_Ex8,
                    F_Ex8,
                    ContourLevels_Ex8,
                    XValsLarge_Ex9,
                    x1Bounds_Ex8,
                    x2Bounds_Ex8,
                    'prob2_3_Ex9_StrongWolfe_Large_Contour.svg'
                    )
PlotContourWithPath(X1_Ex8,
                    X2_Ex8,
                    F_Ex8,
                    ContourLevels_Ex8,
                    XValsSmall_Ex9,
                    x1Bounds_Ex8,
                    x2Bounds_Ex8,
                    'prob2_3_Ex9_StrongWolfe_Small_Contour.svg'
                    )
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We apply both algorithms to the equation from Problem (2.2).
# ------------------------------------------------------------------------------------------- #
# We define the function.
def Func_Ex22(X):
    x1,x2 = X
    f = x1**4 + 3*x1**3 + 3*x2**2 - 6*x1*x2 - 2*x2
    return f

# We define the gradient function.
def GradFunc_Ex22(X):
    x1,x2 = X
    fx1 = 4*x1**3 + 9*x1**2 - 6*x2
    fx2 = 6*x2 - 6*x1 - 2
    return np.array([fx1,fx2])

# We define stagnant parameters.
mu1_Ex22 = 1e-4
Rho_Ex22 = 0.7
mu2_Ex22 = 0.9
Sigma_Ex22 = 2
AlphaInit_Ex22 = 1

# We define base parameters for initial point and step direction.
X0_Ex22_Base = np.array([-1,-1])
P_Ex22_Base = np.array([-np.sqrt(2),-np.sqrt(2)])

# We define experimental parameters for initial point and step direction.
X0_Ex22_Exp = np.array([0,1])
P_Ex22_Exp = np.array([1,0])

# We call upon the backtracking line search function for base values.
[AlphaValsBack_Ex22_Base,XValsBack_Ex22_Base] = BackTrack(Func_Ex22,
                                                          GradFunc_Ex22,
                                                          X0_Ex22_Base,
                                                          P_Ex22_Base,
                                                          AlphaInit_Ex22,
                                                          Rho_Ex22,
                                                          mu1_Ex22
                                                          )

# We call upon the backtracking line search function for experimental values.
[AlphaValsBack_Ex22_Exp,XValsBack_Ex22_Exp] = BackTrack(Func_Ex22,
                                                        GradFunc_Ex22,
                                                        X0_Ex22_Exp,
                                                        P_Ex22_Exp,
                                                        AlphaInit_Ex22,
                                                        Rho_Ex22,
                                                        mu1_Ex22
                                                        )

# We call upon the strong Wolfe line search function for base values.
[AlphaValsWolfe_Ex22_Base,XValsWolfe_Ex22_Base] = StrongWolfe(Func_Ex22,
                                                              GradFunc_Ex22,
                                                              X0_Ex22_Base,
                                                              P_Ex22_Base,
                                                              AlphaInit_Ex22,
                                                              mu1_Ex22,
                                                              mu2_Ex22,
                                                              Sigma_Ex22
                                                              )

# We call upon the strong Wolfe line search function for experimental values.
[AlphaValsWolfe_Ex22_Exp,XValsWolfe_Ex22_Exp] = StrongWolfe(Func_Ex22,
                                                            GradFunc_Ex22,
                                                            X0_Ex22_Exp,
                                                            P_Ex22_Exp,
                                                            AlphaInit_Ex22,
                                                            mu1_Ex22,
                                                            mu2_Ex22,
                                                            Sigma_Ex22
                                                            )

# We define paramaters for plot generation for this problem.
xLim_Ex22 = [0,1]
xTicks_Ex22 = np.arange(0,1,0.2)
yLim_Ex22_Base = [-25,0]
yTicks_Ex22_Base = np.arange(-25,0,5)
yLim_Ex22_Exp = [-10,10]
yTicks_Ex22_Exp = np.arange(-10,10,5)

# We define f and phi function values along both paths, for plotting purposes.
AbscissaVals_Ex22 = np.linspace(0,AlphaInit_Ex22,100)
fOrdinateVals_Ex22_Base = [0] * len(AbscissaVals_Ex22)
fOrdinateVals_Ex22_Exp = [0] * len(AbscissaVals_Ex22)
phiOrdinateVals_Ex22_Base = [0] * len(AbscissaVals_Ex22)
phiOrdinateVals_Ex22_Exp = [0] * len(AbscissaVals_Ex22)
for i,Alpha in enumerate(AbscissaVals_Ex22):
    fOrdinateVals_Ex22_Base[i] = Func_Ex22(X0_Ex22_Base + Alpha * P_Ex22_Base)
    fOrdinateVals_Ex22_Exp[i] = Func_Ex22(X0_Ex22_Exp + Alpha * P_Ex22_Exp)
    phiOrdinateVals_Ex22_Base[i] = Func_Ex22(X0_Ex22_Base) + mu1_Ex22 * Alpha * \
                                    np.dot(GradFunc_Ex22(X0_Ex22_Base),P_Ex22_Base)
    phiOrdinateVals_Ex22_Exp[i] = Func_Ex22(X0_Ex22_Exp) + mu1_Ex22 * Alpha * \
                                    np.dot(GradFunc_Ex22(X0_Ex22_Exp),P_Ex22_Exp)

# We evaluate f at the alpha-values of each backtracking iteration.
ScatterFuncValsBack_Ex22_Base = [0] * len(AlphaValsBack_Ex22_Base)
ScatterFuncValsBack_Ex22_Exp = [0] * len(AlphaValsBack_Ex22_Exp)
for i in range(len(AlphaValsBack_Ex22_Base)):
    ScatterFuncValsBack_Ex22_Base[i] = Func_Ex22(XValsBack_Ex22_Base[i+1])
for i in range(len(AlphaValsBack_Ex22_Exp)):
    ScatterFuncValsBack_Ex22_Exp[i] = Func_Ex22(XValsBack_Ex22_Exp[i+1])

# We evaluate f at the alpha-values of each strong Wolfe iteration.
ScatterFuncValsWolfe_Ex22_Base = [0] * len(AlphaValsWolfe_Ex22_Base)
ScatterFuncValsWolfe_Ex22_Exp = [0] * len(AlphaValsWolfe_Ex22_Exp)
for i in range(len(AlphaValsWolfe_Ex22_Base)):
    ScatterFuncValsWolfe_Ex22_Base[i] = Func_Ex22(XValsWolfe_Ex22_Base[i+1])
for i in range(len(AlphaValsWolfe_Ex22_Exp)):
    ScatterFuncValsWolfe_Ex22_Exp[i] = Func_Ex22(XValsWolfe_Ex22_Exp[i+1])

# We generate plots for both methods, for both base and experimental values.
PlotLineSearch(AbscissaVals_Ex22,
               fOrdinateVals_Ex22_Base,
               phiOrdinateVals_Ex22_Base,
               AlphaValsBack_Ex22_Base,
               ScatterFuncValsBack_Ex22_Base,
               xLim_Ex22,
               xTicks_Ex22,
               yLim_Ex22_Base,
               yTicks_Ex22_Base,
               'prob2_3_Ex22_BackTrack_Base.svg'
               )
PlotLineSearch(AbscissaVals_Ex22,
               fOrdinateVals_Ex22_Exp,
               phiOrdinateVals_Ex22_Exp,
               AlphaValsBack_Ex22_Exp,
               ScatterFuncValsBack_Ex22_Exp,
               xLim_Ex22,
               xTicks_Ex22,
               yLim_Ex22_Exp,
               yTicks_Ex22_Exp,
               'prob2_3_Ex22_BackTrack_Exp.svg'
               )
PlotLineSearch(AbscissaVals_Ex22,
               fOrdinateVals_Ex22_Base,
               phiOrdinateVals_Ex22_Base,
               AlphaValsWolfe_Ex22_Base,
               ScatterFuncValsWolfe_Ex22_Base,
               xLim_Ex22,
               xTicks_Ex22,
               yLim_Ex22_Base,
               yTicks_Ex22_Base,
               'prob2_3_Ex22_WolfeTrack_Base.svg'
               )
PlotLineSearch(AbscissaVals_Ex22,
               fOrdinateVals_Ex22_Exp,
               phiOrdinateVals_Ex22_Exp,
               AlphaValsWolfe_Ex22_Exp,
               ScatterFuncValsWolfe_Ex22_Exp,
               xLim_Ex22,
               xTicks_Ex22,
               yLim_Ex22_Exp,
               yTicks_Ex22_Exp,
               'prob2_3_Ex22_WolfeTrack_Exp.svg'
               )

# We define test arrays for mu2 and rho.
mu2_Ex22_Array = [0.2,0.4,0.6,0.8]
rho_Ex22_Array = [0.2,0.4,0.6,0.8]

# We calculate the number of iterations of backtracking for different rho-values.
print()
print('Problem (2.2) Equation, Backtracking, rho Variation...')
for rho in rho_Ex22_Array:
    [AlphaValsBack_Ex22_RhoVary,XValsBack_Ex22_RhoVary] = BackTrack(Func_Ex22,
                                                                    GradFunc_Ex22,
                                                                    X0_Ex22_Exp,
                                                                    P_Ex22_Exp,
                                                                    AlphaInit_Ex22,
                                                                    rho,
                                                                    mu1_Ex22
                                                                    )
    IterNum = len(AlphaValsBack_Ex22_RhoVary)
    print('For rho = ' + str(rho) + ' backtracking takes ' + str(IterNum) + ' iterations.')
print()

# We calculate the number of iterations of strong Wolfe for different mu2-values.
print()
print('Problem (2.2) Equation, strong Wolfe, mu2 Variation...')
for mu2 in mu2_Ex22_Array:
    [AlphaValsWolfe_Ex22_mu2Vary,XValsWolfe_Ex22_mu2Vary] = StrongWolfe(Func_Ex22,
                                                                        GradFunc_Ex22,
                                                                        X0_Ex22_Exp,
                                                                        P_Ex22_Exp,
                                                                        AlphaInit_Ex22,
                                                                        mu1_Ex22,
                                                                        mu2,
                                                                        Sigma_Ex22
                                                                        )
    IterNum = len(AlphaValsWolfe_Ex22_mu2Vary)
    print('For mu2 = ' + str(mu2) + ' strong Wolfe takes ' + str(IterNum) + ' iterations.')
print()
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We apply both algorithms to the two-dimensional Rosenbrock function.
# ------------------------------------------------------------------------------------------- #
# We define the function.
def Func_ExRosen2(X):
    x1,x2 = X
    f = x1**4 + 3*x1**3 + 3*x2**2 - 6*x1*x2 - 2*x2
    return f

# We define the gradient function.
def GradFunc_ExRosen2(X):
    x1,x2 = X
    fx1 = 2 * (200*x1**3 - 200*x1*x2 + x1 - 1)
    fx2 = 200 * (x2 - x1**2)
    return np.array([fx1,fx2])

# We define stagnant parameters.
mu1_ExRosen2 = 1e-4
Rho_ExRosen2 = 0.7
mu2_ExRosen2 = 0.9
Sigma_ExRosen2 = 2
AlphaInit_ExRosen2 = 2

# We define base parameters for initial point and step direction.
X0_ExRosen2_Base = np.array([0,0])
P_ExRosen2_Base = np.array([np.sqrt(2),np.sqrt(2)])

# We define experimental parameters for initial point and step direction.
X0_ExRosen2_Exp = np.array([1,0])
P_ExRosen2_Exp = np.array([-1,0])

# We call upon the backtracking line search function for base values.
[AlphaValsBack_ExRosen2_Base,XValsBack_ExRosen2_Base] = BackTrack(Func_ExRosen2,
                                                          GradFunc_ExRosen2,
                                                          X0_ExRosen2_Base,
                                                          P_ExRosen2_Base,
                                                          AlphaInit_ExRosen2,
                                                          Rho_ExRosen2,
                                                          mu1_ExRosen2
                                                          )

# We call upon the backtracking line search function for experimental values.
[AlphaValsBack_ExRosen2_Exp,XValsBack_ExRosen2_Exp] = BackTrack(Func_ExRosen2,
                                                        GradFunc_ExRosen2,
                                                        X0_ExRosen2_Exp,
                                                        P_ExRosen2_Exp,
                                                        AlphaInit_ExRosen2,
                                                        Rho_ExRosen2,
                                                        mu1_ExRosen2
                                                        )

# We call upon the strong Wolfe line search function for base values.
[AlphaValsWolfe_ExRosen2_Base,XValsWolfe_ExRosen2_Base] = StrongWolfe(Func_ExRosen2,
                                                              GradFunc_ExRosen2,
                                                              X0_ExRosen2_Base,
                                                              P_ExRosen2_Base,
                                                              AlphaInit_ExRosen2,
                                                              mu1_ExRosen2,
                                                              mu2_ExRosen2,
                                                              Sigma_ExRosen2
                                                              )

# We call upon the strong Wolfe line search function for experimental values.
[AlphaValsWolfe_ExRosen2_Exp,XValsWolfe_ExRosen2_Exp] = StrongWolfe(Func_ExRosen2,
                                                            GradFunc_ExRosen2,
                                                            X0_ExRosen2_Exp,
                                                            P_ExRosen2_Exp,
                                                            AlphaInit_ExRosen2,
                                                            mu1_ExRosen2,
                                                            mu2_ExRosen2,
                                                            Sigma_ExRosen2
                                                            )

# We define paramaters for plot generation for this problem.
xLim_ExRosen2 = [0,2]
xTicks_ExRosen2 = np.arange(0,2,0.4)
yLim_ExRosen2_Base = [-5,5]
yTicks_ExRosen2_Base = np.arange(-5,5,2)
yLim_ExRosen2_Exp = [-5,10]
yTicks_ExRosen2_Exp = np.arange(-5,10,3)

# We define f and phi function values along both paths, for plotting purposes.
AbscissaVals_ExRosen2 = np.linspace(0,AlphaInit_ExRosen2,100)
fOrdinateVals_ExRosen2_Base = [0] * len(AbscissaVals_ExRosen2)
fOrdinateVals_ExRosen2_Exp = [0] * len(AbscissaVals_ExRosen2)
phiOrdinateVals_ExRosen2_Base = [0] * len(AbscissaVals_ExRosen2)
phiOrdinateVals_ExRosen2_Exp = [0] * len(AbscissaVals_ExRosen2)
for i,Alpha in enumerate(AbscissaVals_ExRosen2):
    fOrdinateVals_ExRosen2_Base[i] = Func_ExRosen2(X0_ExRosen2_Base + Alpha * P_ExRosen2_Base)
    fOrdinateVals_ExRosen2_Exp[i] = Func_ExRosen2(X0_ExRosen2_Exp + Alpha * P_ExRosen2_Exp)
    phiOrdinateVals_ExRosen2_Base[i] = Func_ExRosen2(X0_ExRosen2_Base) + mu1_ExRosen2 * Alpha * \
                                    np.dot(GradFunc_ExRosen2(X0_ExRosen2_Base),P_ExRosen2_Base)
    phiOrdinateVals_ExRosen2_Exp[i] = Func_ExRosen2(X0_ExRosen2_Exp) + mu1_ExRosen2 * Alpha * \
                                    np.dot(GradFunc_ExRosen2(X0_ExRosen2_Exp),P_ExRosen2_Exp)

# We evaluate f at the alpha-values of each backtracking iteration.
ScatterFuncValsBack_ExRosen2_Base = [0] * len(AlphaValsBack_ExRosen2_Base)
ScatterFuncValsBack_ExRosen2_Exp = [0] * len(AlphaValsBack_ExRosen2_Exp)
for i in range(len(AlphaValsBack_ExRosen2_Base)):
    ScatterFuncValsBack_ExRosen2_Base[i] = Func_ExRosen2(XValsBack_ExRosen2_Base[i+1])
for i in range(len(AlphaValsBack_ExRosen2_Exp)):
    ScatterFuncValsBack_ExRosen2_Exp[i] = Func_ExRosen2(XValsBack_ExRosen2_Exp[i+1])

# We evaluate f at the alpha-values of each strong Wolfe iteration.
ScatterFuncValsWolfe_ExRosen2_Base = [0] * len(AlphaValsWolfe_ExRosen2_Base)
ScatterFuncValsWolfe_ExRosen2_Exp = [0] * len(AlphaValsWolfe_ExRosen2_Exp)
for i in range(len(AlphaValsWolfe_ExRosen2_Base)):
    ScatterFuncValsWolfe_ExRosen2_Base[i] = Func_ExRosen2(XValsWolfe_ExRosen2_Base[i+1])
for i in range(len(AlphaValsWolfe_ExRosen2_Exp)):
    ScatterFuncValsWolfe_ExRosen2_Exp[i] = Func_ExRosen2(XValsWolfe_ExRosen2_Exp[i+1])

# We generate plots for both methods, for both base and experimental values.
PlotLineSearch(AbscissaVals_ExRosen2,
               fOrdinateVals_ExRosen2_Base,
               phiOrdinateVals_ExRosen2_Base,
               AlphaValsBack_ExRosen2_Base,
               ScatterFuncValsBack_ExRosen2_Base,
               xLim_ExRosen2,
               xTicks_ExRosen2,
               yLim_ExRosen2_Base,
               yTicks_ExRosen2_Base,
               'prob2_3_ExRosen2_BackTrack_Base.svg'
               )
PlotLineSearch(AbscissaVals_ExRosen2,
               fOrdinateVals_ExRosen2_Exp,
               phiOrdinateVals_ExRosen2_Exp,
               AlphaValsBack_ExRosen2_Exp,
               ScatterFuncValsBack_ExRosen2_Exp,
               xLim_ExRosen2,
               xTicks_ExRosen2,
               yLim_ExRosen2_Exp,
               yTicks_ExRosen2_Exp,
               'prob2_3_ExRosen2_BackTrack_Exp.svg'
               )
PlotLineSearch(AbscissaVals_ExRosen2,
               fOrdinateVals_ExRosen2_Base,
               phiOrdinateVals_ExRosen2_Base,
               AlphaValsWolfe_ExRosen2_Base,
               ScatterFuncValsWolfe_ExRosen2_Base,
               xLim_ExRosen2,
               xTicks_ExRosen2,
               yLim_ExRosen2_Base,
               yTicks_ExRosen2_Base,
               'prob2_3_ExRosen2_WolfeTrack_Base.svg'
               )
PlotLineSearch(AbscissaVals_ExRosen2,
               fOrdinateVals_ExRosen2_Exp,
               phiOrdinateVals_ExRosen2_Exp,
               AlphaValsWolfe_ExRosen2_Exp,
               ScatterFuncValsWolfe_ExRosen2_Exp,
               xLim_ExRosen2,
               xTicks_ExRosen2,
               yLim_ExRosen2_Exp,
               yTicks_ExRosen2_Exp,
               'prob2_3_ExRosen2_WolfeTrack_Exp.svg'
               )

# We define test arrays for mu2 and rho.
mu2_ExRosen2_Array = [0.2,0.4,0.6,0.8]
rho_ExRosen2_Array = [0.2,0.4,0.6,0.8]

# We calculate the number of iterations of backtracking for different rho-values.
print()
print('2D Rosenbrock Function, Backtracking, rho Variation...')
for rho in rho_ExRosen2_Array:
    [AlphaValsBack_ExRosen2_RhoVary,XValsBack_ExRosen2_RhoVary] = BackTrack(Func_ExRosen2,
                                                                    GradFunc_ExRosen2,
                                                                    X0_ExRosen2_Exp,
                                                                    P_ExRosen2_Exp,
                                                                    AlphaInit_ExRosen2,
                                                                    rho,
                                                                    mu1_ExRosen2
                                                                    )
    IterNum = len(AlphaValsBack_ExRosen2_RhoVary)
    print('For rho = ' + str(rho) + ' backtracking takes ' + str(IterNum) + ' iterations.')
print()

# We calculate the number of iterations of strong Wolfe for different mu2-values.
print()
print('2D Rosenbrock Function, strong Wolfe, mu2 Variation...')
for mu2 in mu2_ExRosen2_Array:
    [AlphaValsWolfe_ExRosen2_mu2Vary,XValsWolfe_ExRosen2_mu2Vary] = StrongWolfe(Func_ExRosen2,
                                                                        GradFunc_ExRosen2,
                                                                        X0_ExRosen2_Exp,
                                                                        P_ExRosen2_Exp,
                                                                        AlphaInit_ExRosen2,
                                                                        mu1_ExRosen2,
                                                                        mu2,
                                                                        Sigma_ExRosen2
                                                                        )
    IterNum = len(AlphaValsWolfe_ExRosen2_mu2Vary)
    print('For mu2 = ' + str(mu2) + ' strong Wolfe takes ' + str(IterNum) + ' iterations.')
print()
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We apply both algorithms to the six-dimensional Rosenbrock function.
# ------------------------------------------------------------------------------------------- #
# We define the function.
def Func_ExRosen6(x):
    f = np.sum(100 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)
    return f

# We define the gradient function.
def GradFunc_ExRosen6(x):
    Grad = np.zeros_like(x)
    Grad[0] = -400 * x[0] * (x[1] - x[0]**2) + 2 * (x[0] - 1)
    for i in range(1,len(x) - 1):
        Grad[i] = (-400 * x[i] * (x[i+1] - x[i]**2) + 2 * (x[i] - 1) + 200 * \
                   (x[i] - x[i-1]**2))
    Grad[len(x) - 1] = 200 * (x[len(x) - 1] - x[len(x) - 2]**2)
    return Grad

# We define stagnant parameters.
mu1_ExRosen6 = 1e-4
Rho_ExRosen6 = 0.7
mu2_ExRosen6 = 0.9
Sigma_ExRosen6 = 2
AlphaInit_ExRosen6 = 2
X0_ExRosen6 = np.array([0,0,0,0,0,0])
P_ExRosen6 = np.array([np.sqrt(2),np.sqrt(2),np.sqrt(2),np.sqrt(2),np.sqrt(2),np.sqrt(2)])

# We apply the backtracking algorithm.
[AlphaValsBack_ExRosen6,XValsBack_ExRosen6] = BackTrack(Func_ExRosen6,
                                                          GradFunc_ExRosen6,
                                                          X0_ExRosen6,
                                                          P_ExRosen6,
                                                          AlphaInit_ExRosen6,
                                                          Rho_ExRosen6,
                                                          mu1_ExRosen6
                                                          )

# We apply the strong Wolfe algorithm.
[AlphaValsWolfe_ExRosen6,XValsWolfe_ExRosen6] = StrongWolfe(Func_ExRosen6,
                                                            GradFunc_ExRosen6,
                                                            X0_ExRosen6,
                                                            P_ExRosen6,
                                                            AlphaInit_ExRosen6,
                                                            mu1_ExRosen6,
                                                            mu2_ExRosen6,
                                                            Sigma_ExRosen6
                                                            )

# We evaluate function values and extract iteration counts.
Rosen6_Back_Iter = len(AlphaValsBack_ExRosen6)
Rosen6_Wolfe_Iter = len(AlphaValsWolfe_ExRosen6)
Rosen6_Back_Val = Func_ExRosen6(XValsBack_ExRosen6[-1])
Rosen6_Wolfe_Val = Func_ExRosen6(XValsWolfe_ExRosen6[-1])

# We print values to the terminal.
print()
print('6D Rosenbrock, Backtracking...')
print('Found f = ' + str(Rosen6_Back_Val) + ' after ' + str(Rosen6_Back_Iter) + ' iterations.')
print()
print('6D Rosenbrock, strong Wolfe...')
print('Found f = ' + str(Rosen6_Wolfe_Val) + ' after ' + str(Rosen6_Wolfe_Iter) + ' iterations.')
print()
# ------------------------------------------------------------------------------------------- #