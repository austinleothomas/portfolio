# This script solves Problem 4.4 for AEROSP 588.
# --------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------#
# We import modules as needed.
# --------------------------------------------------------------------------------------------#
import numpy as np
import matplotlib.pyplot as plt
from Toolbox.EqualityConstrainedSQP import EqualityConstrainedSQP as SQP
# --------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------#
# We generate an optimization path plotting function.
# --------------------------------------------------------------------------------------------#
def GeneratePathPlot(X1,X2,F,H,ContourLevels,Points,x1Lim,x2Lim,AnnotLoc,FileName,isShow):
    
    # We define properties of the plot.
    FontSize = 11
    FontType = 'Cambria'
    PathColor = '#b31919'
    LineWidth = 1

    # We convert the collection of points to an array.
    Array = np.array(Points)

    # We create the contour plot.
    plt.contour(X1,X2,F,cmap = 'Blues_r',levels = ContourLevels,zorder = 1)
    plt.contour(X1,X2,H,levels = [0],colors = 'black',zorder = 2)
    plt.plot(Array[:,0],Array[:,1],color = PathColor,linewidth = LineWidth,zorder = 3)

    # We create annotations for the plot.
    plt.annotate(
        r'$x_0$',
        xy = (Array[0,0],Array[0,1]),
        xytext = (5,0),
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
        xytext = (0,8),
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
        r'$h(x)$',
        xy = (Array[0,0],Array[0,1]),
        xytext = AnnotLoc,
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
    if isShow:
        plt.show()
    plt.clf()
# --------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------#
# We define the optimization problem in Ex. 5.4.
# --------------------------------------------------------------------------------------------#
def Func54(X):
    x1,x2 = X
    F = x1 + 2 * x2
    delF = np.zeros(2)
    delF[0] = 1
    delF[1] = 2
    return F,delF

def Cons54(X):
    x1,x2 = X
    H = 0.25 * x1 ** 2 + x2 ** 2 - 1
    JacH = np.zeros(2)
    JacH[0] = 0.5 * x1
    JacH[1] = 2 * x2
    return H,JacH
# --------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------#
# We call upon our SQP optimizer to solve Ex. 5.4.
# --------------------------------------------------------------------------------------------#
xInit54 = [1,1]
Output54 = SQP(Func54,Cons54,xInit54,None)

print('\n')
print('Success on Ex. (5.4)!')
print('Optimum Point:')
print(Output54['xStar'])
print('Optimum Value: ',Output54['fStar'])
print('Iterations: ',Output54['Iterations'])
print('\n')
# --------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------#
# We plot the optimization path for Ex. 5.4.
# --------------------------------------------------------------------------------------------#
# We generate x1-, x2-, f-, and h-values for the function.
x1 = np.linspace(-3,3,100)
x2 = np.linspace(-2.5,2.5,100)
X1,X2 = np.meshgrid(x1,x2)
F = np.zeros_like(X1)
H = np.zeros_like(X2)
for i in range(X1.shape[0]):
    for j in range(X1.shape[1]):
        F[i,j],_ = Func54((X1[i,j],X2[i,j]))
        H[i,j],_ = Cons54((X1[i,j],X2[i,j]))

# We generate plotting values for the slanted quadratic.
Contours54 = np.linspace(-10,25,30)
x1Lim54 = [x1[0],x1[-1]]
x2Lim54 = [x2[0],x2[-1]]
AnnotLoc54 = (65,-45)
FileName54 = 'Ex54_PathPlot.svg'

# We call upon our plotting function.
GeneratePathPlot(
    X1,
    X2,
    F,
    H,
    Contours54,
    Output54['PointStorage'],
    x1Lim54,
    x2Lim54,
    AnnotLoc54,
    FileName54,
    False
)
# --------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------#
# We define the multidimensional Rosenbrock function and constraint functions.
# --------------------------------------------------------------------------------------------#
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

def GetCons(n):
    def Cons(X):
        H = np.zeros((n,1))
        JacH = np.zeros((n,len(X)))
        if n == 1:
            H[0] = np.sum(X)
            JacH[0,:] = 1
            JacH = JacH[0]
        if n >= 2:
            H[0] = np.sum(X)
            H[1] = X[0] ** 2 + X[1] ** 3 - 2
            JacH[0,:] = 1
            JacH[1,0] = 2 * X[0]
            JacH[1,1] = 3 * X[1] ** 2
        if n >= 3:
            H[2] = 3 * np.exp(X[0] - X[-1]) - 3
            JacH[2,0] = 3 * np.exp(X[0] - X[-1])
            JacH[2,-1] = -3 * np.exp(X[0] - X[-1])
        return H,JacH
    return Cons
# --------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------#
# We solve the Rosenbrock function for the following cases:

#   I)      n =  2, 1 Constraint(s), x0 = (2,2)

#   II)     n =  4, 1 Constraint(s), x0 = (2,2,...,2)
#   III)    n =  8, 1 Constraint(s), x0 = (2,2,...,2)
#   IV)     n = 16, 1 Constraint(s), x0 = (2,2,...,2)
#
#   V)      n = 16, 1 Constraint(s), x0 = (-1,-1,...,-1)
#   VI)     n = 16, 1 Constraint(s), x0 = (5,5,...,5)
#   VII)    n = 16, 1 Constraint(s), x0 = (1,2,...,16)
#
# --------------------------------------------------------------------------------------------#
# We define the constraints function.
Cons1 = GetCons(1)

# We define initial guess vectors for each case.
x01 = np.full(2,2)
x02 = np.full(4,2)
x03 = np.full(8,2)
x04 = np.full(16,2)
x05 = np.full(16,-1)
x06 = np.full(16,5)
x07 = np.full(16,25)

# We generate solutions via optimization.
Sol1 = SQP(Rosen,Cons1,x01,None)
print('\n')
print('Success on Case I!')
print('Optimum Point:')
print(Sol1['xStar'])
print('Optimum Value: ',Sol1['fStar'])
print('Iterations: ',Sol1['Iterations'])
print('\n')
Sol4 = SQP(Rosen,Cons1,x02,None)
print('\n')
print('Success on Case II!')
print('Optimum Point:')
print(Sol4['xStar'])
print('Optimum Value: ',Sol4['fStar'])
print('Iterations: ',Sol4['Iterations'])
print('\n')
Sol5 = SQP(Rosen,Cons1,x03,None)
print('\n')
print('Success on Case III!')
print('Optimum Point:')
print(Sol5['xStar'])
print('Optimum Value: ',Sol5['fStar'])
print('Iterations: ',Sol5['Iterations'])
print('\n')
Sol6 = SQP(Rosen,Cons1,x04,None)
print('\n')
print('Success on Case IV!')
print('Optimum Point:')
print(Sol6['xStar'])
print('Optimum Value: ',Sol6['fStar'])
print('Iterations: ',Sol6['Iterations'])
print('Function Calls: ',Sol6['FunctionCalls'])
print('\n')
Sol7 = SQP(Rosen,Cons1,x05,None)
print('\n')
print('Success on Case V!')
print('Optimum Point:')
print(Sol7['xStar'])
print('Optimum Value: ',Sol7['fStar'])
print('Iterations: ',Sol7['Iterations'])
print('Function Calls: ',Sol7['FunctionCalls'])
print('\n')
Sol8 = SQP(Rosen,Cons1,x06,None)
print('\n')
print('Success on Case VI!')
print('Optimum Point:')
print(Sol8['xStar'])
print('Optimum Value: ',Sol8['fStar'])
print('Iterations: ',Sol8['Iterations'])
print('Function Calls: ',Sol8['FunctionCalls'])
print('\n')
Sol9 = SQP(Rosen,Cons1,x07,None)
print('\n')
print('Success on Case VII!')
print('Optimum Point:')
print(Sol9['xStar'])
print('Optimum Value: ',Sol9['fStar'])
print('Iterations: ',Sol9['Iterations'])
print('Function Calls: ',Sol9['FunctionCalls'])
print('\n')
# --------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------#
# We generate contour plots for the three two-dimensional problems (Cases I - III).
# --------------------------------------------------------------------------------------------#
# We generate x1-, x2-, f-, and h-values for the function.
x1R = np.linspace(-1,3.5,500)
x2R = np.linspace(-1,3.5,500)
X1R,X2R = np.meshgrid(x1R,x2R)
FR = np.zeros_like(X1R)
HR1 = np.zeros_like(X2R)
HR2 = np.zeros_like(X2R)
HR3 = np.zeros_like(X2R)
for i in range(X1R.shape[0]):
    for j in range(X1R.shape[1]):
        RosenEval,_ = Rosen((X1R[i,j],X2R[i,j]))
        FR[i,j] = np.log(RosenEval)
        HR1[i,j],_ = Cons1((X1R[i,j],X2R[i,j]))
        # HR2[i,j],_ = Cons2((X1R[i,j],X2R[i,j]))
        # HR3[i,j],_ = Cons3((X1R[i,j],X2R[i,j]))

# We generate plotting values for the slanted quadratic.
ContoursR = np.linspace(0.5,10,20)
x1LimR = [x1R[0],x1R[-1]]
x2LimR = [x2R[0],x2R[-1]]
FileNameR1 = 'Rosen1_PathPlot.svg'
FileNameR2 = 'Rosen2_PathPlot.svg'
FileNameR3 = 'Rosen3_PathPlot.svg'

# We call upon our plotting function.
GeneratePathPlot(
    X1R,
    X2R,
    FR,
    HR1,
    ContoursR,
    Sol1['PointStorage'],
    x1LimR,
    x2LimR,
    (-100,-150),
    FileNameR1,
    False
)
# --------------------------------------------------------------------------------------------#