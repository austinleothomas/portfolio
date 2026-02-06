# Module package for U-M Fall 2025 AEROSP 588.
# Authored By: Austin Leo Thomas
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We import modules as needed.
# ---------------------------------------------------------------------------------------------- #
import numpy as np
import matplotlib.pyplot as plt
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define a sub-function to generate a single plot of an evolutionary algoritm iteration.
# ---------------------------------------------------------------------------------------------- #
def ParticlePlotter(X1,X2,F,Points,Contours,xLow,xHigh,Iter,FileName,isLabel,isShow,isSave):

    # We define plot properties.
    FontSize = 12
    FontType = 'Cambria'
    PointColor = '#b31919'

    # We ensure Points is a numpy array.
    Points = np.asarray(Points)

    # We generate the plot.
    plt.contour(X1,X2,F,cmap = 'Blues_r',levels = Contours,zorder = 1)
    plt.scatter(Points[:,0],Points[:,1],c = PointColor,zorder = 2)

    # We configure the plot.
    plt.xlim([xLow[0],xHigh[0]])
    plt.ylim([xLow[1],xHigh[1]])
    plt.xticks(fontsize = FontSize,fontname = FontType)
    plt.yticks(fontsize = FontSize,fontname = FontType)
    plt.xlabel(r'$x_1$',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
    plt.ylabel(r'$x_2$',fontsize = FontSize,fontname = FontType,fontstyle = 'italic')
    if isLabel:
        plt.title('Iter ' + str(Iter),fontsize = FontSize,fontname = FontType,
                  fontstyle = 'italic')

    # We display and save the graph, as requested.
    if isSave:
        plt.savefig(FileName,bbox_inches = 'tight')
    if isShow:
        plt.show()
    plt.clf()
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We define an evolutionary algorithm particle / population plotter a la Ex. (7.7) in the text.
# ---------------------------------------------------------------------------------------------- #
def MultiParticlePlotter(X1,X2,F,PointStorage,Contours,EndIter,CritIters,xLow,xHigh,FileName,
                    isLabel,isShow,isSave):

    # We create file names.
    FileNames = []
    for i in range(len(CritIters)):
        FileNames.append(FileName + '_Iter' + str(CritIters[i]) + '.svg')
    FileNames.append(FileName + '_Iter' + str(EndIter) + '.svg')
    
    # We generate plots for each critical iteration.
    for Index,Iter in enumerate(CritIters):
        if Iter < EndIter:
            ParticlePlotter(
                X1,
                X2,
                F,
                PointStorage[Iter],
                Contours,
                xLow,
                xHigh,
                Iter,
                FileNames[Index],
                isLabel,
                isShow,
                isSave
            )
        else:
            ParticlePlotter(
                X1,
                X2,
                F,
                PointStorage[EndIter - 1],
                Contours,
                xLow,
                xHigh,
                EndIter,
                FileNames[-1],
                isLabel,
                isShow,
                isSave
            )
            return
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
