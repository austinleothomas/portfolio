# Module package for Assignment 5 of U-M Fall 2025 AEROSP 588.
# Authored By: Austin Leo Thomas
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We import modules as needed.
# ---------------------------------------------------------------------------------------------- #
import numpy as np
import matplotlib.pyplot as plt
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define a function to generate a logarithmic array given the starting and ending powers
# of ten. That is, the function generate an array of the form...
# 
#   => [1e-m,...,1e-n] for m > n
# ---------------------------------------------------------------------------------------------- #
def GenLogArray(m,n,Width):
    Array = []
    for i in range(m-1,n-1,-1):
        for j in range(1,Width):
            Array.append(j * 10 ** i)
    Array.append(10 ** m)
    Array = np.sort(Array)
    Array = [f"{x:.0e}" for x in Array]
    Array = [float(x) for x in Array]
    return Array
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define an error plotting function.
# ---------------------------------------------------------------------------------------------- #
def GenErrorPlot(AbscissaVals,OrdinateVals,OrdinateNames,aLim,oLim,FileName,isLegend,isShow):

    # We define plot properties.
    FontSize = 12
    FontType = 'Cambria'
    LineColors = ['#b31919','#0a820e','#072587','#ab0a95']
    LineWidth = 1

    # We plot the data.
    for i,Data in enumerate(OrdinateVals):
        plt.plot(
            AbscissaVals,
            Data,
            color = LineColors[i],
            linewidth = LineWidth,
            label = OrdinateNames[i]
            )

    # We configure the plot.
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(aLim)
    plt.ylim(oLim)
    plt.xticks(fontsize = FontSize,fontname = FontType)
    plt.yticks(fontsize = FontSize,fontname = FontType)
    plt.xlabel(r'step size, $\mathregular{h}$',fontsize = FontSize,fontname = FontType,
               fontstyle = 'italic')
    plt.ylabel(r'relative error, $\mathregular{\epsilon}$',fontsize = FontSize,
               fontname = FontType,fontstyle = 'italic')
    if isLegend:
        plt.legend(loc ='best')
    plt.savefig(FileName,bbox_inches = 'tight')
    
    # We show the graph, if requested, and close it.
    if isShow:
        plt.show()
    plt.clf()
# ---------------------------------------------------------------------------------------------- #
