# AEROSP 588 Fall 2025 - Assignment 2, Problem 2
# Authored By: Austin Leo Thomas
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- 
# We import modules as needed.
# ------------------------------------------------------------------------------------------- #
import matplotlib.pyplot as plt
import numpy as np
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We define the mathematical function.
# ------------------------------------------------------------------------------------------- #
def f(x1,x2):
    f = x1**4 + 3*x1**3 + 3*x2**2 -6*x1*x2 -2*x2
    return f
# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# We generate the plot.
# ------------------------------------------------------------------------------------------- #
# We define value arrays.
x1Bounds = [-4,2]
x2Bounds = [-4,2]
x1 = np.linspace(x1Bounds[0],x1Bounds[1],1000)
x2 = np.linspace(x2Bounds[0],x2Bounds[1],1000)
X1,X2 = np.meshgrid(x1,x2)
F = f(X1,X2)

# We define approximate critical values and classify them.
x1Points = [-1/4,-1-np.sqrt(3),-1+np.sqrt(3)]
x2Points = [1/12,-2/3-np.sqrt(3),-2/3+np.sqrt(3)]
fLabels = ['saddle point','global minimum','local minimum']

# We evaluate the function at these critical values and print them to the terminal.
print()
for i,PointID in enumerate(fLabels):
    print('At ' + PointID + ', f = ' + f"{f(x1Points[i],x2Points[i]):.3g}")
print()

# We define properties of the plot.
FontSize = 12
FontType = 'Cambria'
PointColor = 'black'
ContourLevels = np.linspace(-25,25,30)
PointSize = 20
LabelFontSize = 8
LabelColor = 'black'

# We create the contour plot.
plt.contour(X1,X2,F,cmap = 'Blues_r',levels = ContourLevels,zorder = 1)
plt.scatter(x1Points,x2Points,color = PointColor,s = PointSize,zorder = 2)
plt.xlim(x1Bounds)
plt.ylim(x2Bounds)
plt.xticks(fontsize = FontSize,fontname = FontType)
plt.yticks(fontsize = FontSize,fontname = FontType)
plt.xlabel(r'$x_1$',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
plt.ylabel(r'$x_2$',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
for i in range(len(fLabels)):
    plt.annotate(fLabels[i],xy = (x1Points[i],x2Points[i]),xytext = (0,6),
                 textcoords = 'offset points',fontsize = LabelFontSize,ha = 'center',
                 va = 'center',color = LabelColor,fontname = FontType,bbox = dict(
                     facecolor = 'white',edgecolor = 'none',boxstyle = 'round',pad = 0.1))
plt.savefig('prob2_2_Plot.svg',bbox_inches = 'tight')
plt.clf()
# ------------------------------------------------------------------------------------------- #