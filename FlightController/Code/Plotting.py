# ---------------------------------------------------------------------------------------------- #
# Plot generation script for final project.
# U-M AEROSP 588 Fall '25.
# Austin Leo Thomas.
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We import modules as needed.
# ---------------------------------------------------------------------------------------------- #
import matplotlib.pyplot as plt
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We generate the NM / DIRECT / GPS plot.
# ---------------------------------------------------------------------------------------------- #
# We decide if we want to save / show.
isSavePlot1 = False
isShowPlot1 = False

# We define plot properties.
FontSize = 12
FontType = 'Cambria'
Colors = ['black','#b31919','#078227','#09229e']
Labels = [
    'Baseline Solution',
    'Nelder-Mead Solution',
    'DIRECT Method Solution',
    'GPS Algorithm Solution'
]

# We define each data set.
Baseline_Calls = [0,700]
Baseline_Vals = [41.279,41.279]
NM_Calls = [0,5,10,20,30,40,50,100,150,200,250,300]
NM_Vals = [41.279,35.892,35.837,35.749,35.596,35.381,35.267,35.177,35.164,35.163,35.163,35.163]
DIRECT_Calls = [0,27,45,65,123,213,335,423,509,626]
DIRECT_Vals = [41.279,28.420,28.386,28.386,27.947,27.841,27.691,27.682,27.677,27.666]
GPS_Calls = [0,5,10,30,50,100,150,200,250,500,700]
GPS_Vals = [41.279,34.128,34.302,35.295,32.956,28.996,29.690,37.896,30.206,31.711,32.386]

# We plot.
plt.plot(Baseline_Calls,Baseline_Vals,label = Labels[0],c = Colors[0])
plt.plot(NM_Calls,NM_Vals,label = Labels[1],c = Colors[1])
plt.plot(DIRECT_Calls,DIRECT_Vals,label = Labels[2],c = Colors[2])
plt.plot(GPS_Calls,GPS_Vals,label = Labels[3],c = Colors[3])

# We configure.
plt.xlim([0,700])
plt.ylim([27,42])
plt.xticks(fontsize = FontSize,fontname = FontType)
plt.yticks(fontsize = FontSize,fontname = FontType)
plt.xlabel('Function Calls',fontsize = FontSize,fontname = FontType)
plt.ylabel('Optimum Flight Time [s]',fontsize = FontSize,fontname = FontType)
plt.legend(loc = 'upper right',framealpha = 1)

# We decide if we want to save /show.
if isSavePlot1:
    plt.savefig('./Figures/NM_DIRECT_GPS_Plot.svg',bbox_inches = 'tight')
if isShowPlot1:
    plt.show()
plt.clf()
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We generate the MDO fStar v Evals plot.
# ---------------------------------------------------------------------------------------------- #
# We decide if we want to save / show.
isSavePlot2 = False
isShowPlot2 = False

# We define plot properties.
FontSize = 12
FontType = 'Cambria'
Colors = ['#b31919']

# We define each data set.
Calls = [209,369,808,1426,2897,3975]
Vals = [30.700,30.287,29.735,28.104,27.544,27.529]

# We plot.
plt.plot(Calls,Vals,c = Colors[0])

# We configure.
plt.xlim([0,4000])
plt.ylim([27,32])
plt.xticks(fontsize = FontSize,fontname = FontType)
plt.yticks(fontsize = FontSize,fontname = FontType)
plt.xlabel('Function Calls',fontsize = FontSize,fontname = FontType)
plt.ylabel('Optimum Flight Time [s]',fontsize = FontSize,fontname = FontType)

# We decide if we want to save /show.
if isSavePlot2:
    plt.savefig('./Figures/MDO_Vals_Plot.svg',bbox_inches = 'tight')
if isShowPlot2:
    plt.show()
plt.clf()
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We generate the MDO fStar v Beta plot.
# ---------------------------------------------------------------------------------------------- #
# We decide if we want to save / show.
isSavePlot3 = False
isShowPlot3 = False

# We define plot properties.
FontSize = 12
FontType = 'Cambria'
Colors = ['#b31919']

# We define each data set.
Calls = [0,209,369,808,1426,2897,3975]
Beta = [1,0.568,0.516,0.505,0.967,1.000,0.983]

# We plot.
plt.plot(Calls,Beta,c = Colors[0])

# We configure.
plt.xlim([0,4000])
plt.ylim([0,1])
plt.xticks(fontsize = FontSize,fontname = FontType)
plt.yticks(fontsize = FontSize,fontname = FontType)
plt.xlabel('Function Calls',fontsize = FontSize,fontname = FontType)
plt.ylabel('Scaling Parameter, $\\beta$',fontsize = FontSize,fontname = FontType)

# We decide if we want to save /show.
if isSavePlot3:
    plt.savefig('./Figures/MDO_Beta_Plot.svg',bbox_inches = 'tight')
if isShowPlot3:
    plt.show()
plt.clf()
# ---------------------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------------------- #
# We generate the MDO fStar v Beta plot.
# ---------------------------------------------------------------------------------------------- #
# We decide if we want to save / show.
isSavePlot4 = False
isShowPlot4 = True

# We define plot properties.
FontSize = 12
FontType = 'Cambria'
Colors = ['#b31919']

# We define each data set.
Calls = [0,209,369,808,1426,2897,3975]
Phi = [6998,10010,10367,10445,7222,6988,7332]

# We plot.
plt.plot(Calls,Phi,c = Colors[0])

# We configure.
plt.xlim([0,4000])
plt.ylim([6500,11000])
plt.xticks(fontsize = FontSize,fontname = FontType)
plt.yticks(fontsize = FontSize,fontname = FontType)
plt.xlabel('Function Calls',fontsize = FontSize,fontname = FontType)
plt.ylabel('Control Effort, $\\phi$',fontsize = FontSize,fontname = FontType)

# We decide if we want to save /show.
if isSavePlot4:
    plt.savefig('./Figures/MDO_Phi_Plot.svg',bbox_inches = 'tight')
if isShowPlot4:
    plt.show()
plt.clf()
# ---------------------------------------------------------------------------------------------- #