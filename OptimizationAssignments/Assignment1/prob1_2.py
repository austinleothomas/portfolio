# AEROSP 588 Fall 2025 - Assignment 1, Problem 2
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
def f(x1,x2):
    f = x1**3 + 2*x1*x2**2 - x2**3 - 20*x1
    return f
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We generate the plot.
# ------------------------------------------------------------------------------------------- #
# We define value arrays.
x1Bounds = [-5,5]
x2Bounds = [-5,5]
x1 = np.linspace(x1Bounds[0],x1Bounds[1],1000)
x2 = np.linspace(x2Bounds[0],x2Bounds[1],1000)
X1,X2 = np.meshgrid(x1,x2)
F = f(X1,X2)

# We define approximate minima values.
x1Points = [2.55]
x2Points = [0]

# We define properties of the plot.
FontSize = 12
FontType = 'Cambria'
PointColor = 'black'
ContourLevels = np.linspace(-100,100,10)
PointSize = 20
LabelFontSize = 8
LabelColor = 'black'

# We create the contour plot.
plot.contour(X1,X2,F,cmap = 'Blues_r',levels = ContourLevels,zorder = 1)
plot.scatter(x1Points,x2Points,color = PointColor,s = PointSize,zorder = 2)
plot.xlim(x1Bounds)
plot.ylim(x2Bounds)
plot.xticks(fontsize = FontSize,fontname = FontType)
plot.yticks(fontsize = FontSize,fontname = FontType)
plot.xlabel(r'$x_1$',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
plot.ylabel(r'$x_2$',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
plot.annotate('x*',xy = (x1Points[0],x2Points[0]),xytext = (0,6),textcoords = 'offset points',
              fontsize = LabelFontSize,ha = 'center',va = 'center',color = LabelColor,
              fontname = FontType)
plot.savefig('prob1_2_Plot.svg',bbox_inches = 'tight')
plot.clf()
# ------------------------------------------------------------------------------------------- #