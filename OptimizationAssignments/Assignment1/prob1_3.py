# AEROSP 588 Fall 2025 - Assignment 1, Problem 3
# Authored By: Austin Leo Thomas
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- 
# We import modules as needed.
# ------------------------------------------------------------------------------------------- #
import matplotlib.pyplot as plot
import numpy as np
from scipy.optimize import minimize
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define the mathematical function.
# ------------------------------------------------------------------------------------------- #
def f(X):
    x1,x2 = X
    f = (1 - x1)**2 + (1 - x2)**2 + 0.5*(2*x2 - x1**2)**2
    return f
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We evaluate the function across a set range.
# ------------------------------------------------------------------------------------------- #
# We define value arrays.
x1Bounds = [-12,50]
x2Bounds = [-12,150]
x1 = np.linspace(x1Bounds[0],x1Bounds[1],5000)
x2 = np.linspace(x2Bounds[0],x2Bounds[1],5000)
X = np.meshgrid(x1,x2)
F = f(X)
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define a plot generation function.
# ------------------------------------------------------------------------------------------- #
def GenPlot(X,F,ContourLevels,Points,LabelPosition,x1Lim,x2Lim,FigName):

    # We define properties of the plot.
    FontSize = 12
    FontType = 'Cambria'
    PointStyle = 'ko-'
    PointSize = 4
    LineWidth = 1
    LabelFontSize = 8
    LabelColor = 'black'

    # We resolve the x1 and x2 components from the X array.
    X1,X2 = X

    # We convert the collection of points to an array.
    Array = np.array(Points)

    # We check the size of Points and reshape as needed.
    if Array.ndim == 1:
        Array = Array.reshape(1,2)

    # We create the contour plot.
    plot.contour(X1,X2,F,cmap = 'Blues_r',levels = ContourLevels,zorder = 1)
    plot.plot(Array[:,0],Array[:,1],PointStyle,markersize = PointSize,
              linewidth = LineWidth,zorder = 2)
    
    # We add iteration labels to the points.
    for i,(x1,x2) in enumerate(Array):
        if i == len(Array) - 1:
            Label = 'x*'
        else:
            Label = i
        if LabelPosition[i] != (0,0):
            plot.annotate(Label,xy = (x1,x2),xytext = LabelPosition[i],
                          textcoords = 'offset points',fontsize = LabelFontSize,
                          ha = 'center',va = 'center',color = LabelColor)
    
    # We finish configuring and saving the plot.
    plot.xlim(x1Lim)
    plot.ylim(x2Lim)
    plot.xticks(fontsize = FontSize,fontname = FontType)
    plot.yticks(fontsize = FontSize,fontname = FontType)
    plot.xlabel(r'$x_1$',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
    plot.ylabel(r'$x_2$',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
    plot.savefig(FigName,bbox_inches = 'tight')
    plot.clf()
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We generate the plot for the graphically-approximated minimum value.
# ------------------------------------------------------------------------------------------- #
# We define approximate minima values.
xStar_Guess = [1.2,0.8]

# We define plot properties.
Contours_Guess = np.linspace(0,4,20)
x1Lim_Guess = [0,2]
x2Lim_Guess = [0,2]
FigName_Guess = 'prob1_3_Guess.svg'
LabelPosition_Guess = [(7,7)]

# We generate the plot.
GenPlot(X,F,Contours_Guess,xStar_Guess,LabelPosition_Guess,x1Lim_Guess,x2Lim_Guess,
        FigName_Guess)
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We will optimize from three different starting points: one close to the minimum one and two
# far from the minimum.
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define a function for path storage during optimization runs.
# ------------------------------------------------------------------------------------------- #
def CreateStorage(PathName):
    def StorePath(xk):
        PathName.append(np.copy(xk))
    return StorePath
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define a function to generate a plot of the function value at the current iteration's
# optimum condition versus the number of iterations.
# ------------------------------------------------------------------------------------------- #
def GenIterPlot(Path,f,FigName):

    # We convert the path to an array.
    Array = np.array(Path)

    # We pre-allocate the i- and f-value lists.
    iList = [0] * len(Array)
    fList = [0] * len(Array)

    # We populate lists of i- and f-values.
    for i,X in enumerate(Array):
        iList[i] = i
        fList[i] = f(X)

    # We define properties of the plot.
    FontSize = 12
    FontType = 'Cambria'
    PointStyle = 'ro-'
    PointSize = 4
    LineWidth = 1

    # We generate and save the plot.
    plot.plot(iList,fList,PointStyle,markersize = PointSize,linewidth = LineWidth)
    plot.xlim([0,iList[-1]])
    plot.ylim([0,1.2*fList[0]])
    plot.xticks(fontsize = FontSize,fontname = FontType)
    plot.yticks(fontsize = FontSize,fontname = FontType)
    plot.xlabel('iteration, i',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
    plot.ylabel('f(x*)',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
    plot.savefig(FigName,bbox_inches = 'tight')
    plot.clf()
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We run optimization for a point near the minumum and plot the optimization path.
# ------------------------------------------------------------------------------------------- #
# We create an empty storage array for the optimization path.
Path_Opt1 = []
CallbackFunc_Opt1 = CreateStorage(Path_Opt1)

# We define the initial guess and add it to the path.
InitialGuess_Opt1 = np.array([0,0])
Path_Opt1.append((InitialGuess_Opt1[0],InitialGuess_Opt1[1]))

# We optimize.
xStar_Opt1 = minimize(f,InitialGuess_Opt1,method = 'BFGS',callback = CallbackFunc_Opt1)

# We define plot properties.
Contours_Opt1 = np.linspace(0,4,20)
x1Lim_Opt1 = [-0,1.5]
x2Lim_Opt1 = [-0,1]
FigName_Opt1 = 'prob1_3_Opt1.svg'
LabelPosition_Opt1 = [(15,5),(5,5),(5,-5),(5,5),(0,-10),(-7,-5),(-8,4),(-2,7),(4,6),(9,0)]

# We generate the contour plot.
GenPlot(X,F,Contours_Opt1,Path_Opt1,LabelPosition_Opt1,x1Lim_Opt1,x2Lim_Opt1,FigName_Opt1)

# We generate the iteration plot.
GenIterPlot(Path_Opt1,f,'prob1_3_IterPlot1.svg')
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We run optimization for a point far from the mininum and plot the optimization path.
# ------------------------------------------------------------------------------------------- #
# We create an empty storage array for the optimization path.
Path_Opt2 = []
CallbackFunc_Opt2 = CreateStorage(Path_Opt2)

# We define the initial guess and add it to the path.
InitialGuess_Opt2 = np.array([30,30])
Path_Opt2.append((InitialGuess_Opt2[0],InitialGuess_Opt2[1]))

# We optimize.
xStar_Opt2 = minimize(f,InitialGuess_Opt2,method = 'BFGS',callback = CallbackFunc_Opt2)

# We define plot properties.
Contours_Opt2 = np.linspace(0,4e5,40)
x1Lim_Opt2 = [0,35]
x2Lim_Opt2 = [0,150]
FigName_Opt2 = 'prob1_3_Opt2.svg'
LabelPosition_Opt2 = [(5,5),(-5,-5),(5,5),(0,-8),(7,5),
                      (7,-1),(7,-2),(7,-3),(5,-6),(5,-7),
                      (0,0),(0,0),(0,0),(0,0),(0,0),
                      (0,0),(0,0),(0,0),(0,0),(0,0),
                      (10,7),(-5,7)]

# We generate the contour plot.
GenPlot(X,F,Contours_Opt2,Path_Opt2,LabelPosition_Opt2,x1Lim_Opt2,x2Lim_Opt2,FigName_Opt2)

# We generate the iteration plot.
GenIterPlot(Path_Opt2,f,'prob1_3_IterPlot2.svg')
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We run optimization for another point far from the mininum and plot the optimization path.
# ------------------------------------------------------------------------------------------- #
# We create an empty storage array for the optimization path.
Path_Opt3 = []
CallbackFunc_Opt3 = CreateStorage(Path_Opt3)

# We define the initial guess and add it to the path.
InitialGuess_Opt3 = np.array([-10,-10])
Path_Opt3.append((InitialGuess_Opt3[0],InitialGuess_Opt3[1]))

# We optimize.
xStar_Opt3 = minimize(f,InitialGuess_Opt3,method = 'BFGS',callback = CallbackFunc_Opt3)

# We define plot properties.
Contours_Opt3 = np.linspace(0,6000,40)
x1Lim_Opt3 = [-12,2]
x2Lim_Opt3 = [-12,18]
FigName_Opt3 = 'prob1_3_Opt3.svg'
LabelPosition_Opt3 = [(-5,5),(-5,-7),(-5,-5),(5,5),(5,5),
                      (5,5),(5,5),(5,5),(5,5),(5,5),
                      (0,0),(0,0),(0,0),(0,0),(0,0),
                      (0,0),(0,0),(0,0),(-5,7),(3,-7)]

# We generate the contour plot.
GenPlot(X,F,Contours_Opt3,Path_Opt3,LabelPosition_Opt3,x1Lim_Opt3,x2Lim_Opt3,FigName_Opt3)

# We generate the iteration plot.
GenIterPlot(Path_Opt3,f,'prob1_3_IterPlot3.svg')
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We print out the three optimization solutions, for reference when writing report.
# ------------------------------------------------------------------------------------------- #
print(xStar_Opt1)
print(xStar_Opt2)
print(xStar_Opt3)
# ------------------------------------------------------------------------------------------- #