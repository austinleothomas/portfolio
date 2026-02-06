# AEROSP 588 Fall 2025 - Assignment 1, Problem 1
# Authored By: Austin Leo Thomas
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- 
# We import modules as needed.
# ------------------------------------------------------------------------------------------- #
import matplotlib.pyplot as plot
import numpy as np
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define the mathematical function.
# ------------------------------------------------------------------------------------------- #
def f(x):
    f = (1/12)*x**4 + x**3 - 16*x**2 + 4*x + 12
    return f
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define a function for plot generation.
# ------------------------------------------------------------------------------------------- #
def PlotGen(xArray,fArray,xPoints,fPoints,xLower,xUpper,fLower,fUpper,FigName):

    # We define properties of the plot.
    FontSize = 12
    FontType = 'Cambria'
    PlotColor = '#990e02'
    PointColor = 'black'
    LabelFontSize = 8
    LabelColor = 'black'

    # We generate and save the plot.
    plot.plot(xArray,fArray,color = PlotColor,zorder = 2)
    plot.scatter(xPoints,fPoints,color = PointColor,zorder = 3)
    plot.xlim([xLower,xUpper])
    plot.ylim([fLower,fUpper])
    plot.xticks(fontsize = FontSize,fontname = FontType)
    plot.yticks(fontsize = FontSize,fontname = FontType)
    plot.xlabel('x',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
    plot.ylabel('f(x)',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')

    if 'Main' in FigName:
        for i in [0,1]:
            if i == 0:
                Label = r'$x^{\ast}_g$'
                LabelPosition = (-5.5,10)
            else:
                Label = r'$x^{\ast}_l$'
                LabelPosition = (0,-10)
            plot.annotate(Label,xy = (xPoints[i],fPoints[i]),xytext = LabelPosition,
                          textcoords = 'offset points',fontsize = LabelFontSize,
                          ha = 'center',va = 'center',color = LabelColor,fontname = FontType)
    elif 'Local' in FigName:
        Label = r'$x^{\ast}_l$'
        LabelPosition = (7,-7)
        plot.annotate(Label,xy = (xPoints[0],fPoints[0]),xytext = LabelPosition,
                      textcoords = 'offset points',fontsize = LabelFontSize,ha = 'center',
                      va = 'center',color = LabelColor,fontname = FontType)
    elif 'Global' in FigName:
        Label = r'$x^{\ast}_g$'
        LabelPosition = (10,0)
        plot.annotate(Label,xy = (xPoints[0],fPoints[0]),xytext = LabelPosition,
                      textcoords = 'offset points',fontsize = LabelFontSize,ha = 'center',
                      va = 'center',color = LabelColor,fontname = FontType)

    plot.grid(True,zorder = 1)
    ax = plot.gca()
    ax.ticklabel_format(useOffset = False)
    plot.savefig(FigName,bbox_inches = 'tight')
    plot.clf()
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We generate the plot.
# ------------------------------------------------------------------------------------------- #
# We define value arrays.
xArray = np.linspace(-25,10,1000)
fArray = [f(x) for x in xArray]

# We define approximate minima values.
xGlobal = -15.25
fGlobal = f(xGlobal)
xLocal = 6.25
fLocal = f(xLocal)

# We generate plots of the full function as well as plots zoomed in near minima.
PlotGen(xArray,fArray,[xGlobal,xLocal],[fGlobal,fLocal],-25,10,-2900,100,'prob1_1_MainPlot.svg')
PlotGen(xArray,fArray,[xGlobal],[fGlobal],xGlobal-0.25,xGlobal+0.25,fGlobal-0.25,fGlobal+0.25,
        'prob1_1_GlobalPlot.svg')
PlotGen(xArray,fArray,[xLocal],[fLocal],xLocal-0.25,xLocal+0.25,fLocal-0.25,fLocal+0.25,
        'prob1_1_LocalPlot.svg')
# ------------------------------------------------------------------------------------------- #