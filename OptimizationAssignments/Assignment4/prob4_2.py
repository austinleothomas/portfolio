# This script solves Problem 4.3 for AEROSP 588.
# --------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------#
# We import modules as needed.
# --------------------------------------------------------------------------------------------#
from sympy import symbols,Eq,solve
import matplotlib.pyplot as plt
import numpy as np
# --------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------#
# We define our equations.
# --------------------------------------------------------------------------------------------#
# We define the variables.
tb,tw,s1,s2,o1,o2 = symbols('tb tw s1 s2 o1 o2')

# We define the system.
Eq1 = Eq(0.25 - 12500 * o1 * (3 * tb ** 2 / 48 + 1 / 256) / (tw / 768 + tb ** 3 / 48 + tb / 256) **2 , 0)
Eq2 = Eq(0.25 - 12500 * o1 / (768 * (tw / 768 + tb ** 3 / 48 + tb / 256) **2) - 60000 * o2 / tw ** 2 , 0)
Eq3 = Eq(12500 / (tw / 768 + tb ** 3 / 48 + tb / 256) - 2 * 10 ** 8 + s1 ** 2 , 0)
Eq4 = Eq(600000 / tw - 1.16 * 10 ** 8 + s2 ** 2 , 0)
Eq5 = Eq(2 * o1 * s1 , 0)
Eq6 = Eq(2 * o2 * s2 , 0)

# We solve the system.
Sol = solve((Eq1,Eq2,Eq3,Eq4,Eq5,Eq6),(tb,tw,s1,s2,o1,o2))
print('\n')
print('Solutions of form (tb,tw,s1,s2,o1,o2)...')
print('\n')
for sol in Sol:
    print(sol)
    print('\n')
print('\n')
# --------------------------------------------------------------------------------------------#



# --------------------------------------------------------------------------------------------#
# We generate an optimization path plotting function.
# --------------------------------------------------------------------------------------------#
def GeneratePathPlot(X1,X2,F,G1,G2,ContourLevels,x1Lim,x2Lim,FileName,isShow):
    
    # We define properties of the plot.
    FontSize = 11
    FontType = 'Cambria'
    PathColor = '#b31919'
    LineWidth = 1

    # We create the contour plot.
    plt.contour(X1,X2,F,cmap = 'Blues_r',levels = ContourLevels,zorder = 1)
    plt.contour(X1,X2,G1,levels = [0],colors = 'black',zorder = 2)
    plt.contour(X1,X2,G2,levels = [0],colors = 'black',zorder = 2)
    plt.plot(0.0142604,0.0051724,marker = 'o',color = PathColor,linewidth = LineWidth,zorder = 3)

    # We annotate.
    plt.annotate(
        r'$x^*$',
        xy = (0.0142604,0.0051724),
        xytext = (10,10),
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
    plt.xlabel(r'$t_b [m]$',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
    plt.ylabel(r'$t_w [m]$',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
    plt.savefig(FileName,bbox_inches = 'tight')
    if isShow:
        plt.show()
    plt.clf()
# --------------------------------------------------------------------------------------------#

# --------------------------------------------------------------------------------------------#
# We define the function and constraints
# --------------------------------------------------------------------------------------------#
def Func(X):
    tb,tw = X
    F = 2 * 0.125 * tb + 0.25 * tw
    DelF = np.zeros(2)
    DelF[0] = 0.25
    DelF[1] = 0.25
    return F

def Axial(X):
    tb,tw = X
    I = (0.25 ** 3 * tw) / 12 + (0.125 * tb ** 3) / 6 + (0.25 ** 2 * 0.125 * tb) / 2
    G = 100000 * 1 * 0.25 / (2 * I) - 200 * 10 ** 6
    DelG = np.zeros(2)
    DelG[0] = - (12500 / I ** 2) * (3 * tb ** 2 / 48 + 1 / 256)
    DelG[1] = - (12500 / (768 * I **2))
    return G

def Shear(X):
    _,tw = X
    G = (1.5 * 100000) / (0.25 * tw) - 116 * 10 ** 6
    DelG = np.zeros(2)
    DelG[0] = 0
    DelG[1] = - (600000 / tw ** 2)
    return G
# --------------------------------------------------------------------------------------------#

# --------------------------------------------------------------------------------------------#
# We plot.
# --------------------------------------------------------------------------------------------#
# We generate values for the function.
tb = np.linspace(.001,0.03,100)
tw = np.linspace(0.001,0.03,100)
X1,X2 = np.meshgrid(tb,tw)
F = np.zeros_like(X1)
G1 = np.zeros_like(X2)
G2 = np.zeros_like(X2)
for i in range(X1.shape[0]):
    for j in range(X1.shape[1]):
        F[i,j] = Func((X1[i,j],X2[i,j]))
        G1[i,j] = Axial((X1[i,j],X2[i,j]))
        G2[i,j] = Shear((X1[i,j],X2[i,j]))

# We generate plotting values for the exterior path plot.
Contours = np.linspace(0,0.03,30)
x1Lim = [tb[0],tb[-1]]
x2Lim = [tw[0],tw[-1]]
FileName = 'BeamContour.svg'

# We plot.
GeneratePathPlot(
    X1,
    X2,
    F,
    G1,
    G2,
    Contours,
    x1Lim,
    x2Lim,
    FileName,
    True
)
# --------------------------------------------------------------------------------------------#